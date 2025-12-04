from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget
from resources import settings


class Starting_window(QWidget):
    signal_layer_temp_create_order = pyqtSignal()

    def __init__(self):
        super().__init__()

    def do(self):
        settings.layer_width = 1000
        settings.layer_height = 800

        self.signal_layer_temp_create_order.emit()

