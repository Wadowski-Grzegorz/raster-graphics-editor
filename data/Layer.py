import numpy as np

from data.Image import Image
import utils


class Layer:
    id_counter = 0
    def __init__(
            self,
            layer: np.ndarray = None,
            visible: bool = True,
            images: list = None
        ):

        super().__init__()

        Layer.id_counter += 1
        self._idx = self.id_counter
        self._layer = layer # numpy rgba
        self._qLayer = utils.np_to_q_ptr(self._layer) if layer is not None else None
        self._visible = visible
        self._images = [] if images is None else images # Images in order


    def add_image(self, image: Image):
        self._images.append(image)

    def get_id(self) -> int:
        return self._idx

    def get_layer(self):
        return self._layer

    def get_images(self):
        return self._images

    def get_qLayer(self):
        return self._qLayer

    def get_visible(self):
        return self._visible