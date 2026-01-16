import numpy as np

from core.tool.BlurTool import BlurTool
from core.tool.BrushTool import BrushTool
from core.tool.EraserTool import EraserTool
from core.tool.MoveTool import MoveTool
from core.tool.ResizeTool import ResizeTool

from resources.tools_reversible import tools_reversible

class CoreToolManager:
    def __init__(self, event):
        super().__init__()

        self._event = event

        brush = BrushTool()
        self._tools = [brush, EraserTool(), BlurTool(), MoveTool(), ResizeTool()]
        self._curr_tool = brush

        self._curr_layer = None
        self._temp_layer = None # as numpy

        self._curr_brush = None
        self._curr_color = np.array([0, 0, 0, 255], dtype="uint8")

        self._event.subscribe('layer_created', self.set_current_layer)
        self._event.subscribe('layer_temp_created', self.set_temp_layer)
        self._event.subscribe("layer_changed_type", self.set_current_layer)
        self._event.subscribe('layer_current_idx_changed', self.set_current_layer)
        self._event.subscribe('brush_current_changed', self.changed_brush)

    def init(self):
        self._event.notify(
            'tool_current_changed',
            {
                "id": self._curr_tool.get_idx(),
                "tool": self._curr_tool
            }
        )

    def on_press(self, x, y):
        if self._check_usage() is False:
            return
        self._curr_tool.on_press(
            x, y,
            layer=self._curr_layer,
            temp_layer=self._temp_layer,
            brush=self._curr_brush,
            color=self._curr_color
        )
        self._event.notify('paint_painted', {"layer": self._curr_layer})

    def on_move(self, start_x, start_y, end_x, end_y):
        if self._check_usage() is False:
            return
        self._curr_tool.on_move(
            start_x, start_y,
            end_x, end_y,
            layer=self._curr_layer,
            temp_layer=self._temp_layer,
            brush=self._curr_brush,
            color=self._curr_color
        )
        self._event.notify('paint_painted', {"layer": self._curr_layer})

    def on_release(self):
        if self._check_usage() is False:
            return
        self._curr_tool.on_release(
            layer=self._curr_layer,
            temp_layer=self._temp_layer,
            brush=self._curr_brush,
            color=self._curr_color
        )
        self._event.notify('paint_ended', {"layer": self._curr_layer})

    def _check_usage(self):
        # check if tool can be used on this layer
        layer_flag = self._curr_layer.is_editable()
        if layer_flag:
            return True

        name = self._curr_tool.get_name().lower()
        tool_flag = tools_reversible[name]
        return tool_flag

    def changed_brush(self, data):
        self._curr_brush = data['brush']

    def change_color(self, color: list[int, int, int]):
        self._curr_color[:3] = color
        self._event.notify('color_changed', {"color": self._curr_color})

    def get_current_color(self):
        return self._curr_color.copy()

    def get_tools(self):
        return self._tools.copy()

    def tool_select(self, name:str):
        for tool in self._tools:
            if tool.get_name().lower() == name.lower():
                self._curr_tool = tool
                self._event.notify(
                    'tool_current_changed',
                    {
                        "id": self._curr_tool.get_idx(),
                        "tool": self._curr_tool
                    }
                )
                return True
        return False

    def set_current_layer(self, data):
        self._curr_layer = data['layer']

    def set_temp_layer(self, data):
        self._temp_layer = data['layer'].get_layer()