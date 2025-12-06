from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from dto.SelectableItem import SelectableItem
from gui.components.Tile import Tile


class SelectionMenu(QListWidget):
    def __init__(self, items: list[SelectableItem], select_fun=None):
        super().__init__()
        self.select_fun = select_fun

        for it in items:
            Tile(it.idx, name=it.name, icon=it.icon)
