"""protocols/base.py — کلاس پایه برای همه پروتکل‌ها"""
from abc import ABC, abstractmethod
from config import XRAY_CERT_FILE, XRAY_KEY_FILE


class BaseProtocol(ABC):
    display_name: str = ""
    icon: str = ""
    color: str = "#3B82F6"
    supports_tls: bool = True
    default_tls: bool = True
    supports_reality: bool = False
    default_stream: str = "tcp"
    stream_modes: dict = {}

    @abstractmethod
    def generate_link(self, **kwargs) -> str:
        """تولید لینک کانفیگ (vless://, trojan://, ...)"""

    @abstractmethod
    def get_xray_inbound(self, port: int, **kwargs) -> dict:
        """تولید بلاک inbound برای Xray JSON config"""

    def _build_tls_settings(self, sni: str, alpn: list[str] | None = None) -> dict:
        # ✅ مسیر cert از config مرکزی — نه hardcode
        return {
            "serverName": sni,
            "certificates": [
                {"certificateFile": XRAY_CERT_FILE,
                 "keyFile":         XRAY_KEY_FILE}
            ],
            "alpn": alpn or ["http/1.1"],
        }

    def _build_reality_settings(self, sni: str, pbk: str, sid: str, fp: str) -> dict:
        return {
            "show": False,
            "dest": f"{sni}:443",
            "xver": 0,
            "serverNames": [sni],
            "privateKey": pbk,
            "shortIds": [sid],
            "fingerprint": fp,
        }
