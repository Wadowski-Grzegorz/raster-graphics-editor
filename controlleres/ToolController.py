from gui.Canvas import Canvas
from core.tool.CoreToolManager import core_tool_manager
from gui.tool.tools.GuiToolManager import gui_tool_manager


class ToolController:
    def __init__(self, canvas: Canvas):
        self._canvas = canvas
        self._current_manager = core_tool_manager

        gui_tool_manager.active_tools(self._canvas)

        self._canvas.signal_cursor_pressed.connect(self.on_press)
        self._canvas.signal_cursor_moved.connect(self.on_move)
        self._canvas.signal_cursor_released.connect(self.on_release)


    def tool_selected(self, name:str):
        if core_tool_manager.tool_selected(name):
            self._current_manager = core_tool_manager
        elif gui_tool_manager.tool_selected(name):
            self._current_manager = gui_tool_manager

    def on_press(self, x, y):
        self._current_manager.on_press(x, y)

    def on_move(self, start_x, start_y, end_x, end_y):
        self._current_manager.on_move(start_x, start_y, end_x, end_y)

    def on_release(self):
        self._current_manager.on_release()

    def changed_color(self, color: list[int, int, int]):
        core_tool_manager.changed_color(color)

    def refresh_data(self):
        core_tool_manager.refresh_data()

    def changed_brush(self):
        core_tool_manager.changed_brush()

    def get_tools(self):
        return core_tool_manager.get_tools() + gui_tool_manager.get_tools()