import numpy as np


from core.layer.Layer import Layer

import utils


class LosslessLayer(Layer):

    def __init__(
            self,
            img: np.ndarray = None,
            visible: bool = True,
            position: tuple = (0, 0),
            name: str = 'Image'
        ):

        super().__init__(visible, position, name)

        self._orig_img = img # numpy rgba of original image
        self._transformed_img = self._init_transformed_img()
        self._transformed_img_q = utils.np_to_q_ptr(self._transformed_img)

    def get_layer(self):
        return self._transformed_img

    def get_layer_q(self):
        return self._transformed_img_q

    def _init_transformed_img(self):
        dst = utils.default_arr()
        center_src_y, center_src_x = self._orig_img.shape[0] // 2, self._orig_img.shape[1] // 2
        center_dst_y, center_dst_x = dst.shape[0] // 2, dst.shape[1] // 2

        start_dst_y = max(0, center_dst_y - center_src_y)
        start_dst_x = max(0, center_dst_x - center_src_x)

        h = min(self._orig_img.shape[0], dst.shape[0])
        w = min(self._orig_img.shape[1], dst.shape[1])

        start_src_y = max(0, center_src_y - center_dst_y)
        start_src_x = max(0, center_src_x - center_dst_x)

        dst[start_dst_y:start_dst_y + h, start_dst_x:start_dst_x + w] = (
            self._orig_img)[start_src_y:start_src_y + h, start_src_x:start_src_x + w]

        return dst

    def can_change(self) -> bool:
        return False