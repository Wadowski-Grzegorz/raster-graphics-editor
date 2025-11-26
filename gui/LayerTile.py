from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout


class LayerTile(QWidget):
    def __init__(self, idx: int, name=None):
        super().__init__()
        self._idx = idx
        self._name = name if name else f'Layer {idx}'

        self.setMinimumHeight(60)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel(self._name))

    def sizeHint(self):
        return QSize(100, 60)

    def get_id(self):
        return self._idx

    def get_name(self):
        return self._name