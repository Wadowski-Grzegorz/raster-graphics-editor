import numpy as np
import cv2
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.currImage = None
        self.layers = {} # { idx: [QImage, npImage] }

        self.old_x = None
        self.old_y = None

        self.curr_color = (0, 0, 0)
        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # self.setStyleSheet("background-color:rgb(55,55,55);")
        # print(f'canvas: {self.width()}, {self.height()}')


    def paintEvent(self, e):
        painter = QPainter(self)
        # print(f'canvas: {self.width()}, {self.height()}')
        for image, npImage in self.layers.values():
            # print(f'painting image is: {id(i)}')
            painter.drawImage(0, 0, image)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            x, y = int(e.position().x()), int(e.position().y())
            self.old_x = x
            self.old_y = y
            if 0 <= x < self.currImage.shape[1] and 0 <= y < self.currImage.shape[0]:
                self.currImage[y, x] = [0, 0, 0, 255]
                self.update()

    def mouseMoveEvent(self, e):
        # get position and check if there are in image
        # print(f'{self.size()} canvas0')
        b, g, r = self.curr_color
        brush = (b, g, r, 255)
        x, y = int(e.position().x()), int(e.position().y())
        if (0 <= x < self.currImage.shape[1] and 0 <= y < self.currImage.shape[0] and
                0 <= self.old_x < self.currImage.shape[1] and 0 <= self.old_y < self.currImage.shape[0]):

            cv2.line(self.currImage, (self.old_x, self.old_y), (x, y), brush, 1)
            # self.currImage[..., 3] = 255

            self.old_x = x
            self.old_y = y
            self.update()

        self.old_x = x
        self.old_y = y

    def setColor(self, color: tuple):
        self.curr_color = color

    def set_curr_image(self, idx: int):
        self.currImage = self.layers[idx][1]

    def add_image(self, image: QImage, idx: int):
        ptr = image.bits()
        ptr.setsize(image.width() * image.height() * 4)
        npImage = np.frombuffer(ptr, np.uint8).reshape((image.height(), image.width(), 4))
        self.layers[idx] = [image, npImage]

        self.set_curr_image(idx)
        self.update()

    @QtCore.pyqtSlot(QImage, int)
    def added_new_image(self, image: QImage, idx: int):
        self.add_image(image, idx)

    @QtCore.pyqtSlot(int)
    def changed_image(self, idx: int):
        # print(f'changed image idx: {idx}')
        self.set_curr_image(idx)
        self.update()