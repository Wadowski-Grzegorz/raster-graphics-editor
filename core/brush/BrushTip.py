import numpy as np
import cv2 as cv

class BrushTip:
    def __init__(self, size=1, hardness=1):
        self.size = size
        self.radius = size // 2 if size >= 2 else 1
        self.hardness = hardness

        self.mask = self._make_mask()
        print(self.mask)

    def _make_mask(self):
        radius = self.size // 2
        y, x = np.ogrid[:self.size, :self.size]
        center = radius

        dist = np.sqrt((x - center) ** 2 + (y - center) ** 2)
        mask = np.clip((radius - dist) / radius, 0, 1)

        # nowy profil (wolno w środku, szybko na bokach)
        mask = mask ** max(self.hardness, 0.01)

        return (mask * 255).astype(np.uint8)

    def resize(self, size: int):
        self.size = size
        self.radius = size // 2 if size >= 2 else 1

        self.mask = self._make_mask()