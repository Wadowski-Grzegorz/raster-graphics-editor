import numpy as np

from core.layer.LayerManager import layer_manager
from core.brush.BrushManager import brush_manager
from core.tool.BlurTool import BlurTool
from core.tool.BrushTool import BrushTool
from core.tool.EraserTool import EraserTool
from core.tool.MoveTool import MoveTool

from resources.tools_reversible import tools_reversible

class CoreToolManager:
    def __init__(self):
        super().__init__()

        brush = BrushTool()
        self._tools = [brush, EraserTool(), BlurTool(), MoveTool()]
        self._curr_tool = brush

        self._curr_layer = None
        self._curr_idx = None
        self._temp_layer = None # as numpy

        self._curr_brush = brush_manager.get_current_brush()
        self._curr_color = np.array([0, 0, 0, 255], dtype="uint8")

    def on_press(self, x, y):
        if self.check_usage() is False:
            return
        self._curr_tool.on_press(
            x, y,
            layer=self._curr_layer,
            temp_layer=self._temp_layer,
            brush=self._curr_brush,
            color=self._curr_color
        )

    def on_move(self, start_x, start_y, end_x, end_y):
        if self.check_usage() is False:
            return
        self._curr_tool.on_move(
            start_x, start_y,
            end_x, end_y,
            layer=self._curr_layer,
            temp_layer=self._temp_layer,
            brush=self._curr_brush,
            color=self._curr_color
        )

    def on_release(self):
        if self.check_usage() is False:
            return
        self._curr_tool.on_release(
            layer=self._curr_layer,
            temp_layer=self._temp_layer,
            brush=self._curr_brush,
            color=self._curr_color
        )

    def check_usage(self):
        # check if tool can be used on this layer
        layer_flag = self._curr_layer.can_change()
        if layer_flag:
            return True

        name = self._curr_tool.get_name().lower()
        tool_flag = tools_reversible[name]
        return tool_flag

    def refresh_data(self):
        self._curr_layer = layer_manager.get_current_layer()
        self._temp_layer = layer_manager.get_temp_layer()
        self.refresh_idx()

    def refresh_idx(self):
        self._curr_idx = layer_manager.get_current_idx()

    def changed_layer(self):
        self.refresh_idx()

    def changed_brush(self):
        self._curr_brush = brush_manager.get_current_brush()

    def changed_color(self, color: list[int, int, int]):
        self._curr_color[:3] = color

    def get_current_color(self):
        return self._curr_color.copy()

    def get_tools(self):
        return self._tools.copy()

    def tool_selected(self, name:str):
        for tool in self._tools:
            if tool.get_name().lower() == name.lower():
                self._curr_tool = tool
                return True
        return False

core_tool_manager = CoreToolManager()