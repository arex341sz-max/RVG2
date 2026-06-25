"""auth.py — session + password management"""
import asyncio
import hashlib
import secrets
import time

from fastapi import HTTPException, Request

from config import SECRET_KEY, SESSION_TTL, ADMIN_PW
from state  import AUTH, SESSIONS, SESSIONS_LOCK

SESSION_COOKIE = "rvg_session"


def hash_password(pw: str) -> str:
    return hashlib.sha256(f"{pw}{SECRET_KEY}".encode()).hexdigest()


def init_auth() -> None:
    AUTH["password_hash"] = hash_password(ADMIN_PW)


async def create_session() -> str:
    token = secrets.token_urlsafe(32)
    async with SESSIONS_LOCK:
        SESSIONS[token] = time.time() + SESSION_TTL
    return token


async def is_valid_session(token: str | None) -> bool:
    if not token:
        return False
    async with SESSIONS_LOCK:
        exp = SESSIONS.get(token)
        if exp is None:
            return False
        if exp < time.time():
            SESSIONS.pop(token, None)
            return False
        return True


async def destroy_session(token: str | None) -> None:
    if not token:
        return
    async with SESSIONS_LOCK:
        SESSIONS.pop(token, None)


async def require_auth(request: Request) -> str:
    token = request.cookies.get(SESSION_COOKIE)
    if not await is_valid_session(token):
        raise HTTPException(status_code=401, detail="unauthorized")
    return token
