from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt6.QtGui import QImage


class Layers(QObject):

    # signal_layer_created = pyqtSignal(QImage, int)
    # signal_idx_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.layers = []

    def create(self):
        # create new layer; emit QImage and index
        image = QImage(640, 480, QImage.Format.Format_RGBA8888)
        self.layers.append(image)
        # self.signal_layer_created.emit(image, len(self.layers) - 1)
        return (image, len(self.layers) - 1)
    
    # @pyqtSlot(int)
    # def idx_chosen(self, idx: int):
    #     print(f'idx_chosen image id: {id(self.layers[idx])}')
    #     self.signal_idx_changed.emit(idx)

    def get_layers(self):
        return self.layers