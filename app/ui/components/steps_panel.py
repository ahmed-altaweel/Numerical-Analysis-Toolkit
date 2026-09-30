from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QTextBlockFormat, QTextCursor
from PySide6.QtWidgets import QTextEdit, QWidget

from  utils.formatting import starts_with_arabic


class StepsPanel(QTextEdit):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("StepsView")
        self.setReadOnly(True)
        self.setLayoutDirection(Qt.LeftToRight)
        font = QFont()
        font.setFamilies(["Consolas", "DejaVu Sans Mono", "Courier New"])
        font.setStyleHint(QFont.Monospace)
        font.setPointSize(10)
        self.setFont(font)

    def _block_format(self, line: str) -> QTextBlockFormat:
        block = QTextBlockFormat()
        block.setLayoutDirection(Qt.RightToLeft if starts_with_arabic(line) else Qt.LeftToRight)
        return block

    def show_steps(self, steps: list[str]) -> None:
        self.clear()
        cursor = self.textCursor()
        first = True
        for index, step in enumerate(steps):
            if index > 0:
                cursor.insertBlock(self._block_format(""))
            for line in step.split("\n"):
                block = self._block_format(line)
                if first:
                    cursor.setBlockFormat(block)
                    first = False
                else:
                    cursor.insertBlock(block)
                cursor.insertText(line)
        self.moveCursor(QTextCursor.Start)
