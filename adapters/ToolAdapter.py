import json

from PyQt6.QtGui import QIcon

from core.tool.Tool import Tool
from dto.SelectableItem import SelectableItem

import resources.settings as settings

class ToolAdapter:
    tools_icons_catalog = settings.program_catalog + "\\resources\\icons\\"
    tools_info_file = settings.program_catalog + "\\resources\\info\\tools.json"

    @staticmethod
    def tool_to_selectable(t: Tool) -> SelectableItem:
        with open(ToolAdapter.tools_info_file, 'r', encoding="utf-8") as f:
            data = json.load(f)

        icon_path = ToolAdapter.tools_icons_catalog + data[t.get_name().lower()]

        return SelectableItem(t.get_idx(), t.get_name(), QIcon(icon_path))

    @staticmethod
    def tools_to_selectable(tools: list[Tool]) -> list[SelectableItem]:
        return [ToolAdapter.tool_to_selectable(tool) for tool in tools]

    # @staticmethod
    # def get_tools_selectable() -> list[SelectableItem]:
    #     core_tools = core_tool_manager.get_tools()
    #     gui_tools = gui_tool_manager.get_tools()
    #     return ToolAdapter.tools_to_selectable(core_tools) + ToolAdapter.tools_to_selectable(gui_tools)