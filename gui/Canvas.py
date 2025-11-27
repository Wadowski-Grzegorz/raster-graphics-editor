import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter, QColor, QPixmap
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
        self.background = None

        self._layer_width = None
        self._layer_height = None

        self._scale = 1

        self._offset_x = 0
        self._offset_y = 0

        self._old_x = None
        self._old_y = None

        self._curr_color = [0, 0, 0, 255]


    def paintEvent(self, e):
        painter = QPainter(self)
        scaled_layer_x, scaled_layer_y = int(self._layer_width * self._scale), int(self._layer_height * self._scale)

        if self.background:
            (painter.drawPixmap(self._offset_x, self._offset_y, self.background))

        for idx in self._layers_source.get_order():
            layer = self._layers[idx]
            pixmap = (QPixmap
                      .fromImage(layer)
                      .scaled(scaled_layer_x, scaled_layer_y,
                              Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                              )
                      )
            painter.drawPixmap(self._offset_x, self._offset_y, pixmap)

        if self._temp_layer is not None:
            pixmap = (QPixmap
                      .fromImage(self._temp_layer)
                      .scaled(scaled_layer_x, scaled_layer_y,
                              Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                      )
            painter.drawPixmap(self._offset_x, self._offset_y, pixmap)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            x, y = (int(v) for v in self.convert_to_layer(e.position()))

            if 0 <= x < self._layer_width and 0 <= y < self._layer_height:
                brush_color = np.array(self._curr_color, dtype=np.uint8)

                self.signal_paint_masking.emit(x, y, brush_color)

                self.update()

            self._old_x = x
            self._old_y = y

    def mouseMoveEvent(self, e):
        x, y = (int(v) for v in self.convert_to_layer(e.position()))
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

    def wheelEvent(self, e):
        angle = e.angleDelta().y()
        if angle > 0:
            self._scale *= 1.1
        else:
            self._scale /= 1.1

        self._scale = max(0.1, min(10.0, self._scale))

        self.resize_values()

        self.update()

    def resizeEvent(self, e):
        if self._layer_width is not None and self._layer_height is not None:
            self.resize_values()

        self.update()

    def resize_background(self):
        if self.background is not None:
            scaled_layer_x = int(self._layer_width * self._scale)
            scaled_layer_y = int(self._layer_height * self._scale)

            self.background = self.background.scaled(
                scaled_layer_x, scaled_layer_y,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.FastTransformation
            )

    def resize_values(self):
        self._offset_x = int((self.width() - self._layer_width * self._scale) // 2)
        self._offset_y = int((self.height() - self._layer_height * self._scale) // 2)
        self.resize_background()

    def create_background(self):
        self.background = QPixmap(self._layer_width, self._layer_height)
        self.background.fill(QColor(170, 170, 170))

    def convert_to_layer(self, position):
        x = (position.x() - self._offset_x) / self._scale
        y = (position.y() - self._offset_y) / self._scale
        return x, y

    def set_color(self, color: list):
        self._curr_color = [*color, 255]

    def add_image(self, image: np.ndarray, idx: int):
        self._layers[idx] = QImage(image.data,
                        self._layer_width, self._layer_height, 4*self._layer_width,
                        QImage.Format.Format_RGBA8888)

        self.update()

    def set_layer_size(self, width, height):
        self._layer_width = width
        self._layer_height = height

        self.resize_values()

    @QtCore.pyqtSlot(np.ndarray, int)
    def added_new_image(self, image: np.ndarray, idx: int):
        self.add_image(image, idx)

    @QtCore.pyqtSlot(np.ndarray)
    def added_temp_layer(self, layer: np.ndarray):
        h, w, _ = layer.shape
        self._temp_layer = QImage(layer.data, w, h, QImage.Format.Format_RGBA8888)
        self.set_layer_size(w, h)
        self.create_background()

    @QtCore.pyqtSlot(int)
    def changed_image(self, idx: int):
        self.update()

    @QtCore.pyqtSlot()
    def layers_order_changed(self):
        self.update()