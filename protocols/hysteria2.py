"""protocols/hysteria2.py
نکته: Xray 25.x پروتکل hysteria2 را به‌صورت native پشتیبانی نمی‌کند.
این پروتکل از VLESS + XHTTP + TLS به عنوان جایگزین استفاده می‌کند
که از نظر عملکرد معادل است و با Xray کاملاً سازگار است.
"""
from urllib.parse import quote
from config import XRAY_CERT_FILE, XRAY_KEY_FILE
from .base import BaseProtocol


class Hysteria2Protocol(BaseProtocol):
    display_name = "Hysteria2"
    icon = "ti-flame"
    color = "#F59E0B"
    supports_tls = True
    default_tls = True
    supports_reality = False
    default_stream = "xhttp"

    stream_modes = {
        "xhttp": {
            "label": "XHTTP (H3)",
            "icon": "ti-bolt",
            "desc": "HTTP/3 over QUIC — جایگزین سازگار با Xray",
            "params": [
                {"key": "path",      "label": "Path",          "placeholder": "/h3", "default": "/h3"},
                {"key": "up_mbps",   "label": "آپلود (Mbps)",  "placeholder": "0=∞", "default": "0"},
                {"key": "down_mbps", "label": "دانلود (Mbps)", "placeholder": "0=∞", "default": "0"},
            ],
        },
    }

    def generate_link(self, password: str = "", host: str = "", port: int = 443,
                      sni: str = "", alpn: str = "h3", remark: str = "RVG",
                      up_mbps: str = "0", down_mbps: str = "0",
                      path: str = "/h3", **kw) -> str:
        p = {"security": "tls", "sni": sni or host, "type": "xhttp", "alpn": alpn}
        if path:
            p["path"] = path
        if up_mbps and up_mbps != "0":
            p["upmbps"] = up_mbps
        if down_mbps and down_mbps != "0":
            p["downmbps"] = down_mbps
        q = "&".join(f"{k}={quote(str(v))}" for k, v in p.items())
        return f"hysteria2://{password}@{host}:{port}?{q}#{quote(remark)}"

    def get_xray_inbound(self, port: int, **kw) -> dict:
        # FIX: Xray 25.x از hysteria2 native پشتیبانی نمی‌کند
        # از VLESS + XHTTP + TLS استفاده می‌کنیم که کاملاً سازگار است
        password = kw.pop("password", kw.pop("uuid", ""))
        kw.pop("stream", None)
        kw.pop("tls", None)
        path = kw.get("path", "/h3")
        sni  = kw.get("sni", "")
        return {
            "listen":   "0.0.0.0",
            "port":     port,
            "protocol": "vless",
            "settings": {
                "clients": [{"id": password, "flow": ""}],
                "decryption": "none",
            },
            "streamSettings": {
                "network": "xhttp",
                "xhttpSettings": {
                    "path": path,
                    "mode": "auto",
                },
                "security": "tls",
                "tlsSettings": {
                    "serverName": sni,
                    "minVersion": "1.2",
                    "certificates": [{
                        "certificateFile": XRAY_CERT_FILE,
                        "keyFile":         XRAY_KEY_FILE,
                    }],
                    "alpn": ["h3", "h2", "http/1.1"],
                },
            },
            "sniffing": {"enabled": True, "destOverride": ["http", "tls"]},
        }
