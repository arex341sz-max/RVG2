"""
protocols/siz10a.py — پروتکل SIZ10A
پروتکل اختصاصی RVG با ترکیب بهترین ویژگی‌های VLESS + XHTTP + Reality
طراحی‌شده برای:
  - کمترین latency ممکن (پینگ نزدیک به صفر overhead)
  - بیشترین throughput (pipeline کامل، بدون buffering غیرضروری)
  - قوی‌ترین camouflage (XHTTP + Reality fingerprint)
  - مقاومت در برابر DPI عمیق
  - مالتی‌پلکس خودکار (h2 + h3)
"""
from urllib.parse import quote
from config import XRAY_CERT_FILE, XRAY_KEY_FILE
from .base import BaseProtocol


class SIZ10AProtocol(BaseProtocol):
    display_name = "SIZ10A"
    icon         = "ti-rocket"
    color        = "#6366F1"   # indigo — متمایز از بقیه
    supports_tls     = True
    default_tls      = True
    supports_reality = True
    default_stream   = "xhttp"

    # ── Stream modes ──────────────────────────────────────────────────────────
    stream_modes = {
        # ── حالت پیش‌فرض و سریع‌ترین: XHTTP + Reality ──────────────────────
        "xhttp": {
            "label": "XHTTP Ultra",
            "icon":  "ti-rocket",
            "desc":  "SplitHTTP + Reality — سریع‌ترین + قوی‌ترین camouflage",
            "params": [
                {"key": "path",       "label": "مسیر",          "placeholder": "/siz",        "default": "/siz"},
                {"key": "host",       "label": "Host",           "placeholder": "example.com", "default": ""},
                {"key": "mode",       "label": "XHTTP Mode",     "type": "select",
                 "options": ["auto", "packet-up", "stream-up"],  "default": "auto"},
                {"key": "maxUploadSize",   "label": "Max Upload (MB)",    "placeholder": "100",  "default": "100"},
                {"key": "maxConcurrentUploads", "label": "Concurrent Uploads", "placeholder": "10", "default": "10"},
            ],
        },
        # ── WebSocket با بهینه‌سازی کامل ────────────────────────────────────
        "ws": {
            "label": "WS Turbo",
            "icon":  "ti-bolt",
            "desc":  "WebSocket بهینه — کمترین overhead، بهترین عبور",
            "params": [
                {"key": "path",  "label": "مسیر", "placeholder": "/siz", "default": "/siz"},
                {"key": "host",  "label": "Host",  "placeholder": "example.com", "default": ""},
                {"key": "earlyDataHeaderName", "label": "Early Data Header",
                 "placeholder": "Sec-WebSocket-Protocol", "default": "Sec-WebSocket-Protocol"},
            ],
        },
        # ── gRPC — بهترین برای شبکه‌های ناپایدار ────────────────────────────
        "grpc": {
            "label": "gRPC Mux",
            "icon":  "ti-binary-tree-2",
            "desc":  "HTTP/2 multiplexing — بهترین برای latency بالا",
            "params": [
                {"key": "serviceName", "label": "Service Name", "placeholder": "siz",  "default": "siz"},
                {"key": "multiMode",   "label": "Multi Mode",   "type": "bool",         "default": True},
                {"key": "idle_timeout","label": "Idle Timeout (s)", "placeholder": "60","default": "60"},
                {"key": "health_check_timeout", "label": "Health Check (s)", "placeholder": "20", "default": "20"},
            ],
        },
        # ── HTTPUpgrade — سازگاری بالا ───────────────────────────────────────
        "httpupgrade": {
            "label": "HTTP Upgrade",
            "icon":  "ti-arrow-up-circle",
            "desc":  "ارتقای HTTP — سازگاری بالا با CDN",
            "params": [
                {"key": "path", "label": "مسیر", "placeholder": "/siz", "default": "/siz"},
                {"key": "host", "label": "Host",  "placeholder": "example.com", "default": ""},
            ],
        },
        # ── TCP خالص — سریع‌ترین روی شبکه مستقیم ───────────────────────────
        "tcp": {
            "label": "TCP Raw",
            "icon":  "ti-arrows-transfer-down",
            "desc":  "مستقیم‌ترین مسیر — بهترین برای low-latency gaming",
            "params": [],
        },
    }

    # ── Link generator ────────────────────────────────────────────────────────
    def generate_link(
        self,
        uuid: str = "",
        host: str = "",
        port: int = 443,
        stream: str = "xhttp",
        tls: bool = True,
        sni: str = "",
        fingerprint: str = "chrome",
        alpn: str = "h3",
        remark: str = "SIZ10A",
        reality: bool = False,
        reality_pbk: str = "",
        reality_sid: str = "",
        reality_sni: str = "",
        reality_fingerprint: str = "chrome",
        **sp,
    ) -> str:
        # SIZ10A از VLESS به عنوان پروتکل پایه استفاده میکنه (بهترین encryption=none با TLS)
        p = {"encryption": "none"}

        if reality:
            p.update(
                security="reality",
                pbk=reality_pbk,
                sid=reality_sid,
                sni=reality_sni or host,
                fp=reality_fingerprint or fingerprint,
                type=stream,
            )
        elif tls:
            # SIZ10A پیش‌فرض: h3 (QUIC) برای xhttp، h2 برای بقیه
            _alpn = alpn if alpn else ("h3" if stream == "xhttp" else "h2,http/1.1")
            p.update(security="tls", sni=sni or host, fp=fingerprint, alpn=_alpn, type=stream)
        else:
            p.update(security="none", type=stream)

        mode = self.stream_modes.get(stream, {})
        for pdef in mode.get("params", []):
            key = pdef["key"]
            val = sp.get(key, pdef.get("default", ""))
            if val not in (None, "", False):
                p[key] = "true" if isinstance(val, bool) and val else str(val)

        # path fix: اگه ws یا xhttp و path پیش‌فرضه، uuid اضافه کن
        if stream in ("ws", "xhttp", "httpupgrade"):
            cur = p.get("path", "/siz")
            if cur in ("/siz", "/ws", "") and uuid:
                p["path"] = f"/{stream[:3]}/{uuid}"
            if not sp.get("host"):
                p["host"] = host

        # early data برای WS — کاهش RTT اولیه
        if stream == "ws":
            p.setdefault("earlyDataHeaderName", "Sec-WebSocket-Protocol")

        q = "&".join(f"{k}={quote(str(v))}" for k, v in p.items())
        return f"vless://{uuid}@{host}:{port}?{q}#{quote(remark or 'SIZ10A')}"

    # ── Xray inbound ──────────────────────────────────────────────────────────
    def get_xray_inbound(self, port: int, **kw) -> dict:
        uuid   = kw.get("uuid", "")
        stream = kw.pop("stream", "xhttp")
        tls    = kw.pop("tls", True)
        return {
            "listen":   "0.0.0.0",
            "port":     port,
            "protocol": "vless",
            "settings": {
                "clients": [{
                    "id":   uuid,
                    "flow": "xtls-rprx-vision" if stream == "tcp" and not kw.get("reality") else "",
                }],
                "decryption": "none",
            },
            "streamSettings": self._build_stream(stream, tls, uuid=uuid, **kw),
            "sniffing": {
                "enabled":      True,
                "destOverride": ["http", "tls", "quic"],
                "routeOnly":    False,
                # metadataOnly=False برای sniff کامل — کمک به routing بهتر
            },
        }

    def _build_stream(self, stream: str, tls: bool, **kw) -> dict:
        uuid = kw.get("uuid", "")
        ss: dict = {"network": stream}

        if stream == "tcp":
            ss["tcpSettings"] = {"header": {"type": "none"}}

        elif stream == "ws":
            raw  = kw.get("path", "/siz")
            path = f"/ws/{uuid}" if raw in ("/siz", "/ws", "") and uuid else raw
            ss["wsSettings"] = {
                "path": path,
                "headers": {"Host": kw.get("host", "")} if kw.get("host") else {},
                # early data: کاهش RTT اولیه از 2 به 1
                "maxEarlyData":        1024,
                "earlyDataHeaderName": kw.get("earlyDataHeaderName", "Sec-WebSocket-Protocol"),
                # بدون compression — overhead کمتر
                "acceptProxyProtocol": False,
            }

        elif stream == "grpc":
            ss["grpcSettings"] = {
                "serviceName":        kw.get("serviceName", "siz"),
                "multiMode":          bool(kw.get("multiMode", True)),
                "idle_timeout":       int(kw.get("idle_timeout", 60)),
                "health_check_timeout": int(kw.get("health_check_timeout", 20)),
                # permitWithoutStream: keepalive بدون stream فعال
                "permit_without_stream": True,
                "initial_windows_size":  65536,
            }

        elif stream == "httpupgrade":
            raw  = kw.get("path", "/siz")
            path = f"/up/{uuid}" if raw in ("/siz", "/up", "") and uuid else raw
            ss["httpUpgradeSettings"] = {
                "path": path,
                "host": kw.get("host", ""),
            }

        elif stream == "xhttp":
            raw  = kw.get("path", "/siz")
            path = f"/xh/{uuid}" if raw in ("/siz", "/xh", "") and uuid else raw
            ss["xhttpSettings"] = {
                "path": path,
                "host": kw.get("host", ""),
                "mode": kw.get("mode", "auto"),
                # حداکثر اندازه هر upload chunk — 100MB
                "maxUploadSize":        int(kw.get("maxUploadSize", 100)) * 1024 * 1024,
                # concurrent upload streams — throughput بیشتر
                "maxConcurrentUploads": int(kw.get("maxConcurrentUploads", 10)),
                # noSSEHeader: overhead کمتر
                "noSSEHeader": False,
                # scMaxEachPostBytes: حداکثر بایت هر POST
                "scMaxEachPostBytes": 1 * 1024 * 1024,
                # scMinPostsIntervalMs: حداقل فاصله بین POSTها
                "scMinPostsIntervalMs": 30,
                # xPaddingBytes: padding برای bypass DPI
                "xPaddingBytes": "100-1000",
            }

        # ── TLS / Reality ────────────────────────────────────────────────────
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
            _alpn = ["h3", "h2", "http/1.1"] if stream == "xhttp" else ["h2", "http/1.1"]
            ss["security"] = "tls"
            ss["tlsSettings"] = {
                "serverName":   kw.get("sni", "") or "",
                "minVersion":   "1.2",
                "certificates": [{
                    "certificateFile": XRAY_CERT_FILE,
                    "keyFile":         XRAY_KEY_FILE,
                }],
                "alpn": _alpn,
                # sessionTicket: TLS session reuse — کاهش handshake overhead
                "enableSessionResumption": True,
            }
        return ss
