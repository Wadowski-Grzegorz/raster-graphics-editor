from unittest.mock import MagicMock

from core.tool.CoreToolManager import CoreToolManager

import numpy as np


def test_tool_used():
    mock_event = MagicMock()
    mock_tool = MagicMock()
    layer = MagicMock()
    temp_layer = MagicMock()
    brush = MagicMock()
    color = np.array([10, 55, 0, 255], dtype="uint8")

    tool_manager = CoreToolManager(event=mock_event)
    tool_manager._curr_tool = mock_tool
    tool_manager._curr_layer = layer
    tool_manager._temp_layer = temp_layer
    tool_manager._curr_brush = brush
    tool_manager._curr_color = color

    tool_manager.on_press(4, 4)

    mock_tool.on_press.assert_called_once_with(
        4, 4,
        layer=layer,
        temp_layer=temp_layer,
        brush=brush,
        color=color
    )

    mock_event.notify.assert_called_once_with(
        { "type": "paint_painted", "layer": layer }
    )