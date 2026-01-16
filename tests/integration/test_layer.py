from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QPushButton

from core.EventManager import EventManager
from core.CoreApp import CoreApp
from gui.MainWindow import MainWindow
from Controller import Controller

def test_layer_create(qtbot):
    event = EventManager()
    core = CoreApp(event)
    gui = MainWindow(event)
    control = Controller(gui=gui, core=core)
    gui.set_controller(control)

    layer_len = len(core.layer._layers)

    button_add_layer = None
    for i in range(gui.layer_panel.layout_options.count()):
        w = gui.layer_panel.layout_options.itemAt(i).widget()
        if isinstance(w, QPushButton) and w.text() == 'Add Layer':
            button_add_layer = w
            break
    assert button_add_layer is not None

    qtbot.mouseClick(button_add_layer, QtCore.Qt.MouseButton.LeftButton)
    assert len(core.layer._layers) == layer_len + 1