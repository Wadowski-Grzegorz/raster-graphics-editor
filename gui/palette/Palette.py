from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDockWidget

from gui.palette.ColorMap import ColorMap
from gui.palette.HueBar import HueBar


class Palette(QDockWidget):
    signal_color_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._color = QColor(0, 0, 0)

        dummy = QWidget()
        self.setWidget(dummy)
        self.setTitleBarWidget(QWidget())


        layout = QHBoxLayout(dummy)
        self.setLayout(layout)

        self.color_map = ColorMap()
        layout.addWidget(self.color_map)

        self.hue_bar = HueBar()
        layout.addWidget(self.hue_bar)

        self.color_map.signal_color_changed.connect(self.color_changed)
        self.hue_bar.signal_hue_changed.connect(self.hue_changed)

    def hue_changed(self, hue: int):
        sat, val = self._color.saturation(), self._color.value()
        self._color = QColor(hue, sat, val)
        self.color_map.set_hue(hue)

    def color_changed(self, color: QColor):
        self._color = color

        r, g, b, _ = self._color.getRgb()
        self.signal_color_changed.emit([r, g, b])