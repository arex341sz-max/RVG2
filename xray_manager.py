"""xray_manager.py — مدیریت Xray با لاگ‌گیری قوی"""
import asyncio
import logging
import signal
import time
from pathlib import Path

from config      import XRAY_BIN, XRAY_MAIN_CFG
from xray_config import write_xray_config

logger = logging.getLogger("RVG.xray")

_process:       asyncio.subprocess.Process | None = None
_start_time:    float = 0.0
_restart_count: int   = 0
_running:       bool  = False
_monitor_task:  asyncio.Task | None = None


def is_running() -> bool:
    return _process is not None and _process.returncode is None


def get_status() -> dict:
    return {
        "running":       is_running(),
        "pid":           _process.pid if _process else None,
        "uptime_secs":   int(time.time() - _start_time) if _start_time else 0,
        "restart_count": _restart_count,
        "bin":           XRAY_BIN,
        "config":        XRAY_MAIN_CFG,
        "bin_exists":    Path(XRAY_BIN).exists(),
    }


async def _read_full_stderr(process) -> str:
    try:
        stderr_out = await asyncio.wait_for(process.stderr.read(), timeout=5.0)
        return stderr_out.decode("utf-8", errors="replace").strip()
    except Exception as e:
        return f"Failed to read stderr: {e}"


async def _log_config_for_debug():
    try:
        if Path(XRAY_MAIN_CFG).exists():
            with open(XRAY_MAIN_CFG, "r", encoding="utf-8") as f:
                config_content = f.read()
            logger.error(f"[Xray Config Content]:\n{config_content}")
    except Exception as e:
        logger.error(f"Could not read config for debug: {e}")


async def start_xray() -> bool:
    global _process, _start_time, _running

    if not Path(XRAY_BIN).exists():
        logger.error(f"❌ Xray binary not found: {XRAY_BIN}")
        return False

    logger.info(f"📝 Writing Xray config → {XRAY_MAIN_CFG}")
    await write_xray_config()

    try:
        logger.info(f"🚀 Starting Xray: {XRAY_BIN} run -c {XRAY_MAIN_CFG}")

        _process = await asyncio.create_subprocess_exec(
            XRAY_BIN, "run", "-c", XRAY_MAIN_CFG,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _start_time = time.time()
        _running = True
        logger.info(f"✅ Xray started — PID {_process.pid}")

        await asyncio.sleep(3)

        if _process.returncode is not None:
            stderr_text = await _read_full_stderr(_process)
            if stderr_text:
                for line in stderr_text.splitlines():
                    logger.error(f"[xray/STDERR] {line}")
            await _log_config_for_debug()
            logger.error(f"❌ Xray crashed immediately (rc={_process.returncode})")
            return False

        asyncio.create_task(_pipe_logs(_process.stdout, "OUT"))
        asyncio.create_task(_pipe_logs(_process.stderr, "ERR"))
        logger.info("✅ Xray is running successfully")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to start Xray: {e}")
        await _log_config_for_debug()
        return False


async def stop_xray() -> None:
    global _process, _running
    _running = False
    if _process and _process.returncode is None:
        try:
            logger.info(f"🛑 Stopping Xray (PID {_process.pid})")
            _process.send_signal(signal.SIGTERM)
            await asyncio.wait_for(_process.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            logger.warning("Force killing Xray...")
            _process.kill()
        except Exception as e:
            logger.warning(f"Error stopping Xray: {e}")
        logger.info("🛑 Xray stopped")
    _process = None


async def restart_xray() -> bool:
    global _restart_count
    logger.info("🔄 Restarting Xray...")
    await stop_xray()
    await asyncio.sleep(1)
    ok = await start_xray()
    if ok:
        _restart_count += 1
    return ok


async def reload_xray() -> bool:
    """این تابع توسط api_links.py و api_xray.py import می‌شود"""
    if not is_running():
        logger.warning("Xray not running → full restart")
        return await restart_xray()
    
    await write_xray_config()
    try:
        _process.send_signal(signal.SIGHUP)
        logger.info("🔃 Xray reloaded via SIGHUP")
        return True
    except Exception as e:
        logger.warning(f"SIGHUP failed: {e} → restarting")
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
            logger.warning(f"⚠️ Xray exited (rc={rc}) — restarting...")
            consecutive_crashes += 1
            backoff = min(consecutive_crashes * 3, 45)
            if backoff > 5:
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
                if prefix == "ERR":
                    logger.warning(f"[xray/{prefix}] {text}")
                else:
                    logger.info(f"[xray/{prefix}] {text}")
    except Exception:
        pass
