from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout
from dto.SelectableItem import SelectableItem
from gui.components.SelectionMenu import SelectionMenu


class ToolPanel(QDockWidget):
    signal_tool_selected = pyqtSignal(str)

    def __init__(self, tools_selectable: list[SelectableItem]):
        super().__init__()

        self.tools_selectable = tools_selectable

        dummy = QWidget()
        self.setWidget(dummy)
        layout_main = QVBoxLayout(dummy)

        self.setTitleBarWidget(QWidget())
        self.setMinimumWidth(30)
        self.setMaximumWidth(70)

        self.menu = SelectionMenu(self.tools_selectable, self.tool_choose, identify='name')
        layout_main.addWidget(self.menu)
        self.menu.set_current_row('brush')

    def tool_choose(self, name: str):
        self.signal_tool_selected.emit(name)