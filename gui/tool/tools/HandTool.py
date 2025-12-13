from gui.tool.tools.GuiTool import GuiTool

class HandTool(GuiTool):
    def __init__(self, canvas):
        super().__init__()
        self._name = 'Hand'
        self._canvas = canvas

    def on_press(self, x, y, layer=None):
        pass

    def on_move(self, start_x, start_y, end_x, end_y, layer=None):
        if self._canvas is None:
            return
        dx = end_x - start_x
        dy = end_y - start_y
        self._canvas.move_offset(dx, dy)

    def on_release(self, layer=None):
        pass