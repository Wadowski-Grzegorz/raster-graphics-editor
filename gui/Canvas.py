from PyQt6.QtCore import pyqtSignal, Qt, QTime, QTimer, QPointF
from PyQt6.QtGui import QColor, QPixmap, QBrush, QPainterPath
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem

from gui.EventListener import EventListener

from resources import settings

class Canvas(QGraphicsView, EventListener):
    signal_cursor_pressed = pyqtSignal(int, int)
    signal_cursor_moved = pyqtSignal(int, int, int, int)
    signal_cursor_released = pyqtSignal()
    signal_event_occurred = pyqtSignal(dict)

    MAX_FPS = 30
    MIN_INTERVAL = 1000 // MAX_FPS

    def __init__(self, event_provider):
        super().__init__()
        self._event_provider = event_provider
        self._controller = None

        self._scene = QGraphicsScene(self)
        self._scene.setBackgroundBrush(QBrush(QColor(170, 170, 170)))
        self.setScene(self._scene)

        self._layers = {} # {idx: QGraphicsPixmapItem}
        self._layers_order = []
        self._temp_layer = None # QImage
        self._temp_layer_item = None # QGraphicsPixmapItem
        self._current_idx = 0

        self._offset = QPointF(0, 0)

        self._old_x = None
        self._old_y = None

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._do_update)

        self.from_last_request = 0
        self.will_update = False

        self.event_types.update({
            'layer_created': self.layer_created,
            "layer_order_changed": self.layers_order_changed,
            "layer_visibility_switched": self.layer_visibility_switched,
            "layer_changed_type": self.layer_refresh,
            "layer_temp_created": self.layer_temp_created,
            "layer_current_idx_changed": self.layer_current_idx_changed,
            "paint_painted": self.layer_refresh,
            "paint_ended": self.layer_refresh
        })
        self.subscribe_to_events(self._event_provider, self.signal_event_occurred)

    def request_update(self):
        time = int(QTime.currentTime().msecsSinceStartOfDay())
        elapsed = time - self.from_last_request

        if elapsed >= self.MIN_INTERVAL:
            self._do_update()
            return

        if self.will_update:
            return

        delay = self.MIN_INTERVAL - elapsed
        self.will_update = True
        self.timer.start(delay)

    def _do_update(self):
        self.will_update = False
        self.from_last_request = int(QTime.currentTime().msecsSinceStartOfDay())
        self._scene.update()
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            x, y = (int(v) for v in self.convert_position_to_layer(e.position()))
            if 0 <= x < settings.layer_width and 0 <= y < settings.layer_height:

                self.signal_cursor_pressed.emit(x, y)

            self._old_x = x
            self._old_y = y

    def mouseMoveEvent(self, e):
        x, y = (int(v) for v in self.convert_position_to_layer(e.position()))
        if (
                0 <= x < settings.layer_width and 0 <= y < settings.layer_height and
                0 <= self._old_x < settings.layer_width and 0 <= self._old_y < settings.layer_height and
                ( abs(x - self._old_x) >= 1 or abs(y - self._old_y) >= 1 )
        ):
            self.signal_cursor_moved.emit(
                self._old_x, self._old_y,
                x, y
            )

        self._old_x = x
        self._old_y = y

    def mouseReleaseEvent(self, e):
        self.signal_cursor_released.emit()

    def wheelEvent(self, e):
        angle = e.angleDelta().y()
        if angle > 0:
            self.scale(1.02, 1.02)
        else:
            self.scale(0.98, 0.98)

    def drawForeground(self, painter, rect):
        scene_rect = self._scene.sceneRect()
        scene_rect.translate(self._offset)

        painter.save()
        path = QPainterPath()
        path.setFillRule(Qt.FillRule.OddEvenFill)
        path.addRect(rect)
        path.addRect(scene_rect)
        painter.fillPath(path, QColor(50, 50, 50, 255))
        painter.restore()

    def convert_position_to_layer(self, position):
        scene_pos = self.mapToScene(position.toPoint())
        scene_pos -= self._offset
        return scene_pos.x(), scene_pos.y()

    def move_offset(self, offset_x, offset_y):
        self._offset += QPointF(offset_x, offset_y)
        for i in self._scene.items():
            i.moveBy(offset_x, offset_y)
        self.request_update()

    def set_controller(self, controller):
        self._controller = controller

    def layers_order_changed(self, data):
        self._layers_order = data['order']
        for i, idx in enumerate(self._layers_order):
            self._layers[idx].setZValue(i)

    def layer_created(self, data):
        if self._controller is None:
            return

        layer = self._controller.convert_layer_gui(data['layer'])
        self._layers_order.append(layer.idx)

        pixmap = QPixmap.fromImage(layer.layer)
        item = QGraphicsPixmapItem(pixmap)
        item.setZValue(self._layers_order.index(layer.idx))
        self._layers[layer.idx] = item
        self._scene.addItem(item)

    def resize_scene(self):
        self._scene.setSceneRect(
            0, 0,
            settings.layer_width, settings.layer_height)

    def layer_temp_created(self, data):
        if self._controller is None:
            return
        layer = self._controller.convert_layer_gui(data['layer'])
        self._temp_layer = layer.layer

        pixmap = QPixmap.fromImage(self._temp_layer)
        item = QGraphicsPixmapItem(pixmap)
        item.setZValue(100000)
        self._temp_layer_item = item
        self._scene.addItem(item)

        self.resize_scene()

    def layer_visibility_switched(self, data):
        idx = data['idx']
        self._layers[idx].setVisible(not self._layers[idx].isVisible())

    def layer_refresh(self, data):
        if self._controller is None:
            return
        layer = self._controller.convert_layer_gui(data['layer'])

        pixmap = QPixmap.fromImage(layer.layer)
        item = QGraphicsPixmapItem(pixmap)
        item.setOffset(layer.position[0] + self._offset.x(), layer.position[1] + self._offset.y())
        item.setZValue(self._layers_order.index(layer.idx))
        item.setVisible(layer.visible)

        self._scene.removeItem(self._layers[layer.idx])
        self._layers[layer.idx] = item
        self._scene.addItem(item)
        self.layer_temp_refresh()

    def layer_temp_refresh(self):
        if self._controller is None:
            return

        pixmap = QPixmap.fromImage(self._temp_layer)
        item = QGraphicsPixmapItem(pixmap)
        item.setOffset(self._offset.x(), self._offset.y())
        item.setZValue(self._layers[self._current_idx].zValue() + 0.5)

        self._scene.removeItem(self._temp_layer_item)
        self._temp_layer_item = item
        self._scene.addItem(item)

    def layer_current_idx_changed(self, data):
        self._current_idx = data['idx']
        if self._current_idx in self._layers:
            zValue = self._layers[self._current_idx].zValue()
            self._temp_layer_item.setZValue(zValue+0.5)