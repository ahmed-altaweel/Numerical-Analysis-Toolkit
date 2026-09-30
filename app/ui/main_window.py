from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from  ui.page_registry import SECTIONS
from  ui.widgets.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Numerical Analysis")
        self.resize(1320, 860)
        self.setMinimumSize(1000, 660)

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._stack = QStackedWidget()
        for section in SECTIONS:
            for entry in section.entries:
                self._stack.addWidget(entry.factory())

        self._sidebar = Sidebar([(section.title, [entry.title for entry in section.entries]) for section in SECTIONS])
        self._sidebar.page_selected.connect(self._stack.setCurrentIndex)

        layout.addWidget(self._sidebar)
        layout.addWidget(self._stack, 1)
        self.setCentralWidget(central)
        self._sidebar.select_first()
