import numpy as np

import utils

class Image:
    id_counter = 0
    def __init__(
            self,
            img: np.ndarray = None,
            position: tuple = (0, 0),
        ):

        super().__init__()

        self._image = img # numpy rgba
        self._width = self._image.shape[1]
        self._height = self._image.shape[0]

        self._qImage = utils.np_to_q_ptr(self._image)

        Image.id_counter += 1
        self._idx = self.id_counter

        self._position = position

    def get_qImage(self):
        return self._qImage

    def get_size(self):
        return self._width, self._height

    def get_position(self):
        return self._position