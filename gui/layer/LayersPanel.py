from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QPushButton, QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, \
    QToolButton, QLineEdit

from gui.components.Container import Container
from gui.components.EditableName import EditableName
from adapters.LayerAdapter import layer_adapter

import resources.settings as settings


class LayersPanel(QDockWidget):
    signal_layer_create_order = pyqtSignal()
    signal_layer_choose = pyqtSignal(int)
    signal_layer_reorder_order = pyqtSignal(list)
    signal_layer_visibility_switch = pyqtSignal(int)
    signal_layer_convert = pyqtSignal(int)
    signal_layer_name_change = pyqtSignal(int, str)

    layer_icons_catalog = settings.program_catalog + "\\resources\\icons\\"

    def __init__(self):
        super().__init__()

        dummy = QWidget()
        self.setWidget(dummy)
        self.setTitleBarWidget(QWidget())

        layout_main = QVBoxLayout(dummy)

        self._icon_visible = QPixmap(LayersPanel.layer_icons_catalog + "\\layer_visible.png")
        self._icon_hidden = QPixmap(LayersPanel.layer_icons_catalog + "\\layer_hidden.png")
        self._icon_convert = QPixmap(LayersPanel.layer_icons_catalog + "\\layer_convert.png")

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

    def add_button_layer(self, idx: int, visible=True, name="Layer", convert=True):
        item = QListWidgetItem()
        container = Container(idx=idx)

        # tile = Tile(idx, name=name, show_name=True)
        # container.add_widget(tile, 'name')
        editable_name = EditableName(name=name, idx=idx, fun=self.name_change)
        container.add_widget(editable_name, 'name')

        icon_visible = QIcon(self._icon_visible) if visible else QIcon(self._icon_hidden)
        button = self.create_icon_button(icon_visible, fun=self.switch_visibility, data=idx)
        container.add_widget(button, 'visible')

        if convert:
            icon_convert = QIcon(self._icon_convert)
            button = self.create_icon_button(icon_convert, fun=self.convert_layer, data=idx)
            container.add_widget(button, 'convert')

        item.setSizeHint(container.sizeHint())

        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, container)

    @QtCore.pyqtSlot(int)
    def added_new_layer(self, idx: int):
        layer = layer_adapter.get_layer_gui(idx)
        self.add_button_layer(idx=layer.idx, visible=layer.visible, name=layer.name, convert=not layer.editable)

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

    def refresh(self):
        self.list_widget.clear()

        layers = layer_adapter.get_layers_gui()
        for idx in layer_adapter.get_order():
            self.add_button_layer(
                idx=layers[idx].idx,
                name=layers[idx].name,
                visible=layers[idx].visible,
                convert=not layers[idx].editable
            )

    @QtCore.pyqtSlot()
    def layers_order_changed(self):
        self.refresh()

    def switch_visibility(self, idx: int):
        self.signal_layer_visibility_switch.emit(idx)

    def convert_layer(self, idx: int):
        self.signal_layer_convert.emit(idx)
    
    def create_icon_button(self, icon: QIcon, fun, data):
        button = QToolButton()
        button.setIcon(icon)
        button.setIconSize(QSize(30, 30))
        button.clicked.connect(lambda _, d=data: fun(d))
        button.setStyleSheet("""
            background: transparent;
            border: none;
            padding: 0px;
        """)
        return button

    def name_change(self, idx: int, name: str):
        self.signal_layer_name_change.emit(idx, name)