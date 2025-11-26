import numpy as np
import cv2 as cv

class BrushTip():
    def __init__(self, size=1, hardness=1):
        self.size = size
        self.radius = size // 2 if size >= 2 else 1
        self.hardness = hardness

        self.mask = np.zeros((self.size, self.size), np.uint8)
        radius = self.size // 2
        cv.circle(self.mask, (radius, radius), radius, 255, -1)

    def resize(self, size: int):
        self.size = size
        self.radius = size // 2 if size >= 2 else 1

        self.mask = np.zeros((self.size, self.size), np.uint8)
        radius = self.size // 2
        cv.circle(self.mask, (radius, radius), radius, 255, -1)