from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, HTMLResponse, RedirectResponse, StreamingResponse, JSONResponse
from fastapi import FastAPI, Cookie, HTTPException
from authorization import authorization
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginForm(BaseModel):
    username: str
    password: str
    rt: str


auth = authorization()


@app.post("/login/managebac", response_class=JSONResponse)
async def login_managebac(form: LoginForm):
    return auth.login_managebac(form.username, form.password, form.rt)
