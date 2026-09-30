from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget


class InputField(QWidget):
    submitted = Signal()

    def __init__(
        self,
        label: str,
        default: str = "",
        placeholder: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._default = default
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        self._label = QLabel(label)
        self._label.setObjectName("FieldLabel")
        self._edit = QLineEdit(default)
        self._edit.setPlaceholderText(placeholder)
        self._edit.setLayoutDirection(Qt.LeftToRight)
        self._edit.returnPressed.connect(self.submitted.emit)
        layout.addWidget(self._label)
        layout.addWidget(self._edit)

    def text(self) -> str:
        return self._edit.text()

    def set_text(self, value: str) -> None:
        self._edit.setText(value)

    def reset(self) -> None:
        self._edit.setText(self._default)

    def clear(self) -> None:
        self._edit.clear()
