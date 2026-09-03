import platform
import re
import socket
import subprocess
import time

from app.network.ping import ping_once


def default_gateway():
    if platform.system().lower() != "windows":
        return None

    try:
        flags = subprocess.CREATE_NO_WINDOW
        result = subprocess.run(
            ["route", "print", "-4", "0.0.0.0"],
            capture_output=True,
            text=True,
            timeout=4,
            creationflags=flags
        )

        for line in result.stdout.splitlines():
            match = re.match(
                r"^\s*0\.0\.0\.0\s+0\.0\.0\.0\s+(\d+\.\d+\.\d+\.\d+)\s+\d+\.\d+\.\d+\.\d+\s+\d+\s*$",
                line
            )
            if match:
                return match.group(1)
    except Exception:
        return None

    return None


def gateway_latency():
    gateway = default_gateway()
    if not gateway:
        return {"gateway": None, "latency": None}

    return {"gateway": gateway, "latency": ping_once(gateway)}


def dns_latency(host="cloudflare.com"):
    start = time.perf_counter()
    try:
        socket.getaddrinfo(host, 443)
        return (time.perf_counter() - start) * 1000
    except Exception:
        return None


def internet_check(host="1.1.1.1", port=443):
    try:
        start = time.perf_counter()
        connection = socket.create_connection((host, port), timeout=3)
        elapsed = (time.perf_counter() - start) * 1000
        connection.close()
        return {"online": True, "latency": elapsed}
    except Exception:
        return {"online": False, "latency": None}
