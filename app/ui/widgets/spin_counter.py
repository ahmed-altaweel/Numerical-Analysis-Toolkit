
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor, QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QWidget,
)

# Import palette — defer to avoid circular import at module parse time
def _theme():
    from ui.theme import C_DEEP, C_MID, C_MUTED, C_SOFT, C_BG_INPUT
    return C_DEEP, C_MID, C_MUTED, C_SOFT, C_BG_INPUT



class _StepButton(QPushButton):
    """Small ± button used inside SpinCounter."""

    def __init__(self, symbol: str, parent: QWidget | None = None) -> None:
        super().__init__(symbol, parent)
        C_DEEP, C_MID, C_MUTED, C_SOFT, C_BG_INPUT = _theme()
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedSize(30, 30)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 6px;
                color: {C_MID};
                font-size: 16pt;
                font-weight: bold;
                padding: 0;
            }}
            QPushButton:hover   {{ background: {C_SOFT}; color: {C_DEEP}; }}
            QPushButton:pressed {{ background: #ddd0d6;  color: {C_DEEP}; }}
            """
        )


class SpinCounter(QFrame):
    """
    Custom integer spin counter styled to match the app palette.

    Signals:
        value_changed(int) — emitted whenever the value changes.
    """

    value_changed = Signal(int)

    def __init__(
        self,
        minimum: int = 0,
        maximum: int = 99,
        value: int = 0,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._min = minimum
        self._max = maximum
        self._value = max(minimum, min(maximum, value))

        C_DEEP, C_MID, C_MUTED, C_SOFT, C_BG_INPUT = _theme()

        self.setObjectName("SpinCounter")
        self.setFixedHeight(38)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMinimumWidth(110)
        self.setStyleSheet(
            f"""
            QFrame#SpinCounter {{
                background: {C_BG_INPUT};
                border: 1.5px solid #ddd0d6;
                border-radius: 9px;
            }}
            QFrame#SpinCounter:hover {{
                border-color: {C_MUTED};
            }}
            QLabel#SpinValue {{
                color: {C_DEEP};
                font-weight: bold;
                font-size: 11pt;
                background: transparent;
            }}
            """
        )


        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(0)

        self._dec_btn = _StepButton("−")
        self._dec_btn.clicked.connect(self._decrement)

        self._value_label = QLabel(str(self._value))
        self._value_label.setObjectName("SpinValue")
        self._value_label.setAlignment(Qt.AlignCenter)
        self._value_label.setLayoutDirection(Qt.LeftToRight)

        self._inc_btn = _StepButton("+")
        self._inc_btn.clicked.connect(self._increment)

        layout.addWidget(self._dec_btn)
        layout.addWidget(self._value_label, 1)
        layout.addWidget(self._inc_btn)

        self._refresh_buttons()

    # ── public API ──────────────────────────────────────────────────────────

    def value(self) -> int:
        return self._value

    def setValue(self, val: int) -> None:
        clamped = max(self._min, min(self._max, val))
        if clamped != self._value:
            self._value = clamped
            self._value_label.setText(str(self._value))
            self._refresh_buttons()
            self.value_changed.emit(self._value)

    def setRange(self, minimum: int, maximum: int) -> None:
        self._min = minimum
        self._max = maximum
        self.setValue(self._value)

    def setMinimum(self, minimum: int) -> None:
        self.setRange(minimum, self._max)

    def setMaximum(self, maximum: int) -> None:
        self.setRange(self._min, maximum)

    # ── Qt compatibility shim (matches QSpinBox signal name) ────────────────
    @property
    def valueChanged(self):  # noqa: N802
        return self.value_changed

    # ── internals ────────────────────────────────────────────────────────────

    def _increment(self) -> None:
        self.setValue(self._value + 1)

    def _decrement(self) -> None:
        self.setValue(self._value - 1)

    def _refresh_buttons(self) -> None:
        self._dec_btn.setEnabled(self._value > self._min)
        self._inc_btn.setEnabled(self._value < self._max)

    # Layout direction forced LTR so − is always left, + always right
    def setLayoutDirection(self, direction) -> None:  # noqa: ARG002
        super().setLayoutDirection(Qt.LeftToRight)
