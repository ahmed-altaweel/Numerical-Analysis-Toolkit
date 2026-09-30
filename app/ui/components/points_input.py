from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from  ui.widgets.app_button import AppButton


DEFAULT_POINTS = [("1", "2"), ("2", "3"), ("3", "5"), ("4", "8")]
CELL_SIZE = 36
MAX_VISIBLE_ROWS = 8
MIN_ROWS = 2


class PointsInput(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        lbl = QLabel("النقاط (x, y)")
        lbl.setObjectName("FieldLabel")
        layout.addWidget(lbl)
        self._table = QTableWidget(0, 2)
        self._table.setLayoutDirection(Qt.LeftToRight)
        self._table.setHorizontalHeaderLabels(["x", "y"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.horizontalHeader().setFixedHeight(CELL_SIZE)
        self._table.verticalHeader().setDefaultSectionSize(CELL_SIZE)
        layout.addWidget(self._table)

        buttons = QHBoxLayout()
        add_button = AppButton("إضافة صف", variant="primary")
        remove_button = AppButton("حذف صف", variant="danger")

        add_button.clicked.connect(lambda: self.add_row())
        remove_button.clicked.connect(lambda: self.remove_row())
        buttons.addWidget(add_button)
        buttons.addWidget(remove_button)
        buttons.addStretch(1)
        layout.addLayout(buttons)
        self.reset()

    def _set_row_count(self, count: int) -> None:
        self._table.setRowCount(count)
        for row in range(count):
            for column in range(2):
                if self._table.item(row, column) is None:
                    item = QTableWidgetItem("")
                    item.setTextAlignment(Qt.AlignCenter)
                    self._table.setItem(row, column, item)
        visible = min(count, MAX_VISIBLE_ROWS)
        self._table.setFixedHeight(CELL_SIZE * (visible + 1) + 4)

    def add_row(self) -> None:
        self._set_row_count(self._table.rowCount() + 1)

    def remove_row(self) -> None:
        if self._table.rowCount() > MIN_ROWS:
            self._set_row_count(self._table.rowCount() - 1)

    def points(self) -> list[tuple[str, str]]:
        return [
            (self._table.item(row, 0).text(), self._table.item(row, 1).text())
            for row in range(self._table.rowCount())
        ]

    def reset(self) -> None:
        self._set_row_count(len(DEFAULT_POINTS))
        for row, (x, y) in enumerate(DEFAULT_POINTS):
            self._table.item(row, 0).setText(x)
            self._table.item(row, 1).setText(y)
