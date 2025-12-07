from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from adapters.ToolAdapter import tool_adapter
from gui.tool.ToolsSettingsPanel import ToolsSettingsPanel
from gui.tool.ToolsPanel import ToolsPanel


class ToolsPanelsController(QObject):
    signal_tool_selected = pyqtSignal(str)
    signal_brush_selected = pyqtSignal(int)
    signal_brush_change_parameter = pyqtSignal((str, float), (str, int))

    def __init__(self):
        super().__init__()

        # consistent order of tools and their id's
        tools = tool_adapter.get_tools_selectable()

        self.tools_panel = ToolsPanel(tools)

        self.tools_settings_panel = ToolsSettingsPanel(
            tools,
            self.signal_brush_change_parameter,
            self.signal_brush_selected
        )

        self.tools_panel.signal_tool_selected.connect(self.tool_selected)

    def get_tools_panel(self):
        return self.tools_panel

    def get_tools_settings_panel(self):
        return self.tools_settings_panel

    def tool_selected(self, by_name: str):
        self.tools_settings_panel.tool_changed(by_name)
        self.signal_tool_selected.emit(by_name)

    @pyqtSlot()
    def changed_brush(self):
        self.tools_settings_panel.changed_brush()