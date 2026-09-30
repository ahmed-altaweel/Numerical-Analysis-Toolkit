from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QButtonGroup, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QWidget


class MethodSelector(QWidget):
    """A row of toggle buttons where exactly one is active at a time."""

    method_changed = Signal(str)

    def __init__(
        self,
        options: list[tuple[str, str]],
        label: str = "اختر الطريقة",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._value: str = options[0][1] if options else ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        heading = QLabel(label)
        heading.setObjectName("InputLabel")
        layout.addWidget(heading)

        row = QHBoxLayout()
        row.setSpacing(8)
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._buttons: list[QPushButton] = []

        for index, (text, key) in enumerate(options):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setProperty("method_key", key)
            btn.setObjectName("MethodButton")

            # Round corners only on the edges of the group
            if index == 0:
                btn.setProperty("position", "first")
            elif index == len(options) - 1:
                btn.setProperty("position", "last")
            else:
                btn.setProperty("position", "middle")

            self._group.addButton(btn, index)
            self._buttons.append(btn)
            row.addWidget(btn)

        row.addStretch(1)
        layout.addLayout(row)

        # select first by default
        if self._buttons:
            self._buttons[0].setChecked(True)

        self._group.idClicked.connect(self._on_clicked)

    def _on_clicked(self, btn_id: int) -> None:
        btn = self._buttons[btn_id]
        self._value = btn.property("method_key")
        self.method_changed.emit(self._value)

    def value(self) -> str:
        return self._value

    def reset(self) -> None:
        if self._buttons:
            self._buttons[0].setChecked(True)
            self._value = self._buttons[0].property("method_key")
