"""
Enhanced Sidebar widget with:
  • Gradient deep-indigo background
  • Logo/icon area at the top
  • Section headers styled as ALL-CAPS category labels
  • Smooth active-item indicator
  • Version badge at the bottom
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)


class Sidebar(QFrame):
    page_selected = Signal(int)

    def __init__(
        self,
        sections: list[tuple[str, list[str]]],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(295)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Header area ───────────────────────────────────────────────────
        header = QFrame()
        header.setObjectName("SidebarHeader")
        header.setStyleSheet(
            """
            QFrame#SidebarHeader {
                background: rgba(0,0,0,0.18);
                border-bottom: 1px solid rgba(255,255,255,0.06);
                padding: 6px 0 6px 0;
            }
            """
        )
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(18, 16, 18, 14)
        header_layout.setSpacing(3)

        # App icon / monogram
        monogram = QLabel("∑")
        monogram.setStyleSheet(
            """
            color: #E9D5DA;
            font-size: 24pt;
            font-weight: bold;
            font-family: 'Segoe UI Variable Display', 'Segoe UI', serif;
            background: transparent;
            padding: 0;
            """
        )

        title = QLabel("Numerical Analysis")
        title.setObjectName("SidebarTitle")

        subtitle = QLabel("أدوات التحليل العددي")
        subtitle.setObjectName("SidebarSubtitle")

        header_layout.addWidget(monogram)
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        layout.addWidget(header)

        # ── Nav list ─────────────────────────────────────────────────────
        self._list = QListWidget()
        self._list.setObjectName("SidebarList")
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._list.setTextElideMode(Qt.ElideNone)
        self._list.setSpacing(1)
        from PySide6.QtGui import QCursor
        self._list.setCursor(QCursor(Qt.PointingHandCursor))

        self._first_item: QListWidgetItem | None = None
        index = 0
        for section_title, names in sections:
            # Category header row
            header_item = QListWidgetItem(f"  {section_title.upper()}")
            header_item.setFlags(Qt.NoItemFlags)
            self._list.addItem(header_item)

            for name in names:
                item = QListWidgetItem(f"  {name}")
                item.setData(Qt.UserRole, index)
                self._list.addItem(item)
                if self._first_item is None:
                    self._first_item = item
                index += 1

        self._list.currentItemChanged.connect(self._on_item_changed)
        layout.addWidget(self._list, 1)

        # ── Footer version badge ──────────────────────────────────────────
        footer = QLabel("v1.0  ·  MATH 301")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet(
            """
            color: #4e4b72;
            font-size: 7.5pt;
            letter-spacing: 0.6px;
            background: transparent;
            padding: 10px 0;
            border-top: 1px solid rgba(255,255,255,0.05);
            """
        )
        layout.addWidget(footer)

    # ── Signal plumbing ───────────────────────────────────────────────────
    def _on_item_changed(
        self,
        current: QListWidgetItem | None,
        _previous: QListWidgetItem | None,
    ) -> None:
        if current is None:
            return
        index = current.data(Qt.UserRole)
        if index is not None:
            self.page_selected.emit(int(index))

    def select_first(self) -> None:
        if self._first_item is not None:
            self._list.setCurrentItem(self._first_item)
