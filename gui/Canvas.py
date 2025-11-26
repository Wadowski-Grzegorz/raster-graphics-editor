import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QWidget

class Canvas(QWidget):
    signal_paint_masking = QtCore.pyqtSignal(int, int, np.ndarray)
    signal_paint_masking_line = QtCore.pyqtSignal(int, int, int, int, np.ndarray)
    signal_blend = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.curr_idx = None
        self.layers = {} # { idx: QImage }
        self.temp_layer = None # QImage

        self.layer_width = None
        self.layer_height = None

        self.old_x = None
        self.old_y = None

        self.curr_color = (0, 0, 0)


    def paintEvent(self, e):
        painter = QPainter(self)
        for image in self.layers.values():
            painter.drawImage(0, 0, image)
        if self.temp_layer is not None:
            painter.drawImage(0, 0, self.temp_layer)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            x, y = int(e.position().x()), int(e.position().y())

            if 0 <= x < self.layer_width and 0 <= y < self.layer_height:
                color = (*self.curr_color, 255)
                brush_color = np.array(color, dtype=np.uint8)

                self.signal_paint_masking.emit(x, y, brush_color)

                self.update()

            self.old_x = x
            self.old_y = y

    def mouseMoveEvent(self, e):
        x, y = int(e.position().x()), int(e.position().y())
        if (0 <= x < self.layer_width and 0 <= y < self.layer_height and
                0 <= self.old_x < self.layer_width and 0 <= self.old_y < self.layer_height):

            color = (*self.curr_color, 255)
            brush_color = np.array(color, dtype=np.uint8)

            self.signal_paint_masking_line.emit(
                self.old_x, self.old_y,
                x, y,
                brush_color
            )

            self.update()

        self.old_x = x
        self.old_y = y

    def mouseReleaseEvent(self, e):
        self.signal_blend.emit()
        self.update()


    def setColor(self, color: tuple):
        self.curr_color = color

    def set_curr_image(self, idx: int):
        self.curr_idx = idx

    def add_image(self, image, idx: int):
        qimage = QImage(image.data,
                        self.layer_width, self.layer_height, 4*self.layer_width,
                        QImage.Format.Format_RGBA8888)

        self.layers[idx] = qimage

        self.set_curr_image(idx)
        self.update()

    @QtCore.pyqtSlot(np.ndarray, int)
    def added_new_image(self, image: QImage, idx: int):
        self.add_image(image, idx)

    @QtCore.pyqtSlot(np.ndarray)
    def added_temp_layer(self, layer: np.ndarray):
        h, w, _ = layer.shape
        qLayer = QImage(layer.data, w, h, QImage.Format.Format_RGBA8888)
        self.temp_layer = qLayer
        self.layer_width = w
        self.layer_height = h

    @QtCore.pyqtSlot(int)
    def changed_image(self, idx: int):
        self.set_curr_image(idx)
        self.update()