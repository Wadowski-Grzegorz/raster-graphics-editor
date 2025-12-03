from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDockWidget, QWidget, QHBoxLayout
from gui.tool.ValueField import ValueField

class ToolsPanel(QDockWidget):
    signal_brush_changed_size = pyqtSignal(float)
    signal_brush_changed_opacity = pyqtSignal(float)
    signal_brush_changed_flow = pyqtSignal(float)


    def __init__(self):
        super().__init__()

        dummy = QWidget()
        self.setWidget(dummy)
        layout_main = QHBoxLayout(dummy)

        self.setTitleBarWidget(QWidget())

        self.layout_options = QHBoxLayout()
        layout_main.addLayout(self.layout_options)

        self.size_field = ValueField('size', 1, min_v=1, max_v=1000)
        self.layout_options.addWidget(self.size_field)
        self.size_field.signal_value_changed.connect(self.signal_brush_changed_size)

        self.opacity_field = ValueField('opacity', 100, suffix='%')
        self.layout_options.addWidget(self.opacity_field)
        self.opacity_field.signal_value_changed.connect(
            lambda v: self.signal_brush_changed_opacity.emit(v/100)
        )

        self.flow_field = ValueField('flow', 100, suffix='%')
        self.layout_options.addWidget(self.flow_field)
        self.flow_field.signal_value_changed.connect(
            lambda v: self.signal_brush_changed_flow.emit(v / 100)
        )

