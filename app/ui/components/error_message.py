from PySide6.QtWidgets import QLabel, QWidget


class ErrorMessage(QLabel):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Message")
        self.setWordWrap(True)
        self.hide()

    def show_message(self, text: str, state: str) -> None:
        self.setText(text)
        self.setProperty("state", state)
        self.style().unpolish(self)
        self.style().polish(self)
        self.show()

    def show_success(self, text: str) -> None:
        self.show_message(text, "success")

    def show_warning(self, text: str) -> None:
        self.show_message(text, "warning")

    def show_error(self, text: str) -> None:
        self.show_message(text, "error")

    def clear_message(self) -> None:
        self.setText("")
        self.hide()
