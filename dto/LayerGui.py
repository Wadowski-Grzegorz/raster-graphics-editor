from PyQt6.QtGui import QImage


class LayerGui:
    def __init__(self, idx: int, layer: QImage, visible: bool, position: tuple, name: str):
        self.idx = idx
        self.layer = layer
        self.visible = visible
        self.position = position
        self.name = name
