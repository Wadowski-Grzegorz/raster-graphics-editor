import numpy as np


from core.layer.Layer import Layer

import utils


class LosslessLayer(Layer):

    def __init__(
            self,
            img: np.ndarray = None,
            visible: bool = True,
            position: tuple = (0, 0)
        ):

        super().__init__(visible, position)

        self._orig_img = img # numpy rgba of original image
        self._transformed_img = img.copy()
        self._transformed_img_q = utils.np_to_q_ptr(self._transformed_img)

    def get_layer(self):
        return self._transformed_img

    def get_layer_q(self):
        return self._transformed_img_q