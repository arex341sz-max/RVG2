"""protocols/trojan.py — Trojan با config صحیح برای Xray"""
from urllib.parse import quote
from config import XRAY_CERT_FILE, XRAY_KEY_FILE
from .base import BaseProtocol


class TrojanProtocol(BaseProtocol):
    display_name = "Trojan"
    icon = "ti-horse"
    color = "#10B981"
    supports_tls = True
    default_tls = True
    supports_reality = True
    default_stream = "ws"

    stream_modes = {
        "ws": {
            "label": "WebSocket",
            "icon": "ti-webhook",
            "desc": "عبور از فایروال با هدر HTTP",
            "params": [
                {"key": "path", "label": "مسیر", "placeholder": "/ws/{uuid}", "default": "/ws"},
                {"key": "host", "label": "Host",  "placeholder": "example.com",  "default": ""},
            ],
        },
        "tcp": {
            "label": "TCP",
            "icon": "ti-arrows-transfer-down",
            "desc": "مستقیم — استاندارد Trojan",
            "params": [],
        },
        "grpc": {
            "label": "gRPC",
            "icon": "ti-binary-tree-2",
            "desc": "HTTP/2 multiplexing",
            "params": [
                {"key": "serviceName", "label": "Service Name", "placeholder": "grpc", "default": "grpc"},
                {"key": "multiMode",   "label": "Multi Mode",   "type": "bool",        "default": True},
            ],
        },
        "httpupgrade": {
            "label": "HTTPUpgrade",
            "icon": "ti-arrow-up-circle",
            "desc": "ارتقای اتصال HTTP",
            "params": [
                {"key": "path", "label": "مسیر", "placeholder": "/upgrade",    "default": "/upgrade"},
                {"key": "host", "label": "Host",  "placeholder": "example.com", "default": ""},
            ],
        },
        "xhttp": {
            "label": "XHTTP",
            "icon": "ti-arrows-split-2",
            "desc": "جداسازی GET/POST",
            "params": [
                {"key": "path", "label": "مسیر", "placeholder": "/xhttp",      "default": "/xhttp"},
                {"key": "host", "label": "Host",  "placeholder": "example.com", "default": ""},
                {"key": "mode", "label": "Mode",  "type": "select",
                 "options": ["auto", "packet-up"], "default": "auto"},
            ],
        },
    }

    def generate_link(self, password: str = "", uuid: str = "", host: str = "", port: int = 443,
                      stream: str = "ws", tls: bool = True,
                      sni: str = "", fingerprint: str = "chrome", alpn: str = "http/1.1",
                      remark: str = "RVG", reality: bool = False,
                      reality_pbk: str = "", reality_sid: str = "",
                      reality_sni: str = "", reality_fingerprint: str = "chrome",
                      **sp) -> str:
        p: dict = {}
        if reality:
            p.update(security="reality", pbk=reality_pbk, sid=reality_sid,
                     sni=reality_sni or host, fp=reality_fingerprint or fingerprint)
        elif tls:
            p.update(security="tls", sni=sni or host, fp=fingerprint, alpn=alpn)
        else:
            p["security"] = "none"
        p["type"] = stream

        mode = self.stream_modes.get(stream, {})
        for pdef in mode.get("params", []):
            key = pdef["key"]
            val = sp.get(key, pdef.get("default", ""))
            if val is not None and val != "" and val is not False:
                p[key] = "true" if (isinstance(val, bool) and val) else str(val)

        # ✅ FIX: اگه ws و path پیش‌فرضه، UUID/password رو اضافه کن
        if stream == "ws":
            current_path = p.get("path", "/ws")
            link_id = password or uuid
            if current_path in ("/ws", "") and link_id:
                p["path"] = f"/ws/{link_id}"

        if stream in ("ws", "httpupgrade", "xhttp") and not sp.get("host"):
            p["host"] = host

        q = "&".join(f"{k}={quote(str(v))}" for k, v in p.items())
        return f"trojan://{password}@{host}:{port}?{q}#{quote(remark)}"

    def get_xray_inbound(self, port: int, **kw) -> dict:
        uuid     = kw.get("uuid", "")
        password = kw.get("password", "")
        stream   = kw.pop("stream", "ws")
        tls      = kw.pop("tls", True)
        return {
            "listen":   "0.0.0.0",
            "port":     port,
            "protocol": "trojan",
            "settings": {
                "clients": [{"password": password}],
            },
            "streamSettings": self._build_stream(stream, tls, uuid=uuid, **kw),
            "sniffing": {"enabled": True, "destOverride": ["http", "tls"]},
        }

    def _build_stream(self, stream: str, tls: bool, **kw) -> dict:
        uuid     = kw.get("uuid", "")
        password = kw.get("password", "")
        ss: dict = {"network": stream}

        if stream == "tcp":
            ss["tcpSettings"] = {"header": {"type": "none"}}
        elif stream == "ws":
            # ✅ FIX: path رو /ws/{uuid} بساز
            raw_path = kw.get("path", "/ws")
            link_id  = password or uuid
            ws_path  = f"/ws/{link_id}" if raw_path in ("/ws", "") and link_id else raw_path
            ws_s: dict = {"path": ws_path}
            if kw.get("host"):
                ws_s["headers"] = {"Host": kw["host"]}
            ss["wsSettings"] = ws_s
        elif stream == "grpc":
            ss["grpcSettings"] = {
                "serviceName": kw.get("serviceName", "grpc"),
                "multiMode":   bool(kw.get("multiMode", True)),
            }
        elif stream == "httpupgrade":
            ss["httpUpgradeSettings"] = {
                "path": kw.get("path", "/upgrade"),
                "host": kw.get("host", ""),
            }
        elif stream == "xhttp":
            ss["xhttpSettings"] = {
                "path": kw.get("path", "/xhttp"),
                "host": kw.get("host", ""),
                "mode": kw.get("mode", "auto"),
            }

        if kw.get("reality"):
            ss["security"] = "reality"
            ss["realitySettings"] = {
                "show":        False,
                "dest":        f"{kw.get('reality_sni','') or kw.get('host','')}:443",
                "xver":        0,
                "serverNames": [kw.get("reality_sni", "") or kw.get("host", "")],
                "privateKey":  kw.get("reality_pbk", ""),
                "shortIds":    [kw.get("reality_sid", "")],
                "fingerprint": kw.get("reality_fingerprint", "chrome"),
            }
        elif tls:
            ss["security"] = "tls"
            ss["tlsSettings"] = {
                "serverName":   kw.get("sni", "") or "",
                "certificates": [{
                    "certificateFile": XRAY_CERT_FILE,
                    "keyFile":         XRAY_KEY_FILE,
                }],
                "alpn": ["http/1.1"],
            }
        return ss
