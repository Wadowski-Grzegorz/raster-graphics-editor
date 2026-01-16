from abc import ABC, abstractmethod
import numpy as np

from core.tool.Tool import Tool


class CoreTool(Tool, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def on_press(self, x, y, layer=None, temp_layer=None, brush=None, color=None):
        pass

    def on_move(self, start_x, start_y, end_x, end_y, layer, temp_layer, brush, color):
        # check which value has more to grow
        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)

        # steps - how many pixel to color
        steps = dx if dx >= dy else dy
        step_x = dx / steps if end_x >= start_x else -dx / steps
        step_y = dy / steps if end_y >= start_y else -dy / steps

        brush_radius = brush.get_radius()
        spacing = brush.get_spacing()

        space = (brush_radius * spacing)
        points = np.arange(0, steps, space)
        for i in points:
            a = start_x + step_x * i
            b = start_y + step_y * i
            self.on_press(int(a), int(b), layer, temp_layer, brush, color)

    @abstractmethod
    def on_release(self, layer=None, temp_layer=None, brush=None, color=None):
        pass