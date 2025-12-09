from core.tool.CoreTool import CoreTool

class MoveTool(CoreTool):
    def __init__(self):
        super().__init__()
        self._name = 'Move'

    def on_press(self, x, y, layer=None, temp_layer=None, brush=None, color=None):
        pass

    def on_move(self, start_x, start_y, end_x, end_y, layer=None, temp_layer=None, brush=None, color=None):
        dx = end_x - start_x
        dy = end_y - start_y
        layer.move(dx, dy)

    def on_release(self, layer=None, temp_layer=None, brush=None, color=None):
        pass