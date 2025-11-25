from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget


class Starting_window(QWidget):
    signal_layer_temp_create_order = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

    def do(self):
        self.signal_layer_temp_create_order.emit(1000, 800)

