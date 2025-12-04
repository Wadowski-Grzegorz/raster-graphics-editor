import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPixmap
from PyQt6.QtWidgets import QWidget
from core.layer.DataCenter import data_center
from adapters.Adapter import adapter

import utils
from resources import settings


class Canvas(QWidget):
    signal_paint_masking = QtCore.pyqtSignal(int, int, np.ndarray)
    signal_paint_masking_line = QtCore.pyqtSignal(int, int, int, int, np.ndarray)
    signal_blend = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self._layers_dto = None
        self._temp_layer = None # QImage
        self.background = None

        self._scale = 1

        self._offset_x = 0
        self._offset_y = 0

        self._old_x = None
        self._old_y = None

        self._curr_color = [0, 0, 0, 255]

    def paint(self, painter, paint_me, x, y, scaled_x, scaled_y):
        pixmap = (
            QPixmap
                .fromImage(paint_me)
                .scaled(
                        scaled_x, scaled_y,
                        Qt.AspectRatioMode.IgnoreAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                )
        )
        painter.drawPixmap(x, y, pixmap)

    def paintEvent(self, e):
        painter = QPainter(self)
        scaled_layer_x, scaled_layer_y = (
            int(settings.layer_width * self._scale),
            int(settings.layer_height * self._scale)
        )

        if self.background:
            (painter.drawPixmap(self._offset_x, self._offset_y, self.background))

        for idx in data_center.get_order():
            self._layers_dto = adapter.layers_to_dto(data_center.get_layers())

            layer_dto = self._layers_dto[idx]
            self.paint(painter, layer_dto.qLayer, self._offset_x, self._offset_y, scaled_layer_x, scaled_layer_y)

            if layer_dto.objects:
                for ob in layer_dto.objects:
                    if ob.qImage is not None and not ob.qImage.isNull():
                        scaled_img_x, scaled_img_y = (int(s * self._scale) for s in ob.size)
                        img_px, img_py = ob.position

                        self.paint(painter, ob.qImage,
                                   self._offset_x + img_px, self._offset_y + img_py,
                                   scaled_img_x, scaled_img_y)

        if self._temp_layer is not None:
            self.paint(painter, self._temp_layer, self._offset_x, self._offset_y, scaled_layer_x, scaled_layer_y)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            x, y = (int(v) for v in self.convert_to_layer(e.position()))

            if 0 <= x < settings.layer_width and 0 <= y < settings.layer_height:
                brush_color = np.array(self._curr_color, dtype=np.uint8)

                self.signal_paint_masking.emit(x, y, brush_color)

                self.update()

            self._old_x = x
            self._old_y = y

    def mouseMoveEvent(self, e):
        x, y = (int(v) for v in self.convert_to_layer(e.position()))
        if (
                0 <= x < settings.layer_width and 0 <= y < settings.layer_height and
                0 <= self._old_x < settings.layer_width and 0 <= self._old_y < settings.layer_height and
                abs(x - self._old_x) >= 1 and abs(y - self._old_y) >= 1
        ):

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
        if settings.layer_width is not None and settings.layer_height is not None:
            self.resize_values()

        self.update()

    def resize_background(self):
        if self.background is not None:
            scaled_layer_x = int(settings.layer_width * self._scale)
            scaled_layer_y = int(settings.layer_height * self._scale)

            self.background = self.background.scaled(
                scaled_layer_x, scaled_layer_y,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.FastTransformation
            )

    def resize_values(self):
        self._offset_x = int((self.width() - settings.layer_width * self._scale) // 2)
        self._offset_y = int((self.height() - settings.layer_height * self._scale) // 2)
        self.resize_background()

    def create_background(self):
        self.background = QPixmap(settings.layer_width, settings.layer_height)
        self.background.fill(QColor(170, 170, 170))

    def convert_to_layer(self, position):
        x = (position.x() - self._offset_x) / self._scale
        y = (position.y() - self._offset_y) / self._scale
        return x, y

    def set_color(self, color: list):
        self._curr_color = [*color, 255]

    @QtCore.pyqtSlot()
    def refresh_data(self):
        self._layers_dto = adapter.layers_to_dto(data_center.get_layers())
        self.update()

    @QtCore.pyqtSlot(np.ndarray)
    def added_temp_layer(self, layer: np.ndarray):
        self._temp_layer = utils.np_to_q_ptr(layer)
        self.create_background()
        self.resize_values()

    @QtCore.pyqtSlot()
    def changed_image(self):
        self.update()

    @QtCore.pyqtSlot()
    def layers_order_changed(self):
        self.update()