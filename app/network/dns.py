import socket
import time


def measure_dns_latency(domain="cloudflare.com"):
    start = time.perf_counter()
    socket.gethostbyname(domain)
    return (time.perf_counter() - start) * 1000
