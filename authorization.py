import requests
import re
import random
from config import config
import time
import _thread
import sqlite3
import threading
from contextlib import contextmanager
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi import HTTPException


_local = threading.local()


@contextmanager
def acquire(*locks):
    locks = sorted(locks, key=lambda x: id(x))
    acquired = getattr(_local, 'acquired', [])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('Lock Order Violation')
    acquired.extend(locks)
    _local.acquired = acquired
    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]


class authorization:
    def __init__(self, dbp="./authorization.db", interval=900):
        self.interval = interval
        self.conn = sqlite3.connect(dbp, check_same_thread=False, timeout=5)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS ACCOUNTS
           (USERNAME TEXT,
            PASSWORD TEXT,
            PERMISSION NUMBER,
            MANAGEBACID NUMBER);''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS MANAGEBACCACHE
           (USERNAME TEXT,
            PASSWORD TEXT,
            CTIME NUMBER);''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS SESSIONS
           (COOKIE TEXT,
            USERNAME TEXT,
            CTIME NUMBER);''')
        self.conn.commit()
        _thread.start_new_thread(self.expire, ())
        self.Lock = threading.Lock()

    def setCookie(self, username):
        cookie = ''.join(random.sample(
            "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+{}|-=[]\\:\";',./<>?", 50))
        with acquire(self.Lock):
            self.cur.execute("INSERT INTO SESSIONS VALUES(?, ?, ?)",
                             (cookie, username, int(time.time()), ))
            self.conn.commit()
        return cookie

    def manageBacT2U(self, token):
        with acquire(self.Lock):
            self.cur.execute(
                "SELECT * FROM MANAGEBACTOKENS WHERE TOKEN = ?", (token,))
            r = self.cur.fetchall()
        return r

    def reCaptcha(self, token):  # To Do v3
        rcfg = config("./reCaptcha.json")
        if rcfg["no_authorization"]:
            return True
        payload = {
            "secret": rcfg["secret"],
            "response": token
        }
        r = requests.post(
            "https://recaptcha.net/recaptcha/api/siteverify", data=payload).json()
        if r["success"] and r["score"] > rcfg["threshold"]:
            return True
        else:
            return False

    def randomToken(self):
        return ''.join(random.sample(
            "abcdefghijklmnopqrstuvwxyz1234567890", 36))

    def expire(self):
        while True:
            self.conn.execute(
                "DELETE FROM SESSIONS WHERE CTIME < ?", (int(time.time()) - self.interval,))
            self.conn.execute(
                "DELETE FROM MANAGEBACCACHE WHERE CTIME < ?", (int(time.time()) - 7777777,))
            self.conn.commit()
            time.sleep(60)

    def getPermission(self, USERNAME, PASSWORD=None):
        with acquire(self.Lock):
            self.cur.execute(
                "SELECT * FROM ACCOUNTS WHERE USERNAME = ?", (USERNAME,))
            r = self.cur.fetchall()
        if r:
            if not PASSWORD == None:
                if PASSWORD == r[0][1]:
                    return r[0][2]
                else:
                    return 0
            else:
                return r[0][1]
        else:
            return 0

    def login_managebac(self, username, password, rt):
        if not self.reCaptcha(rt):
            raise HTTPException(status_code=401, detail="Robots go away")
        # Query in cache
        with acquire(self.Lock):
            self.cur.execute(
                "SELECT * FROM MANAGEBACCACHE WHERE USERNAME = ? AND PASSWORD = ?", (username, password,))
            r = self.cur.fetchall()
        if r:
            return {"token": self.setCookie(username)}
        # Try to log in
        ua = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        session = requests.Session()
        text = session.get("https://bgy.managebac.cn/login", headers=ua).text
        tmp = re.search(
            r"""<meta name="csrf-token" \/?[a-zA-Z]+("[^"]*"|'[^']*'|[^'">])*>""", text).group()
        tmp = tmp[tmp.find("content="):]
        authenticity_token = tmp[tmp.find("\"") + 1: tmp.rfind("\"")]
        payload = {
            "authenticity_token": authenticity_token,
            "login": username,
            "password": password,
            "remember_me": 0,
            "commit": "Sign-in"
        }
        r = session.post("https://bgy.managebac.cn/sessions",
                         data=payload, headers=ua)
        reditList = r.history
        if reditList and reditList[len(reditList)-1].headers["location"] == "https://bgy.managebac.cn/student/home":
            with acquire(self.Lock):
                self.cur.execute("INSERT INTO MANAGEBACCACHE VALUES(?, ?, ?)",
                                 (username, password, int(time.time()), ))
                self.conn.commit()
            return {"token": self.setCookie(username)}
        # All login attempts failed
        raise HTTPException(
            status_code=401, detail="Wrong password or username does not exist")
