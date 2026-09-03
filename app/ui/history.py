from PySide6.QtWidgets import QAbstractItemView, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from app.database.database import recent
from app.i18n.language import t


class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        page = QVBoxLayout(self)
        page.setContentsMargins(30, 28, 30, 28)
        page.setSpacing(18)

        self.title = QLabel()
        self.title.setObjectName("PageTitle")
        self.subtitle = QLabel()
        self.subtitle.setObjectName("PageSubtitle")
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)

        page.addWidget(self.title)
        page.addWidget(self.subtitle)
        page.addWidget(self.table)
        self.retranslate()
        self.refresh()

    def refresh(self):
        rows = recent(100)
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            values = [
                row["created_at"],
                f'{row["download"]:.1f} Mbps',
                f'{row["upload"]:.1f} Mbps',
                f'{row["ping"]:.1f} ms',
                f'{row["jitter"]:.1f} ms',
                f'{row["packet_loss"]:.1f}%',
                str(row["score"])
            ]
            for c, value in enumerate(values):
                self.table.setItem(r, c, QTableWidgetItem(value))

    def retranslate(self):
        self.title.setText(t("history_title"))
        self.subtitle.setText(t("history_sub"))
        self.table.setHorizontalHeaderLabels([
            t("date"), t("download"), t("upload"), t("ping"), t("jitter"), t("packet_loss"), t("score")
        ])
