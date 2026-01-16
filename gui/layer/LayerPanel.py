from PyQt6.QtCore import pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QPushButton, QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, \
    QToolButton

from gui.components.Container import Container
from gui.components.EditableName import EditableName

import resources.settings as settings


class LayerPanel(QDockWidget):
    signal_layer_create_order = pyqtSignal()
    signal_layer_choose = pyqtSignal(int)
    signal_layer_reorder_order = pyqtSignal(list)
    signal_layer_visibility_switch = pyqtSignal(int)
    signal_layer_convert = pyqtSignal(int)
    signal_layer_name_change = pyqtSignal(int, str)

    layer_icons_catalog = settings.program_catalog + "\\resources\\icons\\"

    def __init__(self, event):
        super().__init__()

        self._event = event
        self._controller = None

        dummy = QWidget()
        self.setWidget(dummy)
        self.setTitleBarWidget(QWidget())

        layout_main = QVBoxLayout(dummy)

        self._icon_visible = QPixmap(LayerPanel.layer_icons_catalog + "\\layer_visible.png")
        self._icon_hidden = QPixmap(LayerPanel.layer_icons_catalog + "\\layer_hidden.png")
        self._icon_convert = QPixmap(LayerPanel.layer_icons_catalog + "\\layer_convert.png")

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

        self._event.subscribe('layer_created', self.added_new_layer)

    def add_button_layer(self, idx: int, visible=True, name="Layer", convert=True):
        item = QListWidgetItem()
        container = Container(idx=idx)

        editable_name = EditableName(name=name, idx=idx, fun=self.name_change)
        container.add_widget(editable_name, 'name')

        icon_visible = QIcon(self._icon_visible)
        icon_hidden = QIcon(self._icon_hidden)
        if visible:
            button = self._create_toggle_icon_button(icon_hidden, icon_visible, self.switch_visibility, idx)
        else:
            button = self._create_toggle_icon_button(icon_visible, icon_hidden, self.switch_visibility, idx)
        container.add_widget(button, 'visible')

        if convert:
            icon_convert = QIcon(self._icon_convert)
            button = self._create_destructive_icon_button(icon_convert, fun=self.convert_layer, data=idx)
            container.add_widget(button, 'convert')

        item.setSizeHint(container.sizeHint())

        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, container)
        return item

    def added_new_layer(self, data):
        layer = self._controller.convert_layer_gui(data['layer'])
        item = self.add_button_layer(idx=layer.idx, visible=layer.visible, name=layer.name, convert=not layer.editable)
        self.list_widget.setCurrentItem(item)
        item.setSelected(True)

    def layers_moved(self, parent, start, end, destination, row):
        new_order = []
        selected = None
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            new_order.append(widget.get_idx())
            if item.isSelected():
                selected = widget.get_idx()

        self.signal_layer_reorder_order.emit(new_order)
        self.reorder(new_order, selected=selected)

    def layer_choose(self, element_num: int):
        if element_num < 0:
            return
        item = self.list_widget.item(element_num)
        widget = self.list_widget.itemWidget(item)
        self.signal_layer_choose.emit(widget.get_idx())

    def reorder(self, new_order, selected=None):
        self.list_widget.clear()

        layers = self._controller.get_layers_gui()
        for idx in new_order:
            item = self.add_button_layer(
                idx=layers[idx].idx,
                name=layers[idx].name,
                visible=layers[idx].visible,
                convert=not layers[idx].editable
            )
            if selected and idx == selected:
                self.list_widget.setCurrentItem(item)
                item.setSelected(True)

    def switch_visibility(self, data):
        self.signal_layer_visibility_switch.emit(data)

    def convert_layer(self, idx: int):
        self.signal_layer_convert.emit(idx)
    
    def _create_destructive_icon_button(self, icon: QIcon, fun, data):
        button = QToolButton()
        button.setIcon(icon)
        button.setIconSize(QSize(30, 30))
        button.setStyleSheet("""
            background: transparent;
            border: none;
            padding: 0px;
        """)
        button.clicked.connect(lambda _, d=data: fun(d))
        button.clicked.connect(lambda _, b=button: b.setParent(None))
        button.clicked.connect(lambda _, b=button: b.deleteLater())
        return button

    def _create_toggle_icon_button(self, icon_on: QIcon, icon_off: QIcon, fun, data):
        icon_on = QIcon(icon_on)
        icon_off = QIcon(icon_off)
        button = QToolButton()
        button.setCheckable(True)
        button.setIcon(icon_off)
        button.setIconSize(QSize(30, 30))
        button.setStyleSheet(
            """
            background: transparent;
            border: none;
            padding: 0px;
            """
        )
        button.toggled.connect(
            lambda check, b=button, i_on=icon_on, i_off=icon_off: b.setIcon(i_on if check else i_off)
        )
        button.toggled.connect(lambda _, d=data: fun(d))
        return button

    def name_change(self, idx: int, name: str):
        self.signal_layer_name_change.emit(idx, name)

    def set_controller(self, controller):
        self._controller = controller