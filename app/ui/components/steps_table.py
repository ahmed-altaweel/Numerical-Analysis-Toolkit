from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem, QWidget

from  utils.formatting import format_number


class StepsTable(QTableWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setLayoutDirection(Qt.LeftToRight)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setShowGrid(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.verticalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().setDefaultSectionSize(38)
        self.setFocusPolicy(Qt.NoFocus)

    def show_table(self, columns: list[str], rows: list[list[Any]]) -> None:
        self.clear()
        self.setColumnCount(len(columns))
        self.setRowCount(len(rows))
        self.setHorizontalHeaderLabels(columns)

        mono_font = QFont()
        mono_font.setFamilies(["Cascadia Code", "Consolas", "DejaVu Sans Mono"])
        mono_font.setStyleHint(QFont.Monospace)
        mono_font.setPointSize(10)

        for row_index, row in enumerate(rows):
            for column_index, value in enumerate(row):
                item = QTableWidgetItem(format_number(value))
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(mono_font)
                self.setItem(row_index, column_index, item)
