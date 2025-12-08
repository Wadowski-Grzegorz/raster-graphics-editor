from abc import ABC, abstractmethod

from core.tool.Tool import Tool


class GuiTool(Tool, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def on_press(self, x, y, layer=None):
        pass

    @abstractmethod
    def on_move(self, start_x, start_y, end_x, end_y, layer=None):
        pass

    @abstractmethod
    def on_release(self, layer=None):
        pass