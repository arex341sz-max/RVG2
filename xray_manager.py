"""xray_manager.py — مدیریت Xray با لاگ‌گیری دقیق و کامل"""
import asyncio
import logging
import os
import signal
import time
from pathlib import Path

from config      import XRAY_BIN, XRAY_MAIN_CFG, XRAY_CERT_FILE, XRAY_KEY_FILE

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
        "cert_exists":   Path(XRAY_CERT_FILE).exists(),
        "key_exists":    Path(XRAY_KEY_FILE).exists(),
    }


def _preflight_check() -> list[str]:
    """بررسی همه پیش‌نیازها قبل از start — لیست خطاها رو برمی‌گردونه"""
    errors = []
    if not Path(XRAY_BIN).exists():
        errors.append(f"Xray binary not found: {XRAY_BIN}")
    else:
        if not os.access(XRAY_BIN, os.X_OK):
            errors.append(f"Xray binary is not executable: {XRAY_BIN}")

    if not Path(XRAY_CERT_FILE).exists():
        errors.append(f"TLS cert not found: {XRAY_CERT_FILE}")
    if not Path(XRAY_KEY_FILE).exists():
        errors.append(f"TLS key not found: {XRAY_KEY_FILE}")

    cfg_path = Path(XRAY_MAIN_CFG)
    if cfg_path.exists():
        import json
        try:
            with open(cfg_path) as f:
                json.load(f)
        except Exception as e:
            errors.append(f"Xray config JSON is invalid: {e}")
    return errors


async def start_xray() -> bool:
    global _process, _start_time, _running
    
    # Import locally to avoid circular import
    from xray_config import write_xray_config

    await write_xray_config()
    errors = _preflight_check()
    if errors:
        logger.error("═══ Xray PREFLIGHT FAILED ══════════════════")
        for e in errors:
            logger.error(f"  ✗ {e}")
        logger.error("════════════════════════════════════════════")
        return False

    try:
        _process = await asyncio.create_subprocess_exec(
            XRAY_BIN, "run", "-c", XRAY_MAIN_CFG,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**os.environ, "XRAY_LOCATION_ASSET": "/usr/local/share/xray"},
        )
        _start_time = time.time()
        _running    = True
        logger.info(f"🚀 Xray started — PID {_process.pid}")

        stdout_lines: list[str] = []
        stderr_lines: list[str] = []

        async def _collect(stream, bucket):
            try:
                async for line in stream:
                    text = line.decode("utf-8", errors="replace").rstrip()
                    if text:
                        bucket.append(text)
            except Exception:
                pass

        stdout_task = asyncio.create_task(_collect(_process.stdout, stdout_lines))
        stderr_task = asyncio.create_task(_collect(_process.stderr, stderr_lines))

        await asyncio.sleep(3)

        if _process.returncode is not None:
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task), timeout=2.0
                )
            except asyncio.TimeoutError:
                stdout_task.cancel()
                stderr_task.cancel()

            logger.error(f"❌ Xray crashed — exit code: {_process.returncode}")
            logger.error(f"   Binary  : {XRAY_BIN}")
            logger.error(f"   Config  : {XRAY_MAIN_CFG}")
            logger.error(f"   Cert    : {XRAY_CERT_FILE} (exists={Path(XRAY_CERT_FILE).exists()})")
            logger.error(f"   Key     : {XRAY_KEY_FILE} (exists={Path(XRAY_KEY_FILE).exists()})")

            if stdout_lines:
                logger.error("── Xray STDOUT ──────────────────────────────")
                for line in stdout_lines:
                    logger.error(f"  {line}")
            else:
                logger.error("── Xray STDOUT: (empty)")

            if stderr_lines:
                logger.error("── Xray STDERR ──────────────────────────────")
                for line in stderr_lines:
                    logger.error(f"  {line}")
            else:
                logger.error("── Xray STDERR: (empty)")

            try:
                import json
                with open(XRAY_MAIN_CFG) as f:
                    cfg = json.load(f)
                logger.error(f"── Xray CONFIG (inbounds count={len(cfg.get('inbounds', []))}) ──")
                for ib in cfg.get("inbounds", []):
                    logger.error(f"  inbound tag={ib.get('tag')} proto={ib.get('protocol')} "
                                 f"port={ib.get('port')} listen={ib.get('listen')}")
            except Exception as ce:
                logger.error(f"── Could not read config: {ce}")

            logger.error("─────────────────────────────────────────────")
            return False

        asyncio.create_task(_pipe_stdout(_process.stdout, stdout_lines, stdout_task))
        asyncio.create_task(_pipe_stderr(_process.stderr, stderr_lines, stderr_task))

        logger.info("✅ Xray is running")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to start Xray: {e}", exc_info=True)
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
    # Import locally to avoid circular import
    from xray_config import write_xray_config
    
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
                logger.warning(f"⏳ Backoff {backoff}s (attempt #{consecutive})...")
                await asyncio.sleep(backoff)
            ok = await start_xray()
            if ok:
                consecutive = 0
        else:
            consecutive = 0


async def start_monitor() -> None:
    global _monitor_task
    ok = await start_xray()
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


async def _pipe_stdout(stream, already: list[str], task: asyncio.Task) -> None:
    for line in already:
        logger.info(f"[xray] {line}")
    task.cancel()
    try:
        async for line in stream:
            text = line.decode("utf-8", errors="replace").rstrip()
            if text:
                logger.info(f"[xray] {text}")
    except Exception:
        pass


async def _pipe_stderr(stream, already: list[str], task: asyncio.Task) -> None:
    for line in already:
        logger.warning(f"[xray/ERR] {line}")
    task.cancel()
    try:
        async for line in stream:
            text = line.decode("utf-8", errors="replace").rstrip()
            if text:
                logger.warning(f"[xray/ERR] {text}")
    except Exception:
        pass
