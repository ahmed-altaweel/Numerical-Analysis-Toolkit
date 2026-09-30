from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

CELL_SIZE = 34


class MatrixInput(QWidget):
    def __init__(
        self,
        title: str,
        rows: int,
        columns: int,
        column_headers: list[str] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._column_headers = column_headers
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        title_lbl = QLabel(title)
        title_lbl.setObjectName("FieldLabel")
        layout.addWidget(title_lbl)
        self._table = QTableWidget()
        self._table.setLayoutDirection(Qt.LeftToRight)
        self._table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.horizontalHeader().setFixedHeight(CELL_SIZE)
        self._table.verticalHeader().setDefaultSectionSize(CELL_SIZE)
        layout.addWidget(self._table)
        self.resize_matrix(rows, columns)

    def resize_matrix(self, rows: int, columns: int) -> None:
        self._table.setRowCount(rows)
        self._table.setColumnCount(columns)
        if self._column_headers and len(self._column_headers) == columns:
            self._table.setHorizontalHeaderLabels(self._column_headers)
        else:
            self._table.setHorizontalHeaderLabels([str(index + 1) for index in range(columns)])
        self._table.setVerticalHeaderLabels([str(index + 1) for index in range(rows)])
        for row in range(rows):
            for column in range(columns):
                if self._table.item(row, column) is None:
                    item = QTableWidgetItem("")
                    item.setTextAlignment(Qt.AlignCenter)
                    self._table.setItem(row, column, item)
        self._table.setFixedHeight(CELL_SIZE * (rows + 1) + 4)

    def values(self) -> list[list[str]]:
        return [
            [self._table.item(row, column).text() for column in range(self._table.columnCount())]
            for row in range(self._table.rowCount())
        ]

    def column_values(self) -> list[str]:
        return [row[0] for row in self.values()]

    def set_values(self, values: list[list[str]]) -> None:
        for row, row_values in enumerate(values):
            for column, value in enumerate(row_values):
                self._table.item(row, column).setText(value)

    def clear(self) -> None:
        for row in range(self._table.rowCount()):
            for column in range(self._table.columnCount()):
                self._table.item(row, column).setText("")
