from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.database.database import save_test
from app.diagnostics.scoring import score_connection
from app.i18n.language import t
from app.network.internet import network_info
from app.network.ping import ping_test
from app.network.speed import download_test, upload_test


class TestWorker(QThread):
    stage = Signal(str)
    done = Signal(dict)
    failed = Signal(str)

    def run(self):
        try:
            self.stage.emit("testing_ping")
            p = ping_test(count=10)

            self.stage.emit("testing_download")
            down = download_test()

            self.stage.emit("testing_upload")
            up = upload_test()

            net = network_info()
            result = {
                "download": down,
                "upload": up,
                "ping": p["ping"],
                "jitter": p["jitter"],
                "packet_loss": p["packet_loss"],
                "local_ip": net["local_ip"],
                "adapter": net["adapter"]
            }
            result["score"] = score_connection(result["ping"], result["jitter"], result["packet_loss"])
            save_test(result)
            self.done.emit(result)
        except Exception as e:
            self.failed.emit(str(e))


class Metric(QFrame):
    def __init__(self, key, value="--", unit=""):
        super().__init__()
        self.key = key
        self.setObjectName("Metric")
        box = QVBoxLayout(self)
        box.setContentsMargins(16, 14, 16, 14)
        box.setSpacing(3)
        self.name = QLabel()
        self.name.setObjectName("MetricName")
        self.value = QLabel(value)
        self.value.setObjectName("MetricValue")
        self.unit = QLabel(unit)
        self.unit.setObjectName("MetricUnit")
        box.addWidget(self.name)
        box.addWidget(self.value)
        box.addWidget(self.unit)
        self.retranslate()

    def set_value(self, value):
        self.value.setText(str(value))

    def retranslate(self):
        self.name.setText(t(self.key))


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.last_grade = None

        page = QVBoxLayout(self)
        page.setContentsMargins(30, 28, 30, 28)
        page.setSpacing(18)

        top = QHBoxLayout()
        titles = QVBoxLayout()
        self.title = QLabel()
        self.title.setObjectName("PageTitle")
        self.subtitle = QLabel()
        self.subtitle.setObjectName("PageSubtitle")
        titles.addWidget(self.title)
        titles.addWidget(self.subtitle)

        self.state = QLabel()
        self.state.setObjectName("State")
        top.addLayout(titles)
        top.addStretch()
        top.addWidget(self.state)
        page.addLayout(top)

        main = QFrame()
        main.setObjectName("Panel")
        main_box = QHBoxLayout(main)
        main_box.setContentsMargins(20, 18, 20, 18)

        score_box = QVBoxLayout()
        self.score_name = QLabel()
        self.score_name.setObjectName("SmallTitle")
        self.score = QLabel("--")
        self.score.setObjectName("Score")
        self.grade = QLabel()
        self.grade.setObjectName("Muted")
        score_box.addWidget(self.score_name)
        score_box.addWidget(self.score)
        score_box.addWidget(self.grade)

        self.button = QPushButton()
        self.button.setObjectName("Primary")
        self.button.clicked.connect(self.run_test)

        main_box.addLayout(score_box)
        main_box.addStretch()
        main_box.addWidget(self.button)
        page.addWidget(main)

        grid = QGridLayout()
        grid.setSpacing(10)
        self.download = Metric("download", "--", "Mbps")
        self.upload = Metric("upload", "--", "Mbps")
        self.ping = Metric("ping", "--", "ms")
        self.jitter = Metric("jitter", "--", "ms")
        self.loss = Metric("packet_loss", "--", "%")
        self.ip = Metric("local_ip", "--", "")
        self.adapter = Metric("adapter", "--", "")
        self.metrics = [self.download, self.upload, self.ping, self.jitter, self.loss, self.ip, self.adapter]

        for i, item in enumerate(self.metrics):
            grid.addWidget(item, i // 4, i % 4)

        page.addLayout(grid)
        page.addStretch()
        self.retranslate()

    def run_test(self):
        if self.worker and self.worker.isRunning():
            return
        self.button.setEnabled(False)
        self.state.setText(t("running"))
        self.worker = TestWorker()
        self.worker.stage.connect(self.stage_changed)
        self.worker.done.connect(self.test_done)
        self.worker.failed.connect(self.test_failed)
        self.worker.start()

    def stage_changed(self, name):
        self.button.setText(t(name))

    def test_done(self, result):
        self.download.set_value(f'{result["download"]:.1f}')
        self.upload.set_value(f'{result["upload"]:.1f}')
        self.ping.set_value(f'{result["ping"]:.1f}')
        self.jitter.set_value(f'{result["jitter"]:.1f}')
        self.loss.set_value(f'{result["packet_loss"]:.1f}')
        self.ip.set_value(result["local_ip"])
        self.adapter.set_value(result["adapter"])
        self.score.setText(str(result["score"]))

        if result["score"] >= 90:
            self.last_grade = "excellent"
        elif result["score"] >= 75:
            self.last_grade = "good"
        elif result["score"] >= 55:
            self.last_grade = "fair"
        else:
            self.last_grade = "poor"

        self.grade.setText(t(self.last_grade))
        self.state.setText(t("online"))
        self.button.setEnabled(True)
        self.button.setText(t("run_test"))

    def test_failed(self, error):
        self.state.setText(t("error"))
        self.grade.setText(t("test_failed"))
        self.button.setEnabled(True)
        self.button.setText(t("run_test"))

    def retranslate(self):
        self.title.setText(t("connection"))
        self.subtitle.setText(t("connection_sub"))
        self.score_name.setText(t("score"))
        self.button.setText(t("run_test"))
        if self.state.text() in ("", "READY", "PRONTO"):
            self.state.setText(t("ready"))
        if self.last_grade:
            self.grade.setText(t(self.last_grade))
        else:
            self.grade.setText(t("unknown"))
        for item in self.metrics:
            item.retranslate()
