"""routers/api_xray.py — مدیریت Xray از داشبورد"""
import asyncio
from fastapi import APIRouter, Depends

from auth         import require_auth
from xray_manager import get_status, restart_xray, reload_xray, start_xray, stop_xray
from xray_config  import get_port_map

router = APIRouter()


@router.get("/api/xray/status")
async def xray_status(_=Depends(require_auth)):
    return get_status()


@router.post("/api/xray/restart")
async def xray_restart(_=Depends(require_auth)):
    ok = await restart_xray()
    return {"ok": ok}


@router.post("/api/xray/reload")
async def xray_reload(_=Depends(require_auth)):
    """reload config بدون restart (SIGHUP)"""
    ok = await reload_xray()
    return {"ok": ok}


@router.post("/api/xray/start")
async def xray_start(_=Depends(require_auth)):
    ok = await start_xray()
    return {"ok": ok}


@router.post("/api/xray/stop")
async def xray_stop(_=Depends(require_auth)):
    await stop_xray()
    return {"ok": True}


@router.get("/api/xray/ports")
async def xray_ports(_=Depends(require_auth)):
    """نقشه UUID → port اختصاصی Xray"""
    return {"port_map": get_port_map()}
