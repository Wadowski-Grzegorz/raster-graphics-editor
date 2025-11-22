import numpy as np
import cv2 as cv
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from Brush import Brush

class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.currImage = None
        self.layers = {} # { idx: [QImage, npImage] }

        self.old_x = None
        self.old_y = None

        self.curr_brush = Brush(size=100)
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

    def paintMasking(self, x, y, img_x, img_y, brush_radius, brush_color):
        img_y_s, img_y_e = max(y - brush_radius, 0), min(y + brush_radius, img_y)
        img_x_s, img_x_e = max(x - brush_radius, 0), min(x + brush_radius, img_x)

        # cut a peace of image which user will paint with a brush
        paint_image = self.currImage[img_y_s:img_y_e, img_x_s:img_x_e].astype(np.float32)

        # values 0-255 --> 0-1
        mask = self.curr_brush.get_mask().astype(np.float32) / 255.

        mask_y_s = max(brush_radius - y, 0)
        mask_y_e = mask_y_s + img_y_e - img_y_s
        mask_x_s = max(brush_radius - x, 0)
        mask_x_e = mask_x_s + img_x_e - img_x_s

        # mask is [a, b] while image is [a, b, 4], so resize with None
        mask = mask[mask_y_s:mask_y_e, mask_x_s:mask_x_e, None]
        paint_image = paint_image * (1 - mask) + brush_color * mask

        self.currImage[img_y_s:img_y_e, img_x_s:img_x_e] = paint_image.astype(np.uint8)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            x, y = int(e.position().x()), int(e.position().y())
            img_y, img_x = self.currImage.shape[:2]

            if 0 <= x < img_x and 0 <= y < img_y:
                color = (*self.curr_color, 255)
                brush_color = np.array(color, dtype=np.uint8)

                brush_size = self.curr_brush.get_size()
                brush_radius = brush_size // 2

                self.paintMasking(x, y, img_x, img_y, brush_radius, brush_color)

                self.update()

            self.old_x = x
            self.old_y = y

    def mouseMoveEvent(self, e):
        x, y = int(e.position().x()), int(e.position().y())
        img_y, img_x = self.currImage.shape[:2]
        if (0 <= x < img_x and 0 <= y < img_y and
                0 <= self.old_x < img_x and 0 <= self.old_y < img_y):

            # ----- calculating pixel position -----
            # check which value has more to grow
            dx = abs(x - self.old_x)
            dy = abs(y - self.old_y)

            # steps - how many pixel to color
            steps = dx if dx >= dy else dy
            step_x = dx / steps if x >= self.old_x else -dx / steps
            step_y = dy / steps if y >= self.old_y else -dy / steps

            # ----- prepare brush -----
            color = (*self.curr_color, 255)
            brush_color = np.array(color, dtype=np.uint8)

            brush_size = self.curr_brush.get_size()
            brush_radius = brush_size // 2

            # ----- paint -----
            a, b = self.old_x, self.old_y
            for _ in range(steps):
                self.paintMasking(int(a), int(b), img_x, img_y, brush_radius, brush_color)

                a += step_x
                b += step_y

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