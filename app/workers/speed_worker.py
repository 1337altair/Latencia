from PySide6.QtCore import QThread, Signal


class SpeedWorker(QThread):
    completed = Signal(dict)

    def run(self):
        self.completed.emit({"download": None, "upload": None})
