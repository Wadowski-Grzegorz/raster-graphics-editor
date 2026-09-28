from PyQt6.QtCore import pyqtSignal, Qt, QRect, QPoint, QTime, QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QPixmap, QBrush, QPaintEvent, QRegion, QPainterPath, QPolygonF
from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem

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

        pixmap = QPixmap(settings.program_catalog + "\\resources\\icons\\tool_move.png")
        item = QGraphicsPixmapItem(pixmap)
        self._scene.addItem(item)

        pixmap = QPixmap(settings.program_catalog + "\\resources\\icons\\tool_hand.png")
        item = QGraphicsPixmapItem(pixmap)
        self._scene.addItem(item)

        # self._layers_dto = {} # { idx: qImage }
        self._layers = {} # {idx: QGraphicsPixmapItem}
        self._layers_order = []
        self._temp_layer = None # QImage
        self._temp_layer_item = None # QGraphicsPixmapItem
        self._current_idx = 0

        self._background = None
        self._foreground = None

        self._scale = 1

        self._offset_x = 0
        self._offset_y = 0

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
        self.update()

    # def paint(self, painter, paint_me, x, y, scaled_x, scaled_y):
    #     pixmap = (
    #         QPixmap
    #         .fromImage(paint_me)
    #         .scaled(
    #             scaled_x, scaled_y,
    #             Qt.AspectRatioMode.IgnoreAspectRatio,
    #             Qt.TransformationMode.SmoothTransformation
    #         )
    #     )
    #     painter.drawPixmap(x, y, pixmap)
    #
    # def paintEvent(self, e):
    #     painter = QPainter(self)
    #
    #     if self._background is None:
    #         self.create_background()
    #     painter.drawPixmap(0, 0, self._background)
    #
    #     layers = (self._layers_dto[i] for i in self._layers_order)
    #     for l in layers:
    #         if l.visible:
    #             self.paint(
    #                 painter,
    #                 l.layer,
    #                 self._offset_x + int(l.position[0] * self._scale),
    #                 self._offset_y + int(l.position[1] * self._scale),
    #                 int(l.layer.width() * self._scale),
    #                 int(l.layer.height() * self._scale)
    #             )
    #         if self._current_idx == l.idx:
    #             if self._temp_layer is not None:
    #                 self.paint(
    #                     painter,
    #                     self._temp_layer,
    #                     self._offset_x,
    #                     self._offset_y,
    #                     int(self._temp_layer.width() * self._scale),
    #                     int(self._temp_layer.height() * self._scale)
    #                 )
    #
    #     if self._foreground is None:
    #         self.create_foreground()
    #     painter.drawPixmap(0, 0, self._foreground)

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
            # self._scale *= 1.1
            self.scale(1.1, 1.1)
        else:
            # self._scale /= 1.1
            self.scale(0.9, 0.9)

        # self._scale = max(0.1, min(10.0, self._scale))
        # self.resize_values()
        #
        # self.request_update()

    # def resizeEvent(self, e):
    #     if settings.layer_width is not None and settings.layer_height is not None:
    #         self.resize_values()
    #
    #     self.request_update()
    #
    # def resize_values(self):
    #     self._offset_x = int((self.width() - settings.layer_width * self._scale) // 2)
    #     self._offset_y = int((self.height() - settings.layer_height * self._scale) // 2)
    #     self.create_foreground()
    #
    # def create_background(self):
    #     self._background = QPixmap(self.width(), self.height())
    #     self._background.fill(QColor(170, 170, 170))
    #

    def drawForeground(self, painter, rect):
        scene_rect = self._scene.sceneRect()

        color = QColor(50, 50, 50, 255)
        painter.save()
        painter.fillRect(QRectF(rect.topLeft(), scene_rect.bottomLeft()), color)
        painter.fillRect(QRectF(rect.bottomLeft(), scene_rect.bottomRight()), color)
        painter.fillRect(QRectF(scene_rect.topRight(), rect.bottomRight()), color)
        painter.fillRect(QRectF(scene_rect.topLeft(), rect.topRight()), color)
        painter.restore()

    # def create_foreground(self):
    #     self._foreground = QPixmap(self.width(), self.height())
    #     self._foreground.fill(QColor(0, 0, 0, 0))
    #
    #     painter = QPainter(self._foreground)
    #     color = QColor(50, 50, 50, 255)
    #
    #     # left, right, top, bottom
    #     painter.fillRect(QRect(
    #         QPoint(0, 0),
    #         QPoint(self._offset_x, self.height())),
    #         color
    #     )
    #     painter.fillRect(QRect(
    #         QPoint(self._offset_x + int(settings.layer_width * self._scale), 0),
    #         QPoint(self.width(), self.height())),
    #         color
    #     )
    #     painter.fillRect(QRect(
    #         QPoint(self._offset_x, 0),
    #         QPoint(self._offset_x + int(settings.layer_width * self._scale), self._offset_y)),
    #         color
    #     )
    #     painter.fillRect(QRect(
    #         QPoint(self._offset_x, self._offset_y + int(settings.layer_height * self._scale)),
    #         QPoint(self._offset_x + int(settings.layer_width * self._scale), self.height())),
    #         color
    #     )
    #
    #     painter.end()

    def convert_position_to_layer(self, position):
        # x = (position.x() - self._offset_x) / self._scale
        # y = (position.y() - self._offset_y) / self._scale
        # return x, y
        scene_pos = self.mapToScene(position.toPoint())
        return scene_pos.x(), scene_pos.y()


    # def move_offset(self, offset_x, offset_y):
    #     self._offset_x += offset_x
    #     self._offset_y += offset_y
    #     self.request_update()

    def set_controller(self, controller):
        self._controller = controller

    def layers_order_changed(self, data):
        self._layers_order = data['order']
        self.request_update()

    def layer_created(self, data):
        if self._controller is None:
            return
        layer = self._controller.convert_layer_gui(data['layer'])
        # self._layers_dto[layer.idx] = layer
        self._layers_order.append(layer.idx)

        pixmap = (
                    QPixmap
                    .fromImage(layer.layer)
                    # .scaled(
                    #     scaled_x, scaled_y,
                    #     Qt.AspectRatioMode.IgnoreAspectRatio,
                    #     Qt.TransformationMode.SmoothTransformation
                    # )
                )
        item = QGraphicsPixmapItem(pixmap)
        item.setZValue(self._layers_order.index(layer.idx))
        self._layers[layer.idx] = item
        self._scene.addItem(item)

        # self.request_update()

    def resize_scene(self):
        self._scene.setSceneRect(0, 0, settings.layer_width, settings.layer_height)

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
        # self.request_update()

    def layer_visibility_switched(self, data):
        idx = data['idx']
        # self._layers_dto[idx].visible = not self._layers_dto[idx].visible
        self.request_update()

    def layer_refresh(self, data):
        if self._controller is None:
            return
        layer = self._controller.convert_layer_gui(data['layer'])
        # self._layers_dto[layer.idx] = layer

        pixmap = QPixmap.fromImage(layer.layer)
        item = QGraphicsPixmapItem(pixmap)
        item.setOffset(*layer.position)
        item.setZValue(self._layers_order.index(layer.idx))

        self._scene.removeItem(self._layers[layer.idx])
        # add zValue
        self._layers[layer.idx] = item
        self._scene.addItem(item)
        # self.request_update()
        self.layer_temp_refresh()

    def layer_temp_refresh(self):
        if self._controller is None:
            return
        # layer = self._controller.convert_layer_gui(data['layer'])
        # self._layers_dto[layer.idx] = layer

        pixmap = QPixmap.fromImage(self._temp_layer)
        item = QGraphicsPixmapItem(pixmap)
        item.setZValue(1000)

        self._scene.removeItem(self._temp_layer_item)
        self._temp_layer_item = item
        self._scene.addItem(item)
        # self.request_update()

    def layer_current_idx_changed(self, data):
        self._current_idx = data['idx']
        self.request_update()