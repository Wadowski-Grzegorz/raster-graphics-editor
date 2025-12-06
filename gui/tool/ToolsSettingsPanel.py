from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QDockWidget, QWidget, QStackedWidget

from adapters.BrushAdapter import brush_adapter
from gui.components.Container import Container
from gui.components.SelectionList import SelectionList
from gui.components.ValueField import ValueField
from dto.SelectableItem import SelectableItem

class ToolsSettingsPanel(QDockWidget):
    signal_brush_changed_parameter = pyqtSignal((str, float), (str, int))
    signal_brush_selected = pyqtSignal(int)

    def __init__(self, tools: list[SelectableItem]):
        super().__init__()

        self.setTitleBarWidget(QWidget())

        self._stacked_widgets = QStackedWidget()
        for t in tools:
            if t.name.lower() == 'brush':
                self._init_brush()

        self.setWidget(self._stacked_widgets)


    def _init_brush(self):
        container = Container('brush')

        brush_list = SelectionList(brush_adapter.get_brushes_selectable(), self.selected_brush)
        container.add_widget(brush_list, 'brush_list')

        size_field = ValueField('size', min_v=1, max_v=1000)
        container.add_widget(size_field, 'size')
        size_field.signal_value_changed.connect(
            lambda v: self.signal_brush_changed_parameter.emit('size', v)
        )

        opacity_field = ValueField('opacity', suffix='%')
        container.add_widget(opacity_field, 'opacity')
        opacity_field.signal_value_changed.connect(
            lambda v: self.signal_brush_changed_parameter.emit('opacity', v / 100)
        )

        flow_field = ValueField('flow', suffix='%')
        container.add_widget(flow_field, 'flow')
        flow_field.signal_value_changed.connect(
            lambda v: self.signal_brush_changed_parameter.emit('flow', v / 100)
        )

        hardness_field = ValueField('hardness', suffix='%')
        container.add_widget(hardness_field, 'hardness')
        hardness_field.signal_value_changed.connect(
            lambda v: self.signal_brush_changed_parameter.emit('hardness', v / 100)
        )

        self._stacked_widgets.addWidget(container)

        self.changed_brush()

    def selected_brush(self, idx: int):
        self.signal_brush_selected.emit(idx)

    def changed_brush(self):
        brush = brush_adapter.get_current_brush()
        i, container = self.get_tool_nr_widget('brush')

        container.set_widget_value('size', brush.size)
        container.set_widget_value('opacity', brush.opacity * 100)
        container.set_widget_value('flow', brush.flow * 100)
        container.set_widget_value('hardness', brush.hardness * 100)

    @pyqtSlot(str)
    def tool_changed(self, name: str):
        i, widget = self.get_tool_nr_widget(name)
        self._stacked_widgets.setCurrentIndex(i)

    def get_tool_nr_widget(self, name: str):
        name = name.lower()
        for i in range(self._stacked_widgets.count()):
            element = self._stacked_widgets.widget(i)
            if element.get_name() == name:
                return i, element
