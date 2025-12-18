from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDockWidget, QWidget, QStackedWidget

from gui.components.Container import Container
from gui.components.SelectionList import SelectionList
from gui.components.ValueField import ValueField
from dto.SelectableItem import SelectableItem

class ToolSettingsPanel(QDockWidget):

    def __init__(self, event, fun_brush_change_parameter=None, fun_brush_selected=None):
        super().__init__()

        self._event = event
        self._controller = None

        self.fun_brush_change_parameter = fun_brush_change_parameter
        self.fun_brush_selected = fun_brush_selected

        self.setTitleBarWidget(QWidget())

        self._stacked_widgets = QStackedWidget()
        self._brush_affects_tool = []

        self.setWidget(self._stacked_widgets)
        self._event.subscribe('brush_current_changed', self.changed_brush)

    def _init_brush(self):
        container = Container('brush')
        self._tool_uses_brush(container)
        self._stacked_widgets.addWidget(container)

    def _init_eraser(self):
        container = Container('eraser')
        self._tool_uses_brush(container)
        self._stacked_widgets.addWidget(container)

    def _init_move(self):
        container = Container('move')
        self._tool_uses_brush(container)
        self._stacked_widgets.addWidget(container)

    def _init_blur(self):
        container = Container('blur')
        size_field = ValueField('size', min_v=1, max_v=1000)
        container.add_widget(size_field, 'size')
        size_field.signal_value_changed.connect(
            lambda v: self.fun_brush_change_parameter.emit('size', v)
        )
        self._stacked_widgets.addWidget(container)

    def _init_hand(self):
        container = Container('hand')
        self._stacked_widgets.addWidget(container)

    def _init_resize(self):
        container = Container('resize')
        self._stacked_widgets.addWidget(container)

    def _tool_uses_brush(self, container):
        self._brush_affects_tool.append(container.get_name())
        brush_list = SelectionList(self._controller.get_brushes_selectable(), self.select_brush)
        container.add_widget(brush_list, 'brush_list')

        size_field = ValueField('size', min_v=1, max_v=1000)
        container.add_widget(size_field, 'size')
        size_field.signal_value_changed.connect(
            lambda v: self.fun_brush_change_parameter.emit('size', v)
        )

        opacity_field = ValueField('opacity', suffix='%')
        container.add_widget(opacity_field, 'opacity')
        opacity_field.signal_value_changed.connect(
            lambda v: self.fun_brush_change_parameter.emit('opacity', v / 100)
        )

        flow_field = ValueField('flow', suffix='%')
        container.add_widget(flow_field, 'flow')
        flow_field.signal_value_changed.connect(
            lambda v: self.fun_brush_change_parameter.emit('flow', v / 100)
        )

        hardness_field = ValueField('hardness', suffix='%')
        container.add_widget(hardness_field, 'hardness')
        hardness_field.signal_value_changed.connect(
            lambda v: self.fun_brush_change_parameter.emit('hardness', v / 100)
        )

    def select_brush(self, idx: int):
        self.fun_brush_selected.emit(idx)

    def changed_brush(self, data):
        if self._controller is None:
            return
        brush = self._controller.convert_brush_to_gui(data['brush'])
        for name in self._brush_affects_tool:
            i, container = self.get_tool_nr_widget(name)
            container.set_widget_value('size', brush.size)
            container.set_widget_value('opacity', brush.opacity * 100)
            container.set_widget_value('flow', brush.flow * 100)
            container.set_widget_value('hardness', brush.hardness * 100)

        i, container = self.get_tool_nr_widget('blur')
        container.set_widget_value('size', brush.size)

    @pyqtSlot(str)
    def tool_changed(self, name: str):
        i, widget = self.get_tool_nr_widget(name)
        self._stacked_widgets.setCurrentIndex(i)

    def get_tool_nr_widget(self, name: str):
        name_low = name.lower()
        for i in range(self._stacked_widgets.count()):
            element = self._stacked_widgets.widget(i)
            if element.get_name() == name_low:
                return i, element

    def init(self, controller, tools: list[SelectableItem]):
        self._controller = controller
        for t in tools:
            if t.name.lower() == 'brush':
                self._init_brush()
            if t.name.lower() == 'eraser':
                self._init_eraser()
            if t.name.lower() == 'blur':
                self._init_blur()
            if t.name.lower() == 'hand':
                self._init_hand()
            if t.name.lower() == 'move':
                self._init_move()
            if t.name.lower() == 'resize':
                self._init_resize()