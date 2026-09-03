import platform
import re
import subprocess


def get_wifi_info():
    if platform.system().lower() != "windows":
        return {}

    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        output = result.stdout

        def value(pattern):
            match = re.search(pattern, output, re.IGNORECASE)
            return match.group(1).strip() if match else None

        return {
            "ssid": value(r"^\s*SSID\s*:\s*(.+)$"),
            "signal": value(r"^\s*Signal\s*:\s*(.+)$"),
            "channel": value(r"^\s*Channel\s*:\s*(.+)$"),
            "receive_rate": value(r"^\s*Receive rate \(Mbps\)\s*:\s*(.+)$"),
            "transmit_rate": value(r"^\s*Transmit rate \(Mbps\)\s*:\s*(.+)$"),
        }
    except Exception:
        return {}
