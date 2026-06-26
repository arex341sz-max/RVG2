"""protocols/vmess.py — VMess بهینه‌شده"""
import json
import base64
from urllib.parse import quote
from config import XRAY_CERT_FILE, XRAY_KEY_FILE
from .base import BaseProtocol


class VMessProtocol(BaseProtocol):
    display_name     = "VMess"
    icon             = "ti-lock"
    color            = "#8B5CF6"
    supports_tls     = True
    default_tls      = True
    supports_reality = False
    default_stream   = "ws"

    stream_modes = {
        "ws": {
            "label": "WebSocket",
            "icon":  "ti-webhook",
            "desc":  "عبور از فایروال — Early Data فعال",
            "params": [
                {"key": "path", "label": "مسیر", "placeholder": "/ws/{uuid}", "default": "/ws"},
                {"key": "host", "label": "Host",  "placeholder": "example.com", "default": ""},
            ],
        },
        "xhttp": {
            "label": "XHTTP",
            "icon":  "ti-arrows-split-2",
            "desc":  "SplitHTTP — سریع‌ترین",
            "params": [
                {"key": "path", "label": "مسیر", "placeholder": "/xhttp", "default": "/xhttp"},
                {"key": "host", "label": "Host",  "placeholder": "example.com", "default": ""},
                {"key": "mode", "label": "Mode",  "type": "select",
                 "options": ["auto", "packet-up"], "default": "auto"},
            ],
        },
        "grpc": {
            "label": "gRPC",
            "icon":  "ti-binary-tree-2",
            "desc":  "HTTP/2 multiplexing",
            "params": [
                {"key": "serviceName", "label": "Service Name", "placeholder": "grpc", "default": "grpc"},
            ],
        },
        "httpupgrade": {
            "label": "HTTPUpgrade",
            "icon":  "ti-arrow-up-circle",
            "desc":  "ارتقای HTTP",
            "params": [
                {"key": "path", "label": "مسیر", "placeholder": "/upgrade", "default": "/upgrade"},
                {"key": "host", "label": "Host",  "placeholder": "example.com", "default": ""},
            ],
        },
        "tcp": {"label": "TCP", "icon": "ti-arrows-transfer-down", "desc": "مستقیم", "params": []},
    }

    def generate_link(self, uuid: str, host: str, port: int,
                      stream: str = "ws", tls: bool = True,
                      sni: str = "", fingerprint: str = "chrome",
                      alpn: str = "http/1.1", remark: str = "RVG", **sp) -> str:
        ws_path = sp.get("path", "/ws")
        if stream == "ws" and ws_path in ("/ws", "") and uuid:
            ws_path = f"/ws/{uuid}"

        _alpn = "h3" if stream == "xhttp" else alpn
        vmess = {
            "v": "2", "ps": remark, "add": host, "port": str(port),
            "id": uuid, "aid": "0", "scy": "auto",
            "net": stream, "type": "none",
            "host": sp.get("host", "") or host,
            "path": ws_path if stream == "ws" else (sp.get("path", "") or "/"),
            "tls": "tls" if tls else "none",
            "sni": sni or host, "alpn": _alpn, "fp": fingerprint,
        }
        if stream == "grpc":
            vmess["path"] = sp.get("serviceName", "grpc")
            vmess["type"] = "gun"
        return f"vmess://{base64.b64encode(json.dumps(vmess, ensure_ascii=False).encode()).decode()}"

    def get_xray_inbound(self, port: int, **kw) -> dict:
        uuid   = kw.pop("uuid", "")
        stream = kw.pop("stream", "ws")
        tls    = kw.pop("tls", True)
        return {
            "listen":   "0.0.0.0",
            "port":     port,
            "protocol": "vmess",
            "settings": {"clients": [{"id": uuid, "alterId": 0, "security": "auto"}]},
            "streamSettings": self._stream(stream, tls, uuid=uuid, **kw),
            "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"]},
        }

    def _stream(self, stream: str, tls: bool, **kw) -> dict:
        uuid = kw.get("uuid", "")
        ss = {"network": stream}
        if stream == "tcp":
            ss["tcpSettings"] = {"header": {"type": "none"}}
        elif stream == "ws":
            raw  = kw.get("path", "/ws")
            path = f"/ws/{uuid}" if raw in ("/ws", "") and uuid else raw
            ss["wsSettings"] = {
                "path": path,
                "headers":             {"Host": kw.get("host", "")} if kw.get("host") else {},
                "maxEarlyData":        1024,
                "earlyDataHeaderName": "Sec-WebSocket-Protocol",
            }
        elif stream == "xhttp":
            raw  = kw.get("path", "/xhttp")
            path = f"/xhttp/{uuid}" if raw in ("/xhttp", "") and uuid else raw
            ss["xhttpSettings"] = {
                "path": path, "host": kw.get("host", ""),
                "mode": kw.get("mode", "auto"),
                "maxUploadSize": 100 * 1024 * 1024,
                "maxConcurrentUploads": 10,
            }
        elif stream == "grpc":
            ss["grpcSettings"] = {
                "serviceName": kw.get("serviceName", "grpc"),
                "multiMode":   False,
                "idle_timeout": 60,
            }
        elif stream == "httpupgrade":
            raw  = kw.get("path", "/upgrade")
            path = f"/upgrade/{uuid}" if raw in ("/upgrade", "") and uuid else raw
            ss["httpUpgradeSettings"] = {"path": path, "host": kw.get("host", "")}
        if tls:
            ss["security"] = "tls"
            ss["tlsSettings"] = self._build_tls_settings(
                sni=kw.get("sni", "") or kw.get("host", ""),
                alpn=["h2", "http/1.1"],
            )
        return ss
