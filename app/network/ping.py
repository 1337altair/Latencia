import platform
import re
import statistics
import subprocess


def ping_once(host="1.1.1.1"):
    windows = platform.system().lower() == "windows"
    command = ["ping", "-n" if windows else "-c", "1", "-w" if windows else "-W", "1200" if windows else "2", host]

    try:
        flags = subprocess.CREATE_NO_WINDOW if windows else 0
        result = subprocess.run(command, capture_output=True, text=True, timeout=4, creationflags=flags)
        output = result.stdout + result.stderr
        found = re.findall(r"(?:time[=<]|tempo[=<])\s*(\d+(?:[.,]\d+)?)\s*ms", output, re.I)
        if not found:
            return None
        return float(found[-1].replace(",", "."))
    except Exception:
        return None


def ping_test(host="1.1.1.1", count=10):
    values = []
    for _ in range(count):
        value = ping_once(host)
        if value is not None:
            values.append(value)

    if not values:
        raise RuntimeError("No ping replies")

    loss = ((count - len(values)) / count) * 100
    diffs = []
    for i in range(1, len(values)):
        diffs.append(abs(values[i] - values[i - 1]))

    return {
        "ping": statistics.mean(values),
        "jitter": statistics.mean(diffs) if diffs else 0.0,
        "packet_loss": loss,
        "min": min(values),
        "max": max(values)
    }
