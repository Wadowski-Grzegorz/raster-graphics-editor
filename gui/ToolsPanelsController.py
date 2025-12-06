from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

from adapters.BrushAdapter import brush_adapter
from adapters.ToolAdapter import tool_adapter
from gui.tool.ToolsSettingsPanel import ToolsSettingsPanel
from gui.tool.ToolsPanel import ToolsPanel


class ToolsPanelsController(QObject):
    def __init__(self):
        super().__init__()

        # consistent order of tools and their id's
        tools = tool_adapter.get_tools_selectable()

        self.tools_panel = ToolsPanel(tools)
        self.tools_settings_panel = ToolsSettingsPanel(tools)

        self.tools_panel.signal_tool_selected.connect(self.tools_settings_panel.tool_changed)

    def get_tools_panel(self):
        return self.tools_panel

    def get_tools_settings_panel(self):
        return self.tools_settings_panel