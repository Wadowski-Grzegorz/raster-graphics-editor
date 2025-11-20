from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QWidget
from Layers import Layers

class Controller(QWidget):
    signal_layer_created = pyqtSignal(QImage, int)
    signal_idx_changed = pyqtSignal(int)

    def __init__(self, layers: Layers):
        super().__init__()
        self.layers = layers

    def layer_create(self):
        image, idx = self.layers.create()
        self.signal_layer_created.emit(image, idx)

    @pyqtSlot(int)
    def idx_chosen(self, idx: int):
        self.signal_idx_changed.emit(idx)