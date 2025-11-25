from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QWidget

from gui.Canvas import Canvas
from gui.Palette import Palette
from data.Layers import Layers
from gui.Layers_panel import Layers_panel
import numpy as np

class Controller(QWidget):

    def __init__(self, canvas: Canvas, palette: Palette, layers: Layers, layers_panel: Layers_panel):
        super().__init__()
        self.canvas = canvas
        self.palette = palette
        self.layers = layers
        self.layers_panel = layers_panel

        self.palette.color_signal.connect(self.canvas.setColor)
        self.layers_panel.signal_layer_create_order.connect(self.layer_create)
        self.layers_panel.signal_layer_choose.connect(self.idx_chosen)

    def layer_create(self):
        image, idx = self.layers.create()
        self.layers_panel.added_new_layer(image, idx)
        self.canvas.added_new_image(image, idx)

    @pyqtSlot(int)
    def idx_chosen(self, idx: int):
        self.canvas.changed_image(idx)