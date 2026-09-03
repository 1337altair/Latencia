import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QWidget

from app.i18n.language import set_language, t
from app.ui.dashboard import DashboardPage
from app.ui.diagnostics import DiagnosticsPage
from app.ui.history import HistoryPage
from app.ui.monitor import MonitorPage
from app.ui.settings import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Latencia")
        self.resize(1080, 690)
        self.setMinimumSize(900, 590)

        base = QWidget()
        layout = QHBoxLayout(base)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(185)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(17, 22, 17, 16)
        side.setSpacing(6)

        brand = QLabel("LATENCIA")
        brand.setObjectName("Brand")
        self.brand_small = QLabel()
        self.brand_small.setObjectName("BrandSmall")
        side.addWidget(brand)
        side.addWidget(self.brand_small)
        side.addSpacing(20)

        self.stack = QStackedWidget()
        self.dashboard = DashboardPage()
        self.monitor = MonitorPage()
        self.diagnostics = DiagnosticsPage()
        self.history = HistoryPage()
        self.settings = SettingsPage()
        self.pages = [self.dashboard, self.monitor, self.diagnostics, self.history, self.settings]

        for page in self.pages:
            self.stack.addWidget(page)

        self.nav = []
        for i in range(5):
            button = QPushButton()
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda checked=False, index=i: self.open_page(index))
            side.addWidget(button)
            self.nav.append(button)

        side.addStretch()
        signature = QLabel("Feito por: 0xaltair")
        signature.setObjectName("Signature")
        version = QLabel("v0.1.0")
        version.setObjectName("Version")
        side.addWidget(signature)
        side.addWidget(version)

        layout.addWidget(sidebar)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(base)

        self.settings.language_changed.connect(self.language_changed)
        self.retranslate()
        self.open_page(0)

    def open_page(self, index):
        self.stack.setCurrentIndex(index)
        for i, button in enumerate(self.nav):
            button.setChecked(i == index)
        if index == 3:
            self.history.refresh()

    def language_changed(self, language):
        set_language(language)
        self.retranslate()

    def retranslate(self):
        self.brand_small.setText(t("network_tools"))
        names = [t("dashboard"), t("monitor"), t("diagnostics"), t("history"), t("settings")]
        for button, name in zip(self.nav, names):
            button.setText(name)
        for page in self.pages:
            page.retranslate()

    def closeEvent(self, event):
        self.monitor.stop_monitoring()
        event.accept()


def start():
    app = QApplication(sys.argv)
    app.setApplicationName("Latencia")
    style = Path(__file__).resolve().parents[1] / "assets" / "styles" / "main.qss"
    app.setStyleSheet(style.read_text(encoding="utf-8"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
