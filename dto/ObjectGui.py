from PyQt6.QtGui import QImage


class ObjectGui:
    def __init__(self, qImage: QImage, size: tuple[int, int], position: tuple[int, int]):
        self.qImage = qImage
        self.size = size
        self.position = position
