from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, HTMLResponse, RedirectResponse, StreamingResponse
from fastapi import FastAPI, Cookie, HTTPException
import utility
from authorization import authorization
app = FastAPI()

# auth: Optional[str] = Cookie(None)

auth = authorization()

@app.get("/managebac", response_class=PlainTextResponse)
async def managebac(username: str, password: str, rt: str):
    return auth.managebac(username, password, rt)

@app.get("/rsk", response_class=PlainTextResponse)
async def rsk():
    return utility.rsk
    
@app.get("/login", response_class=PlainTextResponse)
async def login(username: str, password: str, rt: str):
    return auth.logIn(username, password, rt)

@app.get("/signup", response_class=PlainTextResponse)
async def signup(username: str, password: str, managebactoken: str, rt: str):
    return auth.signUp(username, password, managebactoken, rt)