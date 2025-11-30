import cv2 as cv

class Image:
    id_counter = 0
    def __init__(
            self,
            # image: np.ndarray = None,
            file_path: str = None,
            visible: bool = True,
            position: tuple = (0, 0),
        ):

        super().__init__()

        image = cv.imRead(file_path) # for now it can be rgb or rgba
        if image is None:
            raise FileNotFoundError
        self._image = image # numpy rgba
        self._size = self._image.shape[:2] if self._image else (0, 0)   # height, width

        Image.id_counter += 1
        self._idx = self.id_counter

        self._visible = visible

        self._position = position # Images in order

