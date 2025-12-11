from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QImage, QPainter

from adapters.LayerAdapter import layer_adapter

import resources.settings as settings

class FileManager(QObject):
    signal_image_read_order = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def read_image(self, path):
        self.signal_image_read_order.emit(path)

    def save_as_image(self, location, type):
        width, height = settings.layer_width, settings.layer_height
        result = QImage(width, height, QImage.Format.Format_ARGB32)
        result.fill(0)

        painter = QPainter(result)
        layers = layer_adapter.get_layers_gui()
        for l in layers:
            painter.drawImage(l.position, l)
        painter.end()

        result.save(location, type)