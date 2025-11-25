from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QWidget

from gui.Canvas import Canvas
from gui.Palette import Palette
from data.Layers import Layers
from gui.Layers_panel import Layers_panel
import numpy as np

class Controller(QWidget):
    signal_layer_created = pyqtSignal(np.ndarray, int)
    signal_idx_changed = pyqtSignal(int)

    def __init__(self, canvas: Canvas, palette: Palette, layers: Layers, layers_panel: Layers_panel):
        super().__init__()
        self.canvas = canvas
        self.palette = palette
        self.layers = layers
        self.layers_panel = layers_panel

        self.palette.color_signal.connect(self.canvas.setColor)
        self.layers_panel.signal_layer_create_order.connect(self.layer_create)
        self.signal_layer_created.connect(self.layers_panel.added_new_layer)
        self.layers_panel.signal_layer_choose.connect(self.idx_chosen)
        self.signal_idx_changed.connect(self.canvas.changed_image)
        self.signal_layer_created.connect(self.canvas.added_new_image)

    def layer_create(self):
        image, idx = self.layers.create()
        self.signal_layer_created.emit(image, idx)

    @pyqtSlot(int)
    def idx_chosen(self, idx: int):
        self.signal_idx_changed.emit(idx)