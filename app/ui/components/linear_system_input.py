from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from  ui.components.matrix_input import MatrixInput
from  ui.widgets.spin_counter import SpinCounter


EXAMPLE_MATRIX = [["10", "-1", "2"], ["-1", "11", "-1"], ["2", "-1", "10"]]
EXAMPLE_VECTOR = [["6"], ["22"], ["-10"]]
EXAMPLE_INITIAL = [["0"], ["0"], ["0"]]
DEFAULT_SIZE = 3


class LinearSystemInput(QWidget):
    MIN_SIZE = 2
    MAX_SIZE = 8

    def __init__(self, with_initial: bool = False, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        size_row = QHBoxLayout()
        self._size_box = SpinCounter(
            minimum=self.MIN_SIZE, maximum=self.MAX_SIZE, value=DEFAULT_SIZE
        )
        self._size_box.setLayoutDirection(Qt.LeftToRight)
        size_lbl = QLabel("حجم النظام (n × n)")
        size_lbl.setObjectName("FieldLabel")
        size_row.addWidget(size_lbl)
        size_row.addWidget(self._size_box)
        size_row.addStretch(1)
        layout.addLayout(size_row)


        tables = QHBoxLayout()
        tables.setSpacing(16)
        self._matrix = MatrixInput("المصفوفة A", DEFAULT_SIZE, DEFAULT_SIZE)
        self._vector = MatrixInput("المتجه B", DEFAULT_SIZE, 1, ["B"])
        tables.addWidget(self._matrix, 4)
        tables.addWidget(self._vector, 1)
        self._initial: MatrixInput | None = None
        if with_initial:
            self._initial = MatrixInput("القيم الابتدائية (Initial X)", DEFAULT_SIZE, 1, ["X0"])
            tables.addWidget(self._initial, 1)
        layout.addLayout(tables)

        self._size_box.valueChanged.connect(self._resize)
        self.reset()

    def _resize(self, size: int) -> None:
        self._matrix.resize_matrix(size, size)
        self._vector.resize_matrix(size, 1)
        if self._initial is not None:
            self._initial.resize_matrix(size, 1)

    def matrix_cells(self) -> list[list[str]]:
        return self._matrix.values()

    def vector_cells(self) -> list[str]:
        return self._vector.column_values()

    def initial_cells(self) -> list[str]:
        return self._initial.column_values() if self._initial is not None else []

    def reset(self) -> None:
        self._size_box.setValue(DEFAULT_SIZE)
        self._resize(DEFAULT_SIZE)
        self._matrix.set_values(EXAMPLE_MATRIX)
        self._vector.set_values(EXAMPLE_VECTOR)
        if self._initial is not None:
            self._initial.set_values(EXAMPLE_INITIAL)
