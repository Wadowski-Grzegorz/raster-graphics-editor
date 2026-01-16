from unittest.mock import MagicMock

from Controller import Controller

def test_controller_core_tool_selected(qtbot):
    mock_gui = MagicMock()
    mock_gui_tool = MagicMock()
    mock_gui.tool = mock_gui_tool
    mock_gui_tool.tool_select.return_value = True

    mock_core = MagicMock()
    mock_core_tool = MagicMock()
    mock_core.tool = mock_core_tool
    mock_core_tool.tool_select.return_value = False

    controller = Controller(gui=mock_gui, core=mock_core)

    controller.tool_select('hand')
    assert controller._current_manager == mock_gui_tool