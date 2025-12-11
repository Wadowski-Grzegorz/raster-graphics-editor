from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QFileDialog

from adapters.LayerAdapter import layer_adapter

import resources.settings as settings

class FileManager(QObject):
    signal_image_read_order = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def read_image_order(self, path):
        self.signal_image_read_order.emit(path)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            None,
            "Save File as",
            "my_work.png",
            "PNG (*.png);; JPG (*jpg);; JPEG (*.jpeg)",
        )
        if filename is None:
            return

        width, height = settings.layer_width, settings.layer_height
        result = QImage(width, height, QImage.Format.Format_ARGB32)
        result.fill(0)

        painter = QPainter(result)
        layers = layer_adapter.get_layers_gui()
        for idx in layer_adapter.get_order():
            painter.drawImage(layers[idx].position[0], layers[idx].position[1], layers[idx].layer)
        painter.end()

        if filename.lower().endswith('.png'):
            result.save(filename, "PNG")
        elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            result.save(filename, "JPEG")
        else:
            result.save(filename, "PNG")


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            None,
            "Select a File to Open",
            "",
            "Images (*.png *.jpg)"
        )
        if filename:
            self.read_image_order(filename)