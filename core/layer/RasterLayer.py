import numpy as np

from core.layer.Layer import Layer
import utils


class RasterLayer(Layer):
    id_counter = 0
    def __init__(
            self,
            layer: np.ndarray = None,
            visible: bool = True,
            position: tuple = (0, 0)
        ):

        super().__init__(visible, position)

        if layer is None:
            self._layer = utils.default_arr()
        else:
            self._layer = layer

        self._qLayer = utils.np_to_q_ptr(self._layer) if self._layer is not None else None

    def get_layer(self):
        return self._layer

    def get_layer_q(self):
        return self._qLayer
