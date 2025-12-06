from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDockWidget, QWidget, QHBoxLayout

from adapters.BrushAdapter import brush_adapter
from gui.components.SelectionList import SelectionList
from gui.components.ValueField import ValueField

class ToolsSettingsPanel(QDockWidget):
    signal_brush_changed_parameter = pyqtSignal((str, float), (str, int))
    signal_brush_selected = pyqtSignal(int)


    def __init__(self):
        super().__init__()

        dummy = QWidget()
        self.setWidget(dummy)
        layout_main = QHBoxLayout(dummy)

        self.setTitleBarWidget(QWidget())

        self.layout_options = QHBoxLayout()
        layout_main.addLayout(self.layout_options)

        self.brush_list = SelectionList(brush_adapter.get_brushes_selectable(), self.selected_brush)
        self.layout_options.addWidget(self.brush_list)

        self.size_field = ValueField('size', min_v=1, max_v=1000)
        self.layout_options.addWidget(self.size_field)
        self.size_field.signal_value_changed.connect(
            lambda v: self.signal_brush_changed_parameter.emit('size', v)
        )

        self.opacity_field = ValueField('opacity', suffix='%')
        self.layout_options.addWidget(self.opacity_field)
        self.opacity_field.signal_value_changed.connect(
            lambda v: self.signal_brush_changed_parameter.emit('opacity', v/100)
        )

        self.flow_field = ValueField('flow', suffix='%')
        self.layout_options.addWidget(self.flow_field)
        self.flow_field.signal_value_changed.connect(
            lambda v: self.signal_brush_changed_parameter.emit('flow', v / 100)
        )

        self.hardness_field = ValueField('hardness', suffix='%')
        self.layout_options.addWidget(self.hardness_field)
        self.hardness_field.signal_value_changed.connect(
            lambda v: self.signal_brush_changed_parameter.emit('hardness', v / 100)
        )

        self.changed_brush()

    def selected_brush(self, idx: int):
        self.signal_brush_selected.emit(idx)

    def changed_brush(self):
        brush = brush_adapter.get_current_brush()
        self.size_field.set_value_quiet(brush.size)
        self.opacity_field.set_value_quiet(brush.opacity * 100)
        self.flow_field.set_value_quiet(brush.flow * 100)
        self.hardness_field.set_value_quiet(brush.hardness * 100)
