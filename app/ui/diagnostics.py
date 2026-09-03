from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from app.diagnostics.analyzer import analyze
from app.i18n.language import t
from app.network.internet import network_info
from app.network.ping import ping_test


class DiagnosticsPage(QWidget):
    def __init__(self):
        super().__init__()
        page = QVBoxLayout(self)
        page.setContentsMargins(30, 28, 30, 28)
        page.setSpacing(18)

        self.title = QLabel()
        self.title.setObjectName("PageTitle")
        self.subtitle = QLabel()
        self.subtitle.setObjectName("PageSubtitle")

        panel = QFrame()
        panel.setObjectName("Panel")
        box = QVBoxLayout(panel)
        box.setContentsMargins(20, 18, 20, 18)
        self.result = QLabel()
        self.result.setWordWrap(True)
        self.result.setObjectName("Diagnostic")
        self.button = QPushButton()
        self.button.setObjectName("Primary")
        self.button.clicked.connect(self.run_diagnostic)
        box.addWidget(self.result)
        box.addSpacing(12)
        box.addWidget(self.button)

        page.addWidget(self.title)
        page.addWidget(self.subtitle)
        page.addWidget(panel)
        page.addStretch()
        self.retranslate()

    def run_diagnostic(self):
        try:
            result = ping_test(count=8)
            self.result.setText(analyze(result, network_info()))
        except Exception:
            self.result.setText(t("test_failed"))

    def retranslate(self):
        self.title.setText(t("diagnostics_title"))
        self.subtitle.setText(t("diagnostics_sub"))
        self.button.setText(t("run_diagnostics"))
        if not self.result.text() or self.result.text() in ("No diagnostic yet.", "Nenhum diagnóstico ainda."):
            self.result.setText(t("no_diagnostic"))
