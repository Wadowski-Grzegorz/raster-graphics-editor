import numpy as np

from core.layer.LayerManager import layer_manager
from core.brush.BrushManager import brush_manager
from core.tool.BrushTool import BrushTool

class ToolManager:
    def __init__(self):
        super().__init__()

        self._tools = {
            'brush': BrushTool()
        }
        self._curr_tool = self._tools['brush']

        self._layers = {} # as numpy
        self._curr_idx = None
        self._temp_layer = None # as numpy

        self._curr_brush = brush_manager.get_current_brush()
        self._curr_color = np.array([0, 0, 0, 255], dtype="uint8")

    def on_press(self, x, y):
        self._curr_tool.on_press(
            x, y,
            layer=self._layers[self._curr_idx],
            temp_layer=self._temp_layer,
            brush=self._curr_brush,
            color=self._curr_color
        )

    def on_move(self, start_x, start_y, end_x, end_y):
        self._curr_tool.on_move(
            start_x, start_y,
            end_x, end_y,
            layer=self._layers[self._curr_idx],
            temp_layer=self._temp_layer,
            brush=self._curr_brush,
            color=self._curr_color
        )

    def on_release(self):
        self._curr_tool.on_release(
            layer=self._layers[self._curr_idx],
            temp_layer=self._temp_layer,
            brush=self._curr_brush,
            color=self._curr_color
        )


    def refresh_data(self):
        self._layers = layer_manager.get_layers_arr()
        self.refresh_idx()

    def refresh_idx(self):
        self._curr_idx = layer_manager.get_current_idx()

    def added_temp_layer(self, layer: np.ndarray):
        self._temp_layer = layer

    def changed_layer(self):
        self.refresh_idx()

    def changed_brush(self):
        self._curr_brush = brush_manager.get_current_brush()

    def changed_color(self, color: list[int, int, int]):
        self._curr_color[:3] = color
    
    def get_current_color(self):
        return self._curr_color.copy()