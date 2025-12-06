from abc import ABC, abstractmethod

from core.tool.Tool import Tool


class CoreTool(Tool, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def on_press(self, x, y, layer=None, temp_layer=None, brush=None, color=None):
        pass

    @abstractmethod
    def on_move(self, start_x, start_y, end_x, end_y, layer=None, temp_layer=None, brush=None, color=None):
        pass

    @abstractmethod
    def on_release(self, layer=None, temp_layer=None, brush=None, color=None):
        pass