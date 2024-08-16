import platform
import time
from os import environ
from typing import Callable, Tuple


class Settings:
    """Wrapper for the settings required by the module.

    >>> Settings

    """

    format_key: Callable = None
    os: str = platform.system()
    # Host file that matches FQDN with server IPs hosting a specific domain
    etc_hosts: str = "/etc/hosts"
    host_id: int = 254
    flush_dns: Tuple = ()
    # Unlike Windows and macOS, Ubuntu and Linux Mint do not cache DNS queries at the operating system level by default.
    start: float = None
    router_pass = None


settings = Settings()
settings.format_key = lambda key: key.lower().replace(" ", "_").replace("-", "_")

if settings.os == "Windows":
    etc_hosts: str = r"C:\Windows\System32\drivers\etc\hosts"
    flush_dns: Tuple[str] = ("ipconfig /flushdnscache",)
elif settings.os == "Darwin":
    flush_dns: Tuple[str, str] = (
        "sudo dscacheutil -flushcache",
        "sudo killall -HUP mDNSResponder",
    )
else:
    flush_dns: Tuple[str, str] = (
        "sudo resolvectl flush-caches",  # Ubuntu 22.04 and higher
        "sudo systemd-resolve --flush-caches",  # Ubuntu 17.04 and higher (18.04)
    )
settings.router_pass = environ.get("router_pass") or environ.get("ROUTER_PASS")
settings.start = time.time()
