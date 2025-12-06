from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QListWidget
from adapters.ToolAdapter import tool_adapter

class ToolsPanel(QDockWidget):
    def __init__(self):
        super().__init__()

        dummy = QWidget()
        self.setWidget(dummy)
        layout_main = QVBoxLayout()

        self.setTitleBarWidget(QWidget())

        self.tools = QListWidget()
        get_tools_selectable()
