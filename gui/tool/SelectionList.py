from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QComboBox


class SelectionList(QComboBox):
    signal_selected = pyqtSignal()

    def __init__(self, options: list, on_select=None):
        super().__init__()

        for icon, text, data in options:
            icon = QIcon(icon)
            self.addItem(icon, text, data)




    # def currentTextChanged(self):
    #     self.signal_selected.emit()