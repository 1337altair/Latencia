from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton, QVBoxLayout, QWidget

from app.diagnostics.analyzer import analyze
from app.i18n.language import t
from app.network.diagnostic_tools import dns_latency, gateway_latency, internet_check
from app.network.internet import network_info
from app.network.ping import ping_test


class DiagnosticWorker(QThread):
    done = Signal(dict)
    failed = Signal()

    def run(self):
        try:
            internet = internet_check()
            network = network_info()
            gateway = gateway_latency()
            dns = dns_latency()

            try:
                result = ping_test(count=10)
            except Exception:
                result = {
                    "ping": 999.0,
                    "jitter": 0.0,
                    "packet_loss": 100.0,
                    "min": 0.0,
                    "max": 0.0,
                }

            self.done.emit(analyze(result, network, gateway, dns, internet))
        except Exception:
            self.failed.emit()


class DiagnosticCard(QFrame):
    def __init__(self, title_key):
        super().__init__()
        self.title_key = title_key
        self.setObjectName("DiagnosticCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)

        self.title = QLabel()
        self.title.setObjectName("DiagnosticCardTitle")

        self.value = QLabel("--")
        self.value.setObjectName("DiagnosticCardValue")

        self.detail = QLabel("")
        self.detail.setObjectName("DiagnosticCardDetail")

        layout.addWidget(self.title)
        layout.addWidget(self.value)
        layout.addWidget(self.detail)

        self.retranslate()

    def set_data(self, value, detail="", state="normal"):
        self.value.setText(value)
        self.detail.setText(detail)
        self.setProperty("state", state)
        self.style().unpolish(self)
        self.style().polish(self)

    def retranslate(self):
        self.title.setText(t(self.title_key))


class DiagnosticsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.last = None

        page = QVBoxLayout(self)
        page.setContentsMargins(30, 28, 30, 28)
        page.setSpacing(16)

        top = QHBoxLayout()

        heading = QVBoxLayout()
        self.title = QLabel()
        self.title.setObjectName("PageTitle")
        self.subtitle = QLabel()
        self.subtitle.setObjectName("PageSubtitle")
        heading.addWidget(self.title)
        heading.addWidget(self.subtitle)

        self.button = QPushButton()
        self.button.setObjectName("Primary")
        self.button.clicked.connect(self.run_diagnostic)

        top.addLayout(heading)
        top.addStretch()
        top.addWidget(self.button)

        page.addLayout(top)

        self.progress = QProgressBar()
        self.progress.setObjectName("DiagnosticProgress")
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(3)
        self.progress.hide()
        page.addWidget(self.progress)

        summary = QFrame()
        summary.setObjectName("DiagnosticSummary")
        summary_layout = QHBoxLayout(summary)
        summary_layout.setContentsMargins(18, 16, 18, 16)
        summary_layout.setSpacing(18)

        score_box = QVBoxLayout()
        self.score_label = QLabel()
        self.score_label.setObjectName("DiagnosticSummaryTitle")
        self.score = QLabel("--")
        self.score.setObjectName("DiagnosticScore")
        score_box.addWidget(self.score_label)
        score_box.addWidget(self.score)

        status_box = QVBoxLayout()
        self.health_label = QLabel()
        self.health_label.setObjectName("DiagnosticSummaryTitle")
        self.health = QLabel()
        self.health.setObjectName("DiagnosticHealth")
        status_box.addWidget(self.health_label)
        status_box.addWidget(self.health)

        summary_layout.addLayout(score_box)
        summary_layout.addSpacing(20)
        summary_layout.addLayout(status_box, 1)

        page.addWidget(summary)

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        self.internet = DiagnosticCard("diag_internet")
        self.gateway = DiagnosticCard("diag_gateway")
        self.ping = DiagnosticCard("ping")
        self.jitter = DiagnosticCard("jitter")
        self.loss = DiagnosticCard("packet_loss")
        self.dns = DiagnosticCard("diag_dns")

        self.cards = [self.internet, self.gateway, self.ping, self.jitter, self.loss, self.dns]
        for i, card in enumerate(self.cards):
            grid.addWidget(card, i // 3, i % 3)

        page.addLayout(grid)

        analysis = QFrame()
        analysis.setObjectName("DiagnosticAnalysis")
        analysis_layout = QVBoxLayout(analysis)
        analysis_layout.setContentsMargins(18, 15, 18, 15)
        analysis_layout.setSpacing(8)

        self.analysis_title = QLabel()
        self.analysis_title.setObjectName("DiagnosticAnalysisTitle")
        self.result = QLabel()
        self.result.setObjectName("Diagnostic")
        self.result.setWordWrap(True)

        analysis_layout.addWidget(self.analysis_title)
        analysis_layout.addWidget(self.result)

        page.addWidget(analysis)
        page.addStretch()

        self.retranslate()

    def run_diagnostic(self):
        if self.worker and self.worker.isRunning():
            return

        self.button.setEnabled(False)
        self.button.setText(t("diag_running"))
        self.progress.setRange(0, 0)
        self.progress.show()
        self.health.setText(t("diag_checking"))

        self.worker = DiagnosticWorker()
        self.worker.done.connect(self.finished)
        self.worker.failed.connect(self.failed)
        self.worker.start()

    def metric_state(self, value, good, fair):
        if value is None:
            return "bad"
        if value <= good:
            return "good"
        if value <= fair:
            return "fair"
        return "bad"

    def quality_text(self, value, good, fair):
        if value is None:
            return "unknown"
        if value <= good:
            return "excellent"
        if value <= fair:
            return "fair"
        return "poor"

    def render_last(self):
        if not self.last:
            if self.worker and self.worker.isRunning():
                self.health.setText(t("diag_checking"))
                self.result.setText(t("diag_waiting"))
            else:
                self.health.setText(t("no_diagnostic"))
                self.result.setText(t("diag_waiting"))
            return

        data = self.last
        metrics = data["metrics"]

        internet_state = "good" if metrics["internet"] == "online" else "bad"
        self.internet.set_data(
            t("online") if metrics["internet"] == "online" else t("diag_offline"),
            metrics["adapter"],
            internet_state,
        )

        gateway_ping = metrics["gateway_ping"]
        gateway_value = f'{gateway_ping:.1f} ms' if gateway_ping is not None else "--"
        self.gateway.set_data(
            gateway_value,
            metrics["gateway"],
            self.metric_state(gateway_ping, 5, 25),
        )

        self.ping.set_data(
            f'{metrics["ping"]:.1f} ms',
            t(self.quality_text(metrics["ping"], 30, 80)),
            self.metric_state(metrics["ping"], 30, 80),
        )

        self.jitter.set_data(
            f'{metrics["jitter"]:.1f} ms',
            t(self.quality_text(metrics["jitter"], 10, 25)),
            self.metric_state(metrics["jitter"], 10, 25),
        )

        self.loss.set_data(
            f'{metrics["packet_loss"]:.1f}%',
            t(self.quality_text(metrics["packet_loss"], 0.1, 2)),
            self.metric_state(metrics["packet_loss"], 0.1, 2),
        )

        dns_value = f'{metrics["dns"]:.1f} ms' if metrics["dns"] is not None else "--"
        dns_detail = t(self.quality_text(metrics["dns"], 60, 150)) if metrics["dns"] is not None else t("diag_failed")
        self.dns.set_data(
            dns_value,
            dns_detail,
            self.metric_state(metrics["dns"], 60, 150),
        )

        self.score.setText(str(data["score"]))
        self.health.setText(t(data["health"]))
        self.result.setText("\n".join(f'• {t(key)}' for key in data["issue_keys"]))

    def finished(self, data):
        self.last = data
        self.render_last()
        self.progress.hide()
        self.button.setEnabled(True)
        self.button.setText(t("run_diagnostics"))

    def failed(self):
        self.progress.hide()
        self.button.setEnabled(True)
        self.button.setText(t("run_diagnostics"))
        self.health.setText(t("test_failed"))
        self.result.setText(t("test_failed"))

    def retranslate(self):
        self.title.setText(t("diagnostics_title"))
        self.subtitle.setText(t("diagnostics_sub"))
        self.score_label.setText(t("diag_health_score"))
        self.health_label.setText(t("diag_result"))
        self.analysis_title.setText(t("diag_analysis"))

        if self.worker and self.worker.isRunning():
            self.button.setText(t("diag_running"))
            self.health.setText(t("diag_checking"))
        else:
            self.button.setText(t("run_diagnostics"))

        for card in self.cards:
            card.retranslate()

        self.render_last()
