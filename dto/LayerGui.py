from PyQt6.QtGui import QImage
from dto.ObjectGui import ObjectGui


class LayerGui:
    def __init__(self, qLayer: QImage, visible: bool, objects: list[ObjectGui]):
        self.qLayer = qLayer
        self.visible = visible
        self.objects = objects
