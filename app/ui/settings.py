from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QFrame, QLabel, QVBoxLayout, QWidget

from app.i18n.language import get_language, t


class SettingsPage(QWidget):
    language_changed = Signal(str)

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
        box.setSpacing(7)

        self.language_title = QLabel()
        self.language_title.setObjectName("SmallTitle")
        self.language_help = QLabel()
        self.language_help.setObjectName("Muted")

        self.combo = QComboBox()
        self.combo.addItem("Português (Brasil)", "pt-BR")
        self.combo.addItem("English", "en")
        pos = self.combo.findData(get_language())
        if pos >= 0:
            self.combo.setCurrentIndex(pos)
        self.combo.currentIndexChanged.connect(self.change_language)

        self.author_title = QLabel()
        self.author_title.setObjectName("SmallTitle")
        author = QLabel("0xaltair")
        author.setObjectName("Author")

        box.addWidget(self.language_title)
        box.addWidget(self.language_help)
        box.addWidget(self.combo)
        box.addSpacing(18)
        box.addWidget(self.author_title)
        box.addWidget(author)

        page.addWidget(self.title)
        page.addWidget(self.subtitle)
        page.addWidget(panel)
        page.addStretch()
        self.retranslate()

    def change_language(self):
        self.language_changed.emit(self.combo.currentData())

    def retranslate(self):
        self.title.setText(t("settings_title"))
        self.subtitle.setText(t("settings_sub"))
        self.language_title.setText(t("language"))
        self.language_help.setText(t("language_help"))
        self.author_title.setText(t("author"))
