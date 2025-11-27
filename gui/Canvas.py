import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QWidget
from data.Layers import Layers

class Canvas(QWidget):
    signal_paint_masking = QtCore.pyqtSignal(int, int, np.ndarray)
    signal_paint_masking_line = QtCore.pyqtSignal(int, int, int, int, np.ndarray)
    signal_blend = QtCore.pyqtSignal()

    def __init__(self, layers_source: Layers):
        super().__init__()

        self._layers_source = layers_source
        self._layers = {} # { idx: QImage }
        self._temp_layer = None # QImage

        self._layer_width = None
        self._layer_height = None

        self._old_x = None
        self._old_y = None

        self._curr_color = [0, 0, 0, 255]


    def paintEvent(self, e):
        painter = QPainter(self)
        for idx in self._layers_source.get_order():
            layer = self._layers[idx]
            painter.drawImage(0, 0, layer)

        if self._temp_layer is not None:
            painter.drawImage(0, 0, self._temp_layer)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            x, y = int(e.position().x()), int(e.position().y())

            if 0 <= x < self._layer_width and 0 <= y < self._layer_height:
                brush_color = np.array(self._curr_color, dtype=np.uint8)

                self.signal_paint_masking.emit(x, y, brush_color)

                self.update()

            self._old_x = x
            self._old_y = y

    def mouseMoveEvent(self, e):
        x, y = int(e.position().x()), int(e.position().y())
        if (0 <= x < self._layer_width and 0 <= y < self._layer_height and
                0 <= self._old_x < self._layer_width and 0 <= self._old_y < self._layer_height):

            brush_color = np.array(self._curr_color, dtype=np.uint8)

            self.signal_paint_masking_line.emit(
                self._old_x, self._old_y,
                x, y,
                brush_color
            )

            self.update()

        self._old_x = x
        self._old_y = y

    def mouseReleaseEvent(self, e):
        self.signal_blend.emit()
        self.update()


    def set_color(self, color: list):
        self._curr_color = [*color, 255]


    def add_image(self, image: np.ndarray, idx: int):
        self._layers[idx] = QImage(image.data,
                        self._layer_width, self._layer_height, 4*self._layer_width,
                        QImage.Format.Format_RGBA8888)

        self.update()

    @QtCore.pyqtSlot(np.ndarray, int)
    def added_new_image(self, image: np.ndarray, idx: int):
        self.add_image(image, idx)

    @QtCore.pyqtSlot(np.ndarray)
    def added_temp_layer(self, layer: np.ndarray):
        h, w, _ = layer.shape
        self._temp_layer = QImage(layer.data, w, h, QImage.Format.Format_RGBA8888)
        self._layer_width = w
        self._layer_height = h

    @QtCore.pyqtSlot(int)
    def changed_image(self, idx: int):
        self.update()

    @QtCore.pyqtSlot()
    def layers_order_changed(self):
        self.update()