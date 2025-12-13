from gui.tool.tools.HandTool import HandTool

class GuiToolManager:
    def __init__(self, canvas):
        super().__init__()

        self._tools = [HandTool(canvas)]
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

    def get_tools(self):
        return self._tools.copy()

    def tool_select(self, name: str):
        for tool in self._tools:
            if tool.get_name().lower() == name.lower():
                self._curr_tool = tool
                return True
        return False