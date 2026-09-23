import sys

from PyQt6.QtWidgets import QApplication

from Controller import Controller
from core.CoreApp import CoreApp
from core.EventManager import EventManager
from gui.MainWindow import MainWindow



if __name__ == "__main__":
    event_provider = EventManager()
    core = CoreApp(event_provider)

    app = QApplication(sys.argv)
    window = MainWindow(event_provider)

    control = Controller(gui=window, core=core)
    window.set_controller(control)

    window.showMaximized()
    app.exec()