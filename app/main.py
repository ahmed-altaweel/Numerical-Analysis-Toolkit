import os
import sys

os.environ.setdefault("QT_API", "pyside6")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from  ui.main_window import MainWindow
from  ui.theme import STYLESHEET


def main() -> int:
    application = QApplication(sys.argv)
    application.setStyle("Fusion")
    application.setLayoutDirection(Qt.RightToLeft)
    application.setStyleSheet(STYLESHEET)
    window = MainWindow()
    window.show()
    return application.exec()


if __name__ == "__main__":
    sys.exit(main())
