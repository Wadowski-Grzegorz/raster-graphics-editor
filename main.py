import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget, QPushButton, QLabel
from Canvas import Canvas
from Palette import Palette
from Layers_panel import Layers_panel
from Layers import Layers
from Controller import Controller

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('pre-app')
        # self.resize(800, 600)
        # print(f'{self.size()} main')

        layout = QVBoxLayout()

        layers = Layers()
        self.controller = Controller(layers)

        self.canvas = Canvas()
        layout.addWidget(self.canvas)


        self.palette = Palette()
        self.palette.color_signal.connect(self.canvas.setColor)
        layout.addLayout(self.palette)

        self.layers_panel = Layers_panel()
        self.layers_panel.signal_layer_create_order.connect(self.controller.layer_create)
        self.controller.signal_layer_created.connect(self.layers_panel.added_new_layer)
        self.layers_panel.signal_layer_choose.connect(self.controller.idx_chosen)
        self.controller.signal_idx_changed.connect(self.canvas.changed_image)
        self.controller.signal_layer_created.connect(self.canvas.added_new_image)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.layers_panel)


        dummy = QWidget()
        dummy.setLayout(layout)

        self.setCentralWidget(dummy)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    app.exec()