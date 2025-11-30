from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget
import globals

class Starting_window(QWidget):
    signal_layer_temp_create_order = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

    def do(self):
        globals.layer = {
            'width': 1000,
            'height': 800,
        }
        self.signal_layer_temp_create_order.emit(
            globals.layer['width'],
            globals.layer['height']
        )

