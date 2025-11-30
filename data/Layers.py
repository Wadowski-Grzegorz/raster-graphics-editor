import numpy as np
import globals
from data.Layer import Layer

class Layers:

    def __init__(self):
        super().__init__()
        self._layers = {} # numpy images rgba
        self._temp_layer = None
        self._layers_order = [] # first in order - first to draw, saved as IDs

    def create(self):
        layer = Layer(np.zeros((globals.layer['height'], globals.layer['width'], 4), dtype=np.uint8))
        idx = layer.get_id()
        self._layers[idx] = layer
        self._layers_order.append(idx)
        return layer.get_layer(), idx

    def create_temp(self, width, height):
        layer = np.zeros((globals.layer['height'], globals.layer['width'], 4), dtype=np.uint8)
        self._temp_layer = layer
        return self._temp_layer

    def get_layers_size(self):
        return len(self._layers)

    def get_order(self):
        return self._layers_order.copy()

    def reorder(self, new_order: list):
        if len(new_order) != self.get_layers_size():
            return

        self._layers_order = new_order.copy()
