import numpy as np
import cv2 as cv

class BrushTip:
    def __init__(self, size=1, hardness=1, shape='circle'):
        self.size = size
        self.radius = size // 2 if size >= 2 else 1
        self.hardness = hardness
        self.shape = shape

        self.mask = self.make_mask()

    def make_mask(self):
        if self.shape != 'circle':
            return None
        radius = self.size / 2
        y, x = np.ogrid[:self.size, :self.size]
        dist = np.sqrt((x - radius) ** 2 + (y - radius) ** 2)

        normalized = np.clip(dist / radius, 0, 1)

        min_power = 1.5
        max_power = 8.0
        power = min_power + (max_power - min_power) * self.hardness
        falloff = normalized ** power

        mask = 255 * (1 - falloff)

        mask[dist > radius] = 0

        return mask.astype(np.uint8)

    def resize(self, size: int):
        self.size = size
        self.radius = size // 2 if size >= 2 else 1

        self.mask = self.make_mask()

    def set_hardness(self):
        self.hardness = self.hardness
        self.mask = self.make_mask()