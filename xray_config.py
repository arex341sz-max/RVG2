"""xray_manager.py — مدیریت Xray با لاگ‌گیری دقیق stderr"""
import asyncio
import logging
import signal
import time
from pathlib import Path

from config      import XRAY_BIN, XRAY_MAIN_CFG

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


async def start_xray() -> bool:
    global _process, _start_time, _running

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

        # stderr رو در background بخون تا buffer پر نشه
        stderr_lines: list[str] = []

        async def _collect_stderr():
            try:
                async for line in _process.stderr:
                    text = line.decode("utf-8", errors="replace").rstrip()
                    if text:
                        stderr_lines.append(text)
            except Exception:
                pass

        stderr_task = asyncio.create_task(_collect_stderr())
        await asyncio.sleep(3)

        if _process.returncode is not None:
            try:
                await asyncio.wait_for(stderr_task, timeout=2.0)
            except asyncio.TimeoutError:
                stderr_task.cancel()

            # ✅ لاگ کامل و واضح stderr
            if stderr_lines:
                logger.error("═══ Xray STDERR ══════════════════════")
                for line in stderr_lines:
                    logger.error(f"  {line}")
                logger.error("══════════════════════════════════════")
            else:
                logger.error("(Xray stderr was empty)")

            logger.error(f"❌ Xray crashed (rc={_process.returncode})")
            return False

        asyncio.create_task(_pipe_stdout(_process.stdout))
        stderr_task.cancel()
        asyncio.create_task(_pipe_stderr_bg(stderr_lines))

        logger.info("✅ Xray is running")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to start Xray: {e}")
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
    _process = None


async def restart_xray() -> bool:
    global _restart_count
    logger.info("🔄 Restarting Xray...")
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
        logger.info("🔃 Xray reloaded (SIGHUP)")
        return True
    except Exception as e:
        logger.warning(f"SIGHUP failed: {e} → restart")
        return await restart_xray()


async def monitor_loop() -> None:
    global _running
    consecutive = 0
    while _running:
        await asyncio.sleep(5)
        if not _running:
            break
        if _process is None or _process.returncode is not None:
            consecutive += 1
            backoff = min(consecutive * 3, 45)
            if backoff > 5:
                logger.warning(f"⏳ Backoff {backoff}s...")
                await asyncio.sleep(backoff)
            ok = await start_xray()
            if ok:
                consecutive = 0
        else:
            consecutive = 0


async def start_monitor() -> None:
    global _monitor_task
    ok = await start_xray()
    # حتی اگه start نشد monitor رو شروع کن تا retry کنه
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


async def _pipe_stdout(stream) -> None:
    try:
        async for line in stream:
            text = line.decode("utf-8", errors="replace").rstrip()
            if text:
                logger.info(f"[xray] {text}")
    except Exception:
        pass


async def _pipe_stderr_bg(already_collected: list[str]) -> None:
    for line in already_collected:
        logger.warning(f"[xray/ERR] {line}")
    if _process and _process.stderr:
        try:
            async for line in _process.stderr:
                text = line.decode("utf-8", errors="replace").rstrip()
                if text:
                    logger.warning(f"[xray/ERR] {text}")
        except Exception:
            pass
