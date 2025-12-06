from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

from gui.tool.ToolsSettingsPanel import ToolsSettingsPanel
from gui.tool.ToolsPanel import ToolsPanel


class ToolsPanelsController(QObject):
    def __init__(self, tools_panel: ToolsPanel, tools_settings_panel: ToolsSettingsPanel):
        super().__init__()

        self.tools_panel = tools_panel
        self.tools_settings_panel = tools_settings_panel
