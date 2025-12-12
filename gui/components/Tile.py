from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout


class Tile(QWidget):
    def __init__(self, idx: int=None, name=None, icon=None, show_name=False, on_click=None):
        super().__init__()
        self._idx = idx
        self._name = name if name else None
        self._icon = icon if icon else None
        self._on_click = on_click if on_click else None

        self.setMinimumHeight(30)
        self.setMinimumWidth(30)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.setStyleSheet("border: 1px solid black; padding: 0px; margin: 0px; ")
        w, h = 0, 0
        if self._icon:
            label = QLabel()
            # label.setStyleSheet("border: 1px solid blue; padding: 0px; margin: 0px; ")
            pixmap = self._icon.pixmap(30, 30)
            label.setPixmap(pixmap)
            layout.addWidget(label)
            w += 50
            h += 50
        if show_name and self._name:
            name = QLabel(self._name)
            layout.addWidget(name)
            w += 80
            h += 40

        self.setFixedSize(QSize(w, h))

    def get_id(self):
        return self._idx

    def get_name(self):
        return self._name
    
    def mousePressEvent(self, event):
        if self._on_click:
            self._on_click()
        super().mousePressEvent(event)