from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from dto.SelectableItem import SelectableItem
from gui.components.Tile import Tile


class SelectionMenu(QListWidget):
    def __init__(self, items: list[SelectableItem], select_fun=None, identify='id'):
        super().__init__()
        self._select_fun = select_fun
        self._identify = identify

        for it in items:
            tile = Tile(it.idx, name=it.name, icon=it.icon, show_name=False)

            item = QListWidgetItem()
            item.setSizeHint(tile.sizeHint())

            self.addItem(item)
            self.setItemWidget(item, tile)

        self.currentItemChanged.connect(self.selected)

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def selected(self, current: QListWidgetItem, previous: QListWidgetItem):
        widget = self.itemWidget(current)
        if self._identify == 'id':
            self._select_fun(widget.get_idx())

        elif self._identify == 'name':
            self._select_fun(widget.get_name())

    def set_current_row(self, name):
        for row in range(self.count()):
            it = self.item(row)
            widget = self.itemWidget(it)
            if widget.get_name().lower() == name.lower():
                self.setCurrentRow(row)
                break