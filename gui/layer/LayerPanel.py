from PyQt6.QtCore import pyqtSignal, QSize, QPoint, Qt, QSignalBlocker
from PyQt6.QtGui import QIcon, QPixmap, QCursor
from PyQt6.QtWidgets import QPushButton, QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, \
    QToolButton, QMenu

from gui.EventListener import EventListener
from gui.components.Container import Container
from gui.components.EditableName import EditableName

import resources.settings as settings


class LayerPanel(QDockWidget, EventListener):
    signal_layer_create_order = pyqtSignal()
    signal_layer_choose = pyqtSignal(int)
    signal_layer_reorder_order = pyqtSignal(list)
    signal_layer_visibility_switch = pyqtSignal(int)
    signal_layer_convert = pyqtSignal(int)
    signal_layer_name_change = pyqtSignal(int, str)
    signal_layer_delete = pyqtSignal(int)
    signal_event_occurred = pyqtSignal(dict)

    layer_icons_catalog = settings.program_catalog + "\\resources\\icons\\"

    def __init__(self, event_provider):
        super().__init__()

        self._event_provider = event_provider
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
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)
        layout_main.addWidget(self.list_widget)

        self.event_types.update({
            'layer_created': self.added_new_layer,
            'layer_deleted': self.layer_deleted,
            'layer_current_idx_changed': self.layer_current_idx_changed,
            'layer_order_restored': self.layer_order_restored,
        })
        self.subscribe_to_events(self._event_provider, self.signal_event_occurred)

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

        self.list_widget.insertItem(0, item)
        self.list_widget.setItemWidget(item, container)
        return item

    def added_new_layer(self, data):
        layer = self._controller.convert_layer_gui(data['layer'])
        item = self.add_button_layer(idx=layer.idx, visible=layer.visible, name=layer.name, convert=not layer.editable)
        self.list_widget.setCurrentItem(item)
        item.setSelected(True)

    def layer_deleted(self, data):
        idx = data['idx']
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            container = self.list_widget.itemWidget(item)

            if container.get_idx() == idx:
                self.list_widget.removeItemWidget(item)
                self.list_widget.takeItem(i)
                container.deleteLater()
                return

    def layer_current_idx_changed(self, data):
        idx = data['idx']
        blocker = QSignalBlocker(self.list_widget)

        try:
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                container = self.list_widget.itemWidget(item)

                if container.get_idx() == idx:
                    self.list_widget.setCurrentItem(item)
                    return
        finally:
            del blocker

    def layers_moved(self, parent, start, end, destination, row):
        new_order = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            new_order.append(widget.get_idx())

        layer_order = list(reversed(new_order))
        self.signal_layer_reorder_order.emit(layer_order)

    def layer_choose(self, element_num: int):
        if element_num < 0:
            return
        item = self.list_widget.item(element_num)
        widget = self.list_widget.itemWidget(item)
        self.signal_layer_choose.emit(widget.get_idx())

    def switch_visibility(self, data):
        self.signal_layer_visibility_switch.emit(data)

    def convert_layer(self, idx: int):
        self.signal_layer_convert.emit(idx)

    def show_context_menu(self, pos):
        item = self.list_widget.itemAt(pos)
        if item is None:
            return

        menu = QMenu()
        delete_action = menu.addAction('Delete')
        selected = menu.exec(self.list_widget.viewport().mapToGlobal(pos))
        if selected == delete_action:
            container = self.list_widget.itemWidget(item)
            self.signal_layer_delete.emit(container.get_idx())

    
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

    def layer_order_restored(self, data):
        self.set_layer_order(data['order'])

    def set_layer_order(self, order):
        blocker = QSignalBlocker(self.list_widget)

        row_order = list(reversed(order))
        rank = {idx: dest_pos for dest_pos, idx in enumerate(row_order)}

        for row in range(self.list_widget.count()):
            item = self.list_widget.item(row)
            widget = self.list_widget.itemWidget(item)
            item.setText(f"{rank[widget.get_idx()]:08d}")

        self.list_widget.sortItems(Qt.SortOrder.AscendingOrder)

        for row in range(self.list_widget.count()):
            self.list_widget.item(row).setText("")

        del blocker