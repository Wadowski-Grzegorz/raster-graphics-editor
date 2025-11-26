import numpy as np


class Layers():

    def __init__(self):
        super().__init__()
        self._layers = {} # numpy images rgba
        self._temp_layer = None
        self._layers_order = [] # first in order - first to draw, saved as IDs
        self._idx = 0

        self.width = None
        self.height = None

    def create(self):
        # create new layer; emit QImage and index
        layer = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        self._idx += 1
        self._layers[self._idx] = layer
        self._layers_order.append(self._idx)
        return layer, self._idx

    def create_temp(self, width, height):
        self.width = width
        self.height = height

        layer = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        self._temp_layer = layer
        return self._temp_layer

    def get_layers(self):
        return self._layers

    def get_layers_size(self):
        return len(self._layers)

    def get_order(self):
        return self._layers_order.copy()

    def reorder(self, new_order: list):
        if len(new_order) != self.get_layers_size():
            return

        self._layers_order = new_order.copy()
