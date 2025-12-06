import json

from PyQt6.QtGui import QIcon

from core.tool.Tool import Tool
from dto.SelectableItem import SelectableItem
from core.tool.ToolManager import tool_manager

import resources.settings as settings

class ToolAdapter:
    tools_icons_catalog = settings.program_catalog + "\\resources\\tools\\icons\\"
    tools_file = settings.program_catalog + "\\resources\\tools\\tool.json"

    @staticmethod
    def tool_to_selectable(t: Tool) -> SelectableItem:
        with open(ToolAdapter.tools_file, 'r', encoding="utf-8") as f:
            data = json.load(f)
        tool = data[t.get_name()]

        icon_path = ToolAdapter.tools_icons_catalog + tool['icon_file']
        print('icon_path: ', icon_path)

        return SelectableItem(0, t.get_name(), QIcon(icon_path))

    @staticmethod
    def tools_to_selectable(tools: list[Tool]) -> list[SelectableItem]:
        return [ToolAdapter.tool_to_selectable(tool) for tool in tools]

    @staticmethod
    def get_tools_selectable() -> list[SelectableItem]:
        core_tools = tool_manager.get_tools()
        return ToolAdapter.tools_to_selectable(core_tools)


tool_adapter = ToolAdapter()