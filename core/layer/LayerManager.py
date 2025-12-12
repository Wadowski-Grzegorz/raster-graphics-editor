import numpy as np
import cv2 as cv

import utils
from core.layer.Layer import Layer
from core.layer.RasterLayer import RasterLayer
from core.layer.LosslessLayer import LosslessLayer

from resources import settings


class LayerManager:

    def __init__(self):
        super().__init__()

        self._layers = {} # id : layer
        self._layers_order = [] # first in order - first to draw, saved as IDs
        self._current_idx = None

        self._temp_layer = None

    def create_empty(self):
        layer = RasterLayer()
        self.append_layer(layer)
        return layer.get_id()

    def add_image(self, file_path: str):
        img_file = cv.imread(file_path, cv.IMREAD_UNCHANGED)
        if img_file is None:
            raise FileNotFoundError

        if img_file.shape[2] == 3:
            img_file = cv.cvtColor(img_file, cv.COLOR_BGR2RGBA)
        elif img_file.shape[2] == 4:
            img_file = cv.cvtColor(img_file, cv.COLOR_BGRA2RGBA)

        img = LosslessLayer(img_file)
        self.append_layer(img)
        return img.get_id()

    def append_layer(self, layer: Layer):
        idx = layer.get_id()
        self._layers[idx] = layer
        self._layers_order.append(idx)
        self.set_current_idx(idx)

    def create_temp(self):
        layer = utils.default_arr()
        self._temp_layer = layer
        return self._temp_layer

    def get_layers_len(self):
        return len(self._layers)

    def get_order(self):
        return self._layers_order.copy()

    def set_current_idx(self, idx):
        self._current_idx = idx

    def get_current_idx(self):
        return self._current_idx

    def get_idx(self):
        return self._current_idx

    def reorder(self, new_order: list):
        if len(new_order) != self.get_layers_len():
            return

        self._layers_order = new_order.copy()

    def get_layers(self):
        return list(self._layers.values())

    def get_layers_arr(self):
        return {idx: l.get_layer() for idx, l in self._layers.items()}

    def get_temp_layer(self):
        return self._temp_layer

    def get_current_layer(self):
        return self._layers[self._current_idx]

    def get_layer(self, idx: int):
        return self._layers[idx]

    def switch_visibility(self, idx: int):
        self._layers[idx].switch_visible()

    def convert_to_editable(self, idx: int):
        l = self._layers[idx]
        if l and not l.is_editable():
            new_layer = RasterLayer(
                idx = l.get_id(),
                layer = l.get_layer(),
                position = l.get_position(),
                name = l.get_name(),
                visible= l.get_visible(),
            )
            self._layers[idx] = new_layer

    def set_name(self, idx: int, name: str):
        if self._layers[idx]:
            self._layers[idx].set_name(name)





layer_manager = LayerManager()