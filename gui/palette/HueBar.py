from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QImage, QColor, QPainter
from PyQt6.QtWidgets import QWidget


class HueBar(QWidget):
    signal_hue_changed = pyqtSignal(int)

    def __init__(self, size_x=15, size_y=150):
        super().__init__()

        self.setFixedSize(size_x, size_y)

        self._bar = None
        self._cursor_y = 0
        self.create_bar()

    def create_bar(self):
        w, h = self.width(), self.height()
        image = QImage(w, h, QImage.Format.Format_RGB32)
        painter = QPainter(image)
        for y in range(h):
            line_h = y / (h - 1)
            color = QColor.fromHsvF(line_h, 1.0, 1.0)
            painter.setPen(color)
            painter.drawLine(0, y, w, y)
        painter.end()

        self._bar = image

    def paintEvent(self, e):
        painter = QPainter(self)
        if self._bar:
            painter.drawImage(0, 0, self._bar)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawLine(0, self._cursor_y, self._bar.width(), self._cursor_y)

    def choose_hue(self, position):
        h = self.height()
        y = int(max(0, min(h - 1, position.y())))
        self._cursor_y = y

        hue = int(y / (h - 1) * 359)
        self.signal_hue_changed.emit(hue)
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.choose_hue(e.position())

    def mouseMoveEvent(self, e):
        self.choose_hue(e.position())
