from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt6.QtGui import QImage, QColor
from PyQt6.QtCore import Qt
import numpy as np


class Layers(QObject):

    # signal_layer_created = pyqtSignal(QImage, int)
    # signal_idx_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.layers = [] # numpy images rgba

    def create(self):
        # create new layer; emit QImage and index
        # image = QImage(640, 480, QImage.Format.Format_RGBA8888)
        image = np.zeros((480, 640, 4), dtype=np.uint8)
        self.layers.append(image)
        # self.signal_layer_created.emit(image, len(self.layers) - 1)
        return (image, len(self.layers) - 1)
    
    # @pyqtSlot(int)
    # def idx_chosen(self, idx: int):
    #     print(f'idx_chosen image id: {id(self.layers[idx])}')
    #     self.signal_idx_changed.emit(idx)

    def get_layers(self):
        return self.layers