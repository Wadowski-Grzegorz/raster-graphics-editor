from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPushButton, QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
import numpy as np

from gui.components.Tile import Tile
from core.layer.LayerManager import layer_manager


class LayersPanel(QDockWidget):
    signal_layer_create_order = pyqtSignal()
    signal_layer_choose = pyqtSignal(int)
    signal_layer_reorder_order = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        dummy = QWidget()
        self.setWidget(dummy)
        self.setTitleBarWidget(QWidget())

        layout_main = QVBoxLayout(dummy)

        # button for adding new layer
        self.layout_options = QHBoxLayout()
        button_add = QPushButton('Add Layer')
        button_add.clicked.connect(self.signal_layer_create_order)
        self.layout_options.addWidget(button_add)
        layout_main.addLayout(self.layout_options)

        # layers
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.list_widget.currentRowChanged.connect(self.layer_choose)
        self.list_widget.model().rowsMoved.connect(self.layers_moved)
        layout_main.addWidget(self.list_widget)

    def add_button_layer(self, idx: int, layer_tile=None):
        item = QListWidgetItem()
        tile = Tile(idx, name=f'Layer {idx}', show_name=True) if layer_tile is None else layer_tile
        item.setSizeHint(tile.sizeHint())

        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, tile)

    @QtCore.pyqtSlot(np.ndarray, int)
    def added_new_layer(self, idx: int):
        self.add_button_layer(idx)

    def layers_moved(self, parent, start, end, destination, row):
        new_order = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            new_order.append(widget.get_id())

        self.signal_layer_reorder_order.emit(new_order)

    def layer_choose(self, element_num: int):
        if element_num < 0:
            return
        item = self.list_widget.item(element_num)
        widget = self.list_widget.itemWidget(item)
        self.signal_layer_choose.emit(widget.get_id())


    def set_layers_order(self, new_order: list):
        tiles = {}
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            tile = self.list_widget.itemWidget(item)
            tiles[tile.get_id()] = tile.get_name()

        self.list_widget.clear()

        for idx in new_order:
            tile = Tile(idx, tiles[idx])
            self.add_button_layer(idx, name=tile, show_name=True)

    @QtCore.pyqtSlot()
    def layers_order_changed(self):
        new_order = layer_manager.get_order()
        self.set_layers_order(new_order)

