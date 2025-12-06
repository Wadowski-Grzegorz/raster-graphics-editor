from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QComboBox

from dto.SelectableItem import SelectableItem


class SelectionList(QComboBox):
    def __init__(self, items: list[SelectableItem], select_fun=None):
        super().__init__()
        self.select_fun = select_fun

        for it in items:
            self.addItem(it.icon, it.name, it.idx)

        self.currentIndexChanged.connect(self.selected)

    @pyqtSlot(int)
    def selected(self, idx):
        real_idx = self.itemData(idx)
        self.select_fun(real_idx)