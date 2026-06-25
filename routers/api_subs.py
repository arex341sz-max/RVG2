"""routers/api_subs.py — گروه‌های ساب"""
import asyncio
import secrets
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request

from auth             import hash_password, require_auth
from config           import PUBLIC_DOMAIN
from core.persistence import save_state
from link_manager     import generate_uuid, fmt_bytes, is_allowed
from state            import LINKS, LINKS_LOCK, SUBS, SUBS_LOCK
import os

router = APIRouter()


def _host():
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", PUBLIC_DOMAIN)


@router.post("/api/subs")
async def create_sub(request: Request, _=Depends(require_auth)):
    body     = await request.json()
    name     = (body.get("name") or "گروه جدید").strip()[:60]
    desc     = (body.get("desc") or "").strip()[:200]
    password = (body.get("password") or "").strip()
    sub_id   = generate_uuid()
    uuid_key = secrets.token_urlsafe(16)
    async with SUBS_LOCK:
        SUBS[sub_id] = {
            "name":          name,
            "desc":          desc,
            "password_hash": hash_password(password) if password else None,
            "uuid_key":      uuid_key,
            "created_at":    datetime.now().isoformat(),
            "link_ids":      [],
        }
    asyncio.create_task(save_state())
    host = _host()
    return {"sub_id": sub_id, **SUBS[sub_id], "password_hash": None,
            "has_password": bool(password),
            "public_url": f"https://{host}/p/{uuid_key}",
            "sub_url":    f"https://{host}/sub-group/{uuid_key}"}


@router.get("/api/subs")
async def list_subs(_=Depends(require_auth)):
    host = _host()
    async with SUBS_LOCK:
        snap_subs = dict(SUBS)
    async with LINKS_LOCK:
        snap_links = dict(LINKS)
    result = []
    for sid, s in snap_subs.items():
        ids          = s.get("link_ids", [])
        active_count = sum(1 for lid in ids if is_allowed(snap_links.get(lid)))
        total_used   = sum(snap_links[lid].get("used_bytes", 0) for lid in ids if lid in snap_links)
        result.append({
            "sub_id": sid, **s, "password_hash": None,
            "has_password":    s.get("password_hash") is not None,
            "links_count":     len(ids),
            "active_count":    active_count,
            "total_used_bytes":total_used,
            "total_used_fmt":  fmt_bytes(total_used),
            "public_url":      f"https://{host}/p/{s['uuid_key']}",
            "sub_url":         f"https://{host}/sub-group/{s['uuid_key']}",
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"subs": result}


@router.patch("/api/subs/{sub_id}")
async def update_sub(sub_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(404, "sub not found")
        s = SUBS[sub_id]
        if "name" in body:
            s["name"] = str(body["name"])[:60]
        if "desc" in body:
            s["desc"] = str(body["desc"])[:200]
        if "password" in body:
            pw = str(body["password"]).strip()
            s["password_hash"] = hash_password(pw) if pw else None
        if "link_ids" in body:
            s["link_ids"] = list(body["link_ids"])
    asyncio.create_task(save_state())
    return {"ok": True}


@router.delete("/api/subs/{sub_id}")
async def delete_sub(sub_id: str, _=Depends(require_auth)):
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(404, "sub not found")
        del SUBS[sub_id]
    async with LINKS_LOCK:
        for link in LINKS.values():
            if link.get("sub_id") == sub_id:
                link["sub_id"] = None
    asyncio.create_task(save_state())
    return {"ok": True, "deleted": sub_id}


@router.post("/api/subs/{sub_id}/links")
async def assign_link(sub_id: str, request: Request, _=Depends(require_auth)):
    body    = await request.json()
    link_id = str(body.get("link_id", ""))
    action  = str(body.get("action", "add"))
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(404, "sub not found")
        ids = SUBS[sub_id].setdefault("link_ids", [])
        if action == "add":
            if link_id not in ids:
                ids.append(link_id)
        else:
            if link_id in ids:
                ids.remove(link_id)
    async with LINKS_LOCK:
        if link_id in LINKS:
            LINKS[link_id]["sub_id"] = sub_id if action == "add" else None
    asyncio.create_task(save_state())
    return {"ok": True}
