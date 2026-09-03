from PySide6.QtCore import QThread, Signal
from app.network.ping import ping_once


class NetworkMonitorWorker(QThread):
    updated = Signal(float)

    def __init__(self, host="1.1.1.1"):
        super().__init__()
        self.host = host
        self.running = True

    def run(self):
        while self.running:
            value = ping_once(self.host)
            if value is not None:
                self.updated.emit(value)
            self.msleep(1000)

    def stop(self):
        self.running = False
