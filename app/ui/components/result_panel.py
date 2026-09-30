import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from  models.algorithm_result import AlgorithmResult
from  ui.components.error_message import ErrorMessage
from  utils.formatting import format_number

PLACEHOLDER = "لم يتم إجراء أي حساب بعد. أدخل البيانات ثم اضغط «احسب»."


class ResultPanel(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        title = QLabel("النتيجة (Result)")
        title.setObjectName("CardTitle")

        self._status   = ErrorMessage()
        self._warnings = ErrorMessage()

        self._values = QWidget()
        self._grid = QGridLayout(self._values)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setHorizontalSpacing(24)
        self._grid.setVerticalSpacing(10)
        self._grid.setColumnStretch(1, 1)

        layout.addWidget(title)
        layout.addWidget(self._status)
        layout.addWidget(self._warnings)
        layout.addWidget(self._values)

    def _clear_values(self) -> None:
        while self._grid.count():
            item = self._grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def show_placeholder(self) -> None:
        self._clear_values()
        self._warnings.clear_message()
        self._status.show_message(PLACEHOLDER, "warning")
        self._status.setProperty("state", "neutral")
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)

    def show_result(self, result: AlgorithmResult, label: str, error_label: str) -> None:
        self._clear_values()

        if result.success:
            self._status.show_success(result.message or "اكتمل الحساب بنجاح.")
        else:
            self._status.show_error(result.message or "تعذر إكمال الحساب.")

        if result.warnings:
            self._warnings.show_warning("\n".join(f"• {text}" for text in result.warnings))
        else:
            self._warnings.clear_message()

        rows = self._build_rows(result, label, error_label)
        primary_labels = {label} | {f"x{i}" for i in range(1, 100)}

        for row, (name, value) in enumerate(rows):
            is_primary = name in primary_labels

            name_label = QLabel(name)
            name_label.setObjectName("ResultPrimaryName" if is_primary else "ResultName")

            value_label = QLabel(value)
            value_label.setObjectName("ResultPrimaryValue" if is_primary else "ResultValue")
            value_label.setLayoutDirection(Qt.LeftToRight)
            value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

            self._grid.addWidget(name_label, row, 0, Qt.AlignTop)
            self._grid.addWidget(value_label, row, 1, Qt.AlignLeft | Qt.AlignTop)

    @staticmethod
    def _build_rows(result: AlgorithmResult, label: str, error_label: str) -> list[tuple[str, str]]:
        rows: list[tuple[str, str]] = []
        if result.result is not None:
            if isinstance(result.result, (list, tuple, np.ndarray)):
                for index, item in enumerate(np.asarray(result.result).ravel(), start=1):
                    rows.append((f"x{index}", format_number(item, 10)))
            else:
                rows.append((label, format_number(result.result, 10)))
        if result.iteration_count is not None:
            rows.append(("عدد التكرارات", str(result.iteration_count)))
        if result.error is not None:
            rows.append((error_label, format_number(result.error, 6)))
        return rows
