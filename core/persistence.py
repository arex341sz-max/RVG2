"""core/persistence.py — ذخیره و بازیابی state از فایل JSON"""
import asyncio
import json
import logging
from pathlib import Path

import aiofiles

from config import DATA_DIR
from state  import LINKS, SUBS, AUTH, LINKS_LOCK, SUBS_LOCK

logger    = logging.getLogger("RVG.persistence")
DATA_FILE = Path(DATA_DIR) / "rvg_state.json"
_SAVE_LOCK = asyncio.Lock()


async def load_state() -> None:
    try:
        Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            return
        async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = await f.read()
        data = json.loads(raw)
        LINKS.update(data.get("links", {}))
        SUBS.update(data.get("subs",  {}))
        if "password_hash" in data:
            AUTH["password_hash"] = data["password_hash"]
        logger.info(f"✅ State loaded — {len(LINKS)} links, {len(SUBS)} subs")
    except Exception as e:
        logger.warning(f"Could not load state: {e}")


async def save_state() -> None:
    async with _SAVE_LOCK:
        try:
            Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
            from datetime import datetime
            data = {
                "links":         dict(LINKS),
                "subs":          dict(SUBS),
                "password_hash": AUTH.get("password_hash", ""),
                "saved_at":      datetime.now().isoformat(),
            }
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.warning(f"Could not save state: {e}")
