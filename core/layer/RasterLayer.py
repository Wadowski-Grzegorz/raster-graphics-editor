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

    # def adjust_size(self, th, tw):
    #     h, w = self._layer.shape[:2]
    #     pos_x, pos_y = self._position
    #
    #     needed_h = h + abs(pos_y)
    #     needed_w = w + abs(pos_x)
    #
    #     if needed_h > h or needed_w > w:
    #         bigger_h = max(needed_h, h)
    #         bigger_w = max(needed_w, w)
    #         new_layer = np.zeros((bigger_h, bigger_w, 4), dtype=np.uint8)
    #
    #         start_h, start_w = max(pos_y, 0), max(pos_x, 0)
    #         end_h, end_w = start_h + h, start_w + w
    #         new_layer[start_h:end_h, start_w:end_w, :] = self._layer
    #
    #         self._layer = new_layer
    #         self._position = min(pos_x, 0), min(pos_y, 0)

    def adjust_size(self):
        h, w = self._layer.shape[:2]
        pos_x, pos_y = self._position

        needed_h = max(h, settings.layer_height - min(pos_y, 0))
        needed_w = max(w, settings.layer_width - min(pos_x, 0))

        if needed_h > h or needed_w > w:
            new_layer = utils.arr(needed_h, needed_w)

            start_h, start_w = max(pos_y, 0), max(pos_x, 0)
            end_h, end_w = start_h + h, start_w + w
            new_layer[start_h:end_h, start_w:end_w, :] = self._layer

            self._layer = new_layer
            self._position = min(pos_x, 0), min(pos_y, 0)

    def is_editable(self) -> bool:
        return True

    def set_layer(self, resized):
        self._layer = resized