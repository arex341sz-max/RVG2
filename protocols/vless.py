"""protocols/vless.py"""
from urllib.parse import quote
from .base import BaseProtocol

class VLESSProtocol(BaseProtocol):
    display_name = "VLESS"
    icon = "ti-shield-check"
    color = "#3B82F6"
    supports_tls = True
    default_tls = True
    supports_reality = True
    default_stream = "ws"

    stream_modes = {
        "ws": {"label": "WebSocket", "params": []},
        "tcp": {"label": "TCP", "params": []},
    }

    def generate_link(self, uuid, host, port, **k):
        return f"vless://{uuid}@{host}:{port}?security=tls&type=ws&path=/ws#RVG"

    def get_xray_inbound(self, port: int, **kw):
        return {
            "listen": "127.0.0.1",
            "port": port,
            "protocol": "vless",
            "settings": {
                "clients": [{"id": kw.get("uuid", ""), "flow": ""}],
                "decryption": "none"
            },
            "streamSettings": {
                "network": "ws",
                "wsSettings": {"path": "/ws"},
                "security": "tls",
                "tlsSettings": {
                    "serverName": "localhost",
                    "certificates": [
                        {"certificateFile": "/data/certs/cert.pem", "keyFile": "/data/certs/key.pem"}
                    ],
                    "alpn": ["http/1.1"]
                }
            },
            "sniffing": {"enabled": True, "destOverride": ["http", "tls"]}
        }
