from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton

from core.EventManager import EventManager
from core.CoreApp import CoreApp
from gui.MainWindow import MainWindow
from Controller import Controller

from gui.components.Container import Container

def test_brush_parameter_change(qtbot):
    event = EventManager()
    core = CoreApp(event)
    gui = MainWindow(event)
    control = Controller(gui=gui, core=core)
    gui.set_controller(control)

    value_field = None
    container = gui.tool.tool_settings_panel._stacked_widgets.currentWidget()
    value_field = container._widgets['size']
    assert value_field is not None

    value_field.spinbox.setFocus()
    value_field.spinbox.clear()
    qtbot.keyClicks(value_field.spinbox, "14")
    qtbot.keyPress(value_field.spinbox, Qt.Key.Key_Enter)

    assert core.brush._curr_brush.get_size() == 14

