import numpy as np
import cv2 as cv

from data.Image import Image
from data.Layer import Layer

import settings

class DataCenter:

    def __init__(self):
        super().__init__()
        self._layers = {} # id : layer
        self._temp_layer = None
        self._layers_order = [] # first in order - first to draw, saved as IDs
        self._current_idx = None

    def create(self):
        layer = Layer(np.zeros((settings.layer_height, settings.layer_width, 4), dtype=np.uint8))
        idx = layer.get_id()
        self._layers[idx] = layer
        self._layers_order.append(idx)
        self.set_current_idx(idx)
        return layer.get_layer(), idx

    def create_temp(self):
        layer = np.zeros((settings.layer_height, settings.layer_width, 4), dtype=np.uint8)
        self._temp_layer = layer
        return self._temp_layer

    def get_layers_size(self):
        return len(self._layers)

    def get_order(self):
        return self._layers_order.copy()

    def set_current_idx(self, idx):
        self._current_idx = idx

    def get_idx(self):
        return self._current_idx

    def reorder(self, new_order: list):
        if len(new_order) != self.get_layers_size():
            return

        self._layers_order = new_order.copy()

    def add_image(self, file_path: str):
        img_file = cv.imread(file_path, cv.IMREAD_UNCHANGED)
        if img_file is None:
            raise FileNotFoundError

        if img_file.shape[2] == 3:
            img_file = cv.cvtColor(img_file, cv.COLOR_BGR2RGBA)
        elif img_file.shape[2] == 4:
            img_file = cv.cvtColor(img_file, cv.COLOR_BGRA2RGBA)

        img = Image(img_file)
        self._layers[self._current_idx].add_image(img)

    def get_layers(self):
        return list(self._layers.values())

data_center = DataCenter()