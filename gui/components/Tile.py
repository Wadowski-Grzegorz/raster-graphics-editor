from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout


class Tile(QWidget):
    def __init__(self, idx: int, name=None, icon=None, show_name=False):
        super().__init__()
        self._idx = idx
        self._name = name if name else None
        self._icon = icon if icon else None

        self.setMinimumHeight(60)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        self.setLayout(layout)

        if self._icon:
            layout.addWidget(QPixmap(self._icon))
        if show_name and self._name:
            layout.addWidget(QLabel(self._name))

    def sizeHint(self):
        return QSize(100, 60)

    def get_id(self):
        return self._idx

    def get_name(self):
        return self._name