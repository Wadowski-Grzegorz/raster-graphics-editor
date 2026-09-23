from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from gui.tool.ToolSettingsPanel import ToolSettingsPanel
from gui.tool.ToolPanel import ToolPanel
from gui.tool.tools.GuiToolManager import GuiToolManager


class ToolPanelsManager(QObject):
    signal_tool_select = pyqtSignal(str)
    signal_brush_select = pyqtSignal(int)
    signal_brush_change_parameter = pyqtSignal((str, float), (str, int))

    def __init__(self, event_provider, canvas):
        super().__init__()
        self._event_provider = event_provider
        self._controller = None
        # consistent order of tools and their id's

        self._tool_manager = GuiToolManager(canvas)
        self.tool_panel = None
        self.tool_settings_panel = None

    def get_tool_panel(self):
        return self.tool_panel

    def get_tool_settings_panel(self):
        return self.tool_settings_panel

    def tool_selected(self, by_name: str):
        self.tool_settings_panel.tool_changed(by_name)
        self.signal_tool_select.emit(by_name)

    def set_controller(self, controller):
        self._controller = controller
        self._init()

    def _init(self):
        core_tools = self._controller.get_tools_selectable()
        gui_tools = self._controller.convert_tools_to_selectable( self._tool_manager.get_tools() )
        tools = core_tools + gui_tools
        self.tool_panel = ToolPanel(tools)
        self.tool_settings_panel = ToolSettingsPanel(
            self._event_provider,
            self.signal_brush_change_parameter,
            self.signal_brush_select
        )
        self.tool_settings_panel.init(self._controller, tools)
        self.tool_panel.signal_tool_selected.connect(self.tool_selected)

    def tool_select(self, name):
        return self._tool_manager.tool_select(name)

    def on_press(self, x, y):
        self._tool_manager.on_press(x, y)

    def on_move(self, start_x, start_y, end_x, end_y):
        self._tool_manager.on_move(start_x, start_y, end_x, end_y)

    def on_release(self):
        self._tool_manager.on_release()

    def get_tools(self):
        return self._tool_manager.get_tools()