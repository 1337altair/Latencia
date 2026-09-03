from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.i18n.language import t
from app.network.ping import ping_once


class MonitorThread(QThread):
    changed = Signal(float)
    timeout = Signal()

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            value = ping_once()
            if value is None:
                self.timeout.emit()
            else:
                self.changed.emit(value)
            self.msleep(1000)

    def stop(self):
        self.running = False
        self.wait(1500)


class MonitorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None

        page = QVBoxLayout(self)
        page.setContentsMargins(30, 28, 30, 28)
        page.setSpacing(18)

        self.title = QLabel()
        self.title.setObjectName("PageTitle")
        self.subtitle = QLabel()
        self.subtitle.setObjectName("PageSubtitle")
        page.addWidget(self.title)
        page.addWidget(self.subtitle)

        panel = QFrame()
        panel.setObjectName("Panel")
        box = QVBoxLayout(panel)
        box.setContentsMargins(20, 18, 20, 18)

        self.current_title = QLabel()
        self.current_title.setObjectName("SmallTitle")
        self.value = QLabel("-- ms")
        self.value.setObjectName("BigValue")
        self.state = QLabel()
        self.state.setObjectName("Muted")

        buttons = QHBoxLayout()
        self.start_btn = QPushButton()
        self.start_btn.setObjectName("Primary")
        self.start_btn.clicked.connect(self.start_monitoring)
        self.stop_btn = QPushButton()
        self.stop_btn.clicked.connect(self.stop_monitoring)
        self.stop_btn.setEnabled(False)
        buttons.addWidget(self.start_btn)
        buttons.addWidget(self.stop_btn)
        buttons.addStretch()

        box.addWidget(self.current_title)
        box.addWidget(self.value)
        box.addWidget(self.state)
        box.addSpacing(12)
        box.addLayout(buttons)
        page.addWidget(panel)
        page.addStretch()
        self.retranslate()

    def start_monitoring(self):
        if self.worker and self.worker.isRunning():
            return
        self.worker = MonitorThread()
        self.worker.changed.connect(self.update_value)
        self.worker.timeout.connect(self.show_timeout)
        self.worker.start()
        self.state.setText(t("monitoring"))
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_monitoring(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
        self.state.setText(t("monitor_stopped"))
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def update_value(self, value):
        self.value.setText(f"{value:.1f} ms")

    def show_timeout(self):
        self.value.setText(t("timeout"))

    def retranslate(self):
        self.title.setText(t("monitor_title"))
        self.subtitle.setText(t("monitor_sub"))
        self.current_title.setText(t("current_latency"))
        self.start_btn.setText(t("start"))
        self.stop_btn.setText(t("stop"))
        if not self.worker or not self.worker.isRunning():
            self.state.setText(t("monitor_stopped"))
