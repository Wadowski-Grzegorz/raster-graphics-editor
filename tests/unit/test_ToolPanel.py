import pytest

from dto.SelectableItem import SelectableItem
from gui.tool.ToolPanel import ToolPanel
from PyQt6.QtGui import QIcon

@pytest.fixture(scope='function')
def tools():
    return [
            SelectableItem(1, "brush", QIcon()),
            SelectableItem(2, "blur", QIcon()),
        ]

def test_tool_panel_emits_selected(qtbot, tools):
    tool_panel = ToolPanel(tools)
    qtbot.addWidget(tool_panel)

    item_name = 'blur'

    with qtbot.waitSignal(tool_panel.signal_tool_selected) as blocker:
        tool_panel.menu.set_current_row(item_name)

    assert blocker.args[0] == item_name

# def test_tool_panel_select(qtbot, tools):
#     tool_panel = ToolPanel(tools)
#     qtbot.addWidget(tool_panel)
#
#     item_name = 'blur'
#
#     current_row = tool_panel.menu.currentRow()
#     current_widget = tool_panel.menu.itemWidget(tool_panel.menu.item(current_row))
#
#     assert current_widget.get_name() == item_name