import os
import time
import requests


def download_test(size=25000000):
    url = f"https://speed.cloudflare.com/__down?bytes={size}"
    start = time.perf_counter()
    received = 0

    with requests.get(url, stream=True, timeout=30, headers={"Cache-Control": "no-cache"}) as response:
        response.raise_for_status()
        for chunk in response.iter_content(256 * 1024):
            if chunk:
                received += len(chunk)

    seconds = time.perf_counter() - start
    if seconds <= 0:
        return 0.0
    return (received * 8 / seconds) / 1000000


def upload_test(size=8000000):
    data = os.urandom(size)
    start = time.perf_counter()
    response = requests.post("https://speed.cloudflare.com/__up", data=data, timeout=30)
    response.raise_for_status()
    seconds = time.perf_counter() - start
    if seconds <= 0:
        return 0.0
    return (size * 8 / seconds) / 1000000
