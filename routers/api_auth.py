from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from auth  import (SESSION_COOKIE, SESSION_TTL, hash_password,
                   create_session, destroy_session, is_valid_session, require_auth)
from state import AUTH, SESSIONS, SESSIONS_LOCK
from config import SESSION_TTL
import time

router = APIRouter()


@router.post("/api/login")
async def login(request: Request):
    body = await request.json()
    if hash_password(str(body.get("password", ""))) != AUTH["password_hash"]:
        raise HTTPException(status_code=401, detail="رمز عبور اشتباه است")
    token = await create_session()
    resp  = JSONResponse({"ok": True})
    resp.set_cookie(SESSION_COOKIE, token, max_age=SESSION_TTL,
                    httponly=True, samesite="lax", path="/")
    return resp


@router.post("/api/logout")
async def logout(request: Request):
    await destroy_session(request.cookies.get(SESSION_COOKIE))
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(SESSION_COOKIE, path="/")
    return resp


@router.get("/api/me")
async def me(request: Request):
    return {"authenticated": await is_valid_session(request.cookies.get(SESSION_COOKIE))}


@router.post("/api/change-password")
async def change_password(request: Request, token: str = Depends(require_auth)):
    body = await request.json()
    if hash_password(str(body.get("current_password", ""))) != AUTH["password_hash"]:
        raise HTTPException(status_code=400, detail="رمز فعلی اشتباه است")
    new = str(body.get("new_password", ""))
    if len(new) < 4:
        raise HTTPException(status_code=400, detail="رمز جدید حداقل ۴ کاراکتر")
    AUTH["password_hash"] = hash_password(new)
    async with SESSIONS_LOCK:
        SESSIONS.clear()
        SESSIONS[token] = time.time() + SESSION_TTL
    from core.persistence import save_state
    await save_state()
    return {"ok": True}
