from core.layer.LayerManager import layer_manager
from gui.Canvas import Canvas
from gui.tool.tools.HandTool import HandTool


class GuiToolManager:
    def __init__(self):
        super().__init__()

        self._tools = [HandTool()]
        self._curr_tool = self._tools[0]

    def on_press(self, x, y):
        self._curr_tool.on_press(
            x, y,
        )

    def on_move(self, start_x, start_y, end_x, end_y):
        self._curr_tool.on_move(
            start_x, start_y,
            end_x, end_y,
        )

    def on_release(self):
        self._curr_tool.on_release()

    def refresh_data(self):
        self._layers = layer_manager.get_layers_arr()
        self.refresh_idx()

    def refresh_idx(self):
        self._curr_idx = layer_manager.get_current_idx()

    def changed_layer(self):
        self.refresh_idx()

    def get_tools(self):
        return self._tools.copy()

    def tool_selected(self, name: str):
        for tool in self._tools:
            if tool.get_name().lower() == name.lower():
                self._curr_tool = tool
                return True
        return False

    def active_tools(self, canvas: Canvas):
        for tool in self._tools:
            if tool.get_name().lower() == 'hand':
                tool.active(canvas)


gui_tool_manager = GuiToolManager()