"""xray_manager.py — اجرا، مانیتور و ری‌استارت Xray به عنوان subprocess"""
import asyncio
import logging
import os
import signal
import time
from pathlib import Path

from config      import XRAY_BIN, XRAY_MAIN_CFG
from xray_config import write_xray_config

logger = logging.getLogger("RVG.xray")

_process:      asyncio.subprocess.Process | None = None
_start_time:   float = 0.0
_restart_count: int  = 0
_running:       bool = False
_monitor_task:  asyncio.Task | None = None


def is_running() -> bool:
    return _process is not None and _process.returncode is None


def get_status() -> dict:
    return {
        "running":        is_running(),
        "pid":            _process.pid if _process else None,
        "uptime_secs":    int(time.time() - _start_time) if _start_time else 0,
        "restart_count":  _restart_count,
        "bin":            XRAY_BIN,
        "config":         XRAY_MAIN_CFG,
        "bin_exists":     Path(XRAY_BIN).exists(),
    }


async def start_xray() -> bool:
    global _process, _start_time, _restart_count, _running

    if not Path(XRAY_BIN).exists():
        logger.error(f"❌ Xray binary not found: {XRAY_BIN}")
        return False

    await write_xray_config()

    try:
        _process = await asyncio.create_subprocess_exec(
            XRAY_BIN, "run", "-c", XRAY_MAIN_CFG,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _start_time = time.time()
        _running    = True
        logger.info(f"🚀 Xray started — PID {_process.pid}")

        asyncio.create_task(_pipe_logs(_process.stdout, "OUT"))
        asyncio.create_task(_pipe_logs(_process.stderr, "ERR"))
        return True
    except Exception as e:
        logger.error(f"❌ Xray start failed: {e}")
        return False


async def stop_xray() -> None:
    global _process, _running
    _running = False
    if _process and _process.returncode is None:
        try:
            _process.send_signal(signal.SIGTERM)
            await asyncio.wait_for(_process.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            _process.kill()
        except Exception:
            pass
        logger.info("🛑 Xray stopped")
    _process = None


async def restart_xray() -> bool:
    global _restart_count
    logger.info("🔄 Restarting Xray…")
    await stop_xray()
    await asyncio.sleep(0.5)
    ok = await start_xray()
    if ok:
        _restart_count += 1
    return ok


async def reload_xray() -> bool:
    if not is_running():
        return await restart_xray()
    await write_xray_config()
    try:
        _process.send_signal(signal.SIGHUP)
        logger.info("🔃 Xray config reloaded (SIGHUP)")
        return True
    except Exception as e:
        logger.warning(f"SIGHUP failed: {e} — falling back to restart")
        return await restart_xray()


async def monitor_loop() -> None:
    global _running
    _running = True
    consecutive_crashes = 0

    while _running:
        await asyncio.sleep(5)
        if not _running:
            break
        if _process is None or _process.returncode is not None:
            rc = _process.returncode if _process else "N/A"
            logger.warning(f"⚠️  Xray exited (rc={rc}) — restarting…")
            consecutive_crashes += 1
            backoff = min(consecutive_crashes * 2, 30)
            if backoff > 2:
                logger.warning(f"⏳ Backoff {backoff}s (crashes={consecutive_crashes})")
                await asyncio.sleep(backoff)
            ok = await start_xray()
            if ok:
                consecutive_crashes = 0
        else:
            consecutive_crashes = 0


async def start_monitor() -> None:
    global _monitor_task
    ok = await start_xray()
    if ok:
        _monitor_task = asyncio.create_task(monitor_loop())


async def stop_monitor() -> None:
    global _running, _monitor_task
    _running = False
    if _monitor_task:
        _monitor_task.cancel()
        try:
            await _monitor_task
        except asyncio.CancelledError:
            pass
    await stop_xray()


async def _pipe_logs(stream: asyncio.StreamReader | None, prefix: str) -> None:
    if not stream:
        return
    try:
        async for line in stream:
            text = line.decode("utf-8", errors="replace").rstrip()
            if text:
                # ERR رو با WARNING لاگ کن تا توی لاگ ظاهر بشه
                if prefix == "ERR":
                    logger.warning(f"[xray/{prefix}] {text}")
                else:
                    logger.debug(f"[xray/{prefix}] {text}")
    except Exception:
        pass
