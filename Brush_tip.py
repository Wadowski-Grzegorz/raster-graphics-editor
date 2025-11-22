import numpy as np
import cv2 as cv

class Brush_tip():
    def __init__(self, size=1, hardness=1):
        self.size = size
        self.hardness = hardness

        radius = self.size // 2
        self.mask = np.zeros((self.size, self.size), np.uint8)
        cv.circle(self.mask, (radius, radius), radius, 150, -1)


