from PyQt6.QtGui import QIcon


class SelectableItem:
    def __init__(self, idx: int, name: str, icon: QIcon):
        self.idx = idx
        self.name = name
        self.icon = icon