import numpy as np
from data.Image import Image

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
        self._visible = visible
        self._images = images # Images in order

    def add_image(self, image: Image):
        self._images.append(image)

    def get_id(self) -> int:
        return self._idx

    def get_layer(self):
        return self._layer