from PyQt6 import QtCore
from PyQt6.QtCore import QObject


class ImageCaretaker(QObject):
    signal_image_read_order = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def read_image(self, path):
        self.signal_image_read_order.emit(path)
