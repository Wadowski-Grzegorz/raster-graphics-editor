from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from tool.ValueField import ValueField

class Tools_panel(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        dummy = QWidget()
        self.setWidget(dummy)
        layout_main = QHBoxLayout(dummy)

        self.setTitleBarWidget(QWidget())

        self.layout_options = QHBoxLayout()
        layout_main.addLayout(self.layout_options)

        self.layout_options.addWidget(ValueField('size', 1, min=1, max=1000, suffix='', step=0.5))
        self.layout_options.addWidget(ValueField('opacity', 100))
        self.layout_options.addWidget(ValueField('flow', 100))

