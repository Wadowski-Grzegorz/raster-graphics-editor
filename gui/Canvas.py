import random

import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtGui import QPainter, QColor, QPixmap
from PyQt6.QtWidgets import QWidget
from core.layer.LayerManager import layer_manager
from adapters.LayerAdapter import layer_adapter

import utils
from resources import settings


class Canvas(QWidget):
    signal_cursor_pressed = QtCore.pyqtSignal(int, int)
    signal_cursor_moved = QtCore.pyqtSignal(int, int, int, int)
    signal_cursor_released = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self._layers_dto = None
        self._temp_layer = None # QImage
        self._background = None
        self._foreground = None

        self._scale = 1

        self._offset_x = 0
        self._offset_y = 0

        self._old_x = None
        self._old_y = None

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
        self._layers_dto = layer_adapter.layers_to_dto(layer_manager.get_layers())

        if self._background is None:
            self.create_background()
        painter.drawPixmap(0, 0, self._background)

        for idx in layer_manager.get_order():
            layer_dto = self._layers_dto[idx]
            # layer_dto.layer.save(f'aaaa.png')
            self.paint(
                painter,
                layer_dto.layer,
                self._offset_x + layer_dto.position[0],
                self._offset_y + layer_dto.position[1],
                int(layer_dto.layer.width() * self._scale),
                int(layer_dto.layer.height() * self._scale)
            )

        if self._temp_layer is not None:
            self.paint(
                painter,
                self._temp_layer,
                self._offset_x,
                self._offset_y,
                int(self._temp_layer.width() * self._scale),
                int(self._temp_layer.height() * self._scale)
            )

        if self._foreground is None:
            self.create_foreground()
        painter.drawPixmap(0, 0, self._foreground)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            x, y = (int(v) for v in self.convert_to_layer(e.position()))

            if 0 <= x < settings.layer_width and 0 <= y < settings.layer_height:

                self.signal_cursor_pressed.emit(x, y)

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

            self.signal_cursor_moved.emit(
                self._old_x, self._old_y,
                x, y
            )

            self.update()

        self._old_x = x
        self._old_y = y

    def mouseReleaseEvent(self, e):
        self.signal_cursor_released.emit()
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

    def resize_values(self):
        self._offset_x = int((self.width() - settings.layer_width * self._scale) // 2)
        self._offset_y = int((self.height() - settings.layer_height * self._scale) // 2)
        self.create_foreground()

    def create_background(self):
        self._background = QPixmap(self.width(), self.height())
        self._background.fill(QColor(170, 170, 170))

    def create_foreground(self):
        self._foreground = QPixmap(self.width(), self.height())
        self._foreground.fill(QColor(0, 0, 0, 0))

        painter = QPainter(self._foreground)
        color = QColor(50, 50, 50, 255)

        # left, right, top, bottom
        painter.fillRect(QRect(
            QPoint(0, 0),
            QPoint(self._offset_x, self.height())),
            color
        )
        painter.fillRect(QRect(
     QPoint(self._offset_x + settings.layer_width * self._scale, 0),
            QPoint(self.width(), self.height())),
            color
        )
        painter.fillRect(QRect(
     QPoint(self._offset_x, 0),
            QPoint(self._offset_x + settings.layer_width * self._scale, self._offset_y)),
            color
        )
        painter.fillRect(QRect(
            QPoint(self._offset_x, self._offset_y + settings.layer_height * self._scale),
            QPoint(self._offset_x + settings.layer_width * self._scale, self.height())),
            color
        )

        painter.end()

    def convert_to_layer(self, position):
        x = (position.x() - self._offset_x) / self._scale
        y = (position.y() - self._offset_y) / self._scale
        return x, y

    @QtCore.pyqtSlot()
    def refresh_data(self):
        self._layers_dto = layer_adapter.layers_to_dto(layer_manager.get_layers())
        self.update()

    @QtCore.pyqtSlot(np.ndarray)
    def added_temp_layer(self, layer: np.ndarray):
        self._temp_layer = utils.np_to_q_ptr(layer)
        self.resize_values()

    @QtCore.pyqtSlot()
    def changed_image(self):
        self.update()

    @QtCore.pyqtSlot()
    def layers_order_changed(self):
        self.update()

    def move_offset(self, offset_x, offset_y):
        self._offset_x += offset_x
        self._offset_y += offset_y