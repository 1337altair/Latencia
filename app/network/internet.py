import socket
import psutil


def local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("1.1.1.1", 80))
        return sock.getsockname()[0]
    except Exception:
        return "-"
    finally:
        sock.close()


def active_adapter():
    stats = psutil.net_if_stats()
    addresses = psutil.net_if_addrs()

    for name, state in stats.items():
        if not state.isup:
            continue
        for addr in addresses.get(name, []):
            if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                return name
    return "-"


def network_info():
    return {"local_ip": local_ip(), "adapter": active_adapter()}
