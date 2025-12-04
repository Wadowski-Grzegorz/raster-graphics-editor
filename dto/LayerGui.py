from PyQt6.QtGui import QImage


class LayerGui:
    def __init__(self, layer: QImage, visible: bool, position: tuple):
        self.layer = layer
        self.visible = visible
        self.position = position
