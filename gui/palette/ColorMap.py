from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QImage, QPixmap, QPainter
from PyQt6.QtWidgets import QWidget


class ColorMap(QWidget):
    signal_color_changed = pyqtSignal(QColor)
    def __init__(self, hue=0, size_x=200, size_y=200):
        super().__init__()

        self._map = None
        self._hue = hue
        self.setFixedSize(size_x, size_y)

        self._cursor = (0, 0)
        self.create_map()

    def create_map(self):
        w, h = self.width(), self.height()
        image = QImage(w, h, QImage.Format.Format_RGB32)
        for x in range(w):
            for y in range(h):
                sat = int(x / (w - 1) * 255)
                val = int((h - y - 1) / (h - 1) * 255)
                image.setPixelColor(x, y, QColor.fromHsv(self._hue, sat, val))
        self._map = QPixmap.fromImage(image)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        if self._map:
            painter.drawPixmap(0, 0, self._map)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawEllipse(*self._cursor, 4, 4)

    def choose_color(self, pos_x, pos_y):
        w, h = self.width(), self.height()
        x = max(0, min(w - 1, int(pos_x)))
        y = max(0, min(h - 1, int(pos_y)))

        self._cursor = x, y
        sat = int(x / (w - 1) * 255)
        val = int((h - y - 1) / (h - 1) * 255)

        sel_color = QColor.fromHsv(self._hue, sat, val)
        self.signal_color_changed.emit(sel_color)
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.choose_color(e.position().x(), e.position().y())

    def mouseMoveEvent(self, e):
        self.choose_color(e.position().x(), e.position().y())

    def set_hue(self, hue: int):
        self._hue = hue
        self.create_map()
        self.choose_color(*self._cursor)
