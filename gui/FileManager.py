from PyQt6 import QtCore
from PyQt6.QtCore import QObject, pyqtSlot, Qt
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QFileDialog

import os
import resources.settings as settings

class FileManager(QObject):
    signal_image_read = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._controller = None

    def read_image_order(self, path):
        self.signal_image_read.emit(path)

    @pyqtSlot()
    def save_file(self):
        filename, selected_filter = QFileDialog.getSaveFileName(
            None,
            "Save File as",
            "my_work.png",
            "All Files (*)",
        )
        if not filename:
            return

        print(filename)
        name, extension = os.path.splitext(filename)
        if not extension:
            filename = os.path.splitext(filename)[0] + '.png'
            extension = '.png'
                
        width, height = settings.layer_width, settings.layer_height
        result = QImage(width, height, QImage.Format.Format_ARGB32)
        if extension == ".png":
            result.fill(255)
        elif extension in ('.jpg', '.jpeg'):
            result.fill(Qt.GlobalColor.white)

        painter = QPainter(result)

        if self._controller is None:
            return
        layers = self._controller.get_layers_gui()
        for idx in self._controller.get_layers_order():
            painter.drawImage(layers[idx].position[0], layers[idx].position[1], layers[idx].layer)
        painter.end()

        print('saving file:', filename)
        success = result.save(filename)
        print(success)

    @pyqtSlot()
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            None,
            "Select a File to Open",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )
        if filename:
            self.read_image_order(filename)

    def set_controller(self, controller):
        self._controller = controller