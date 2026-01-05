import numpy as np


from core.layer.Layer import Layer

import utils
import resources.settings as settings


class LosslessLayer(Layer):

    def __init__(
            self,
            img: np.ndarray = None,
            visible: bool = True,
            position: tuple = (0, 0),
            name: str = 'Image',
            idx: int = None,
        ):

        super().__init__(visible, position, name, idx)

        self._orig_img = img # numpy rgba of original image
        self._transformed_img = None
        self._scale = (1.0, 1.0)

        self._init_transformed_img()

    def get_layer(self):
        return self._transformed_img

    def get_orig(self):
        return self._orig_img

    def transform_by(self, scale_x, scale_y):
        self._scale = (self._scale[0] * scale_x, self._scale[1] * scale_y)
        return self._scale

    def set_layer(self, resized):
        self._transformed_img = resized

    def _init_transformed_img(self):
        if self._orig_img is None:
            return
        dst = self._orig_img.copy()
        half_global_w, half_global_h = settings.layer_width // 2, settings.layer_height // 2
        half_dst_w, half_dst_h = dst.shape[1] // 2, dst.shape[0] // 2

        self.set_position(half_global_w - half_dst_w, half_global_h - half_dst_h)
        self._transformed_img = dst

    def is_editable(self) -> bool:
        return False