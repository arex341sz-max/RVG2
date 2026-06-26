"""config.py — تمام تنظیمات از environment variables"""
import os
import secrets

PORT          = int(os.environ.get("PORT", 8000))
SECRET_KEY    = os.environ.get("SECRET_KEY", secrets.token_urlsafe(32))
ADMIN_PW      = os.environ.get("ADMIN_PASSWORD", "123456")
PUBLIC_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost")

DATA_DIR        = os.environ.get("DATA_DIR", "/data")
XRAY_CONFIG_DIR = os.environ.get("XRAY_CONFIG_DIR", "/data/xray-configs")
XRAY_BIN        = os.environ.get("XRAY_BIN", "/usr/local/bin/xray")
XRAY_MAIN_CFG   = os.environ.get("XRAY_MAIN_CFG", "/data/xray-main.json")

XRAY_CERT_DIR  = os.environ.get("XRAY_CERT_DIR", "/data/certs")
XRAY_CERT_FILE = os.path.join(XRAY_CERT_DIR, "cert.pem")
XRAY_KEY_FILE  = os.path.join(XRAY_CERT_DIR, "key.pem")

XRAY_PORT_BASE = int(os.environ.get("XRAY_PORT_BASE", 10000))
XRAY_PORT_MAX  = int(os.environ.get("XRAY_PORT_MAX",  19999))

SESSION_TTL = 60 * 60 * 24 * 7

# ── Performance Tuning ────────────────────────────────────────────────────────
# بافر relay — 512KB برای throughput بیشتر
RELAY_BUF        = int(os.environ.get("RELAY_BUF",      512 * 1024))
# حداکثر اندازه پاکت WS دریافتی
WS_MAX_SIZE      = int(os.environ.get("WS_MAX_SIZE",    16 * 1024 * 1024))  # 16MB
# timeout اتصال اولیه
CONNECT_TIMEOUT  = float(os.environ.get("CONNECT_TIMEOUT", 8.0))
# timeout دریافت اولین پاکت
HANDSHAKE_TIMEOUT= float(os.environ.get("HANDSHAKE_TIMEOUT", 12.0))
# drain threshold — فقط وقتی buffer از این بیشتر شد drain کن
DRAIN_THRESHOLD  = int(os.environ.get("DRAIN_THRESHOLD", 256 * 1024))
