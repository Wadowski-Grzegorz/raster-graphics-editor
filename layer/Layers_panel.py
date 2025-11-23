from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QPushButton, QDockWidget, QWidget, QVBoxLayout, QHBoxLayout


class Layers_panel(QDockWidget):
    signal_layer_create_order = pyqtSignal()
    signal_layer_choose = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        dummy = QWidget()
        self.setWidget(dummy)
        self.setTitleBarWidget(QWidget())

        layout_main = QVBoxLayout(dummy)

        self.layout_options = QHBoxLayout()
        button_add = QPushButton('add layer')
        button_add.clicked.connect(self.signal_layer_create_order)
        self.layout_options.addWidget(button_add)
        layout_main.addLayout(self.layout_options)

        self.layout_menu = QVBoxLayout()
        layout_main.addLayout(self.layout_menu)

    def add_button_layer(self, idx: int):
        button = QPushButton(f'{idx}')
        button.clicked.connect(lambda _, i=idx: self.signal_layer_choose.emit(idx))
        self.layout_menu.addWidget(button)
        # print(f'added new button, idx: {idx}')

    @QtCore.pyqtSlot(QImage, int)
    def added_new_layer(self, i: QImage, idx: int):
        self.add_button_layer(idx)
