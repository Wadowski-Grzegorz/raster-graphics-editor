from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPushButton, QHBoxLayout


#BGR
COLORS = {
    (255, 0, 0): 'blue',
    (0, 255, 0): 'green',
    (0, 0, 255): 'red',
    (0, 0, 0): 'black',
    (255, 255, 255): 'white',
}

class Palette(QHBoxLayout):
    color_signal = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()

        for value, color in COLORS.items():
            button = QPushButton()

            b, g, r = value
            button.setStyleSheet(f"background-color:rgb{(r, g, b)};")

            button.clicked.connect(lambda _, v=value: self.color_signal.emit(v))
            self.addWidget(button)