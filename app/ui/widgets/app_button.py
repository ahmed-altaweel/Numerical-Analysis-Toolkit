
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PySide6.QtGui import QCursor, QEnterEvent
from PySide6.QtWidgets import QPushButton, QWidget


class AppButton(QPushButton):

    def __init__(
        self,
        text: str = "",
        variant: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if variant:
            # Convert e.g. "primary" → "PrimaryButton"
            obj_name = variant.capitalize() + "Button"
            self.setObjectName(obj_name)
