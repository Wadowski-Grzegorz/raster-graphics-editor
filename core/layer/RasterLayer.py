import numpy as np

from core.layer.Layer import Layer
import utils
import resources.settings as settings


class RasterLayer(Layer):
    id_counter = 0
    def __init__(
            self,
            layer: np.ndarray = None,
            visible: bool = True,
            position: tuple = (0, 0),
            name: str = 'Canvas',
            idx: int = None,
        ):

        super().__init__(visible, position, name, idx)

        self._layer = self._init_layer(layer)

        self._qLayer = utils.np_to_q_ptr(self._layer) if self._layer is not None else None

    def _init_layer(self, layer):
        if layer is None:
            return utils.default_arr()
        else:
            def_h, def_w = settings.layer_height, settings.layer_width
            src_h, src_w = layer.shape[:2]
            h = max(src_h, def_h)
            w = max(src_w, def_w)
            new_layer = utils.arr(h, w)
            new_layer[:src_h, :src_w] = layer[:src_h, :src_w]
            return new_layer

    def get_layer(self):
        return self._layer

    def get_layer_q(self):
        return self._qLayer

    def refresh(self):
        self._qLayer = utils.np_to_q_ptr(self._layer)

    def adjust_size(self):
        h, w = self._layer.shape[:2]
        pos_x, pos_y = self._position

        needed_h = h + abs(pos_y)
        needed_w = w + abs(pos_x)

        if needed_h > h or needed_w > w:
            bigger_h = max(needed_h, h)
            bigger_w = max(needed_w, w)
            new_layer = np.zeros((bigger_h, bigger_w, 4), dtype=np.uint8)

            start_h, start_w = max(pos_y, 0), max(pos_x, 0)
            end_h, end_w = start_h + h, start_w + w
            new_layer[start_h:end_h, start_w:end_w, :] = self._layer

            self._layer = new_layer
            self._position = min(pos_x, 0), min(pos_y, 0)
            self.refresh()

    def get_cut_as(self, example):
        h, w = self.get_borders_as(example)
        return self._layer[h[0]: h[1], w[0]: w[1]]

    def get_borders_as(self, example):
        pos_x, pos_y = self._position
        ex_h, ex_w = example.shape[:2]

        start_h, start_w = abs(pos_y), abs(pos_x)
        return (start_h, start_h + ex_h), (start_w, start_w + ex_w)

    def replace(self, matrix):
        h, w = self.get_borders_as(matrix)
        if matrix.ndim == 2:
            self._layer[h[0]: h[1], w[0]: w[1], 3] = matrix
        if matrix.ndim == 3:
            self._layer[h[0]: h[1], w[0]: w[1], :3] = matrix

    def is_editable(self) -> bool:
        return True