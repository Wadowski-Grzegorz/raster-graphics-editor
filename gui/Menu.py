from PyQt6 import QtCore
from PyQt6.QtGui import QAction, QKeySequence, QIcon
from PyQt6.QtWidgets import QMenuBar

from gui.FileManager import FileManager

import resources.settings as settings


class Menu(QMenuBar):
    signal_undo = QtCore.pyqtSignal()
    signal_redo = QtCore.pyqtSignal()

    icons_catalog = settings.program_catalog + "\\resources\\icons\\"

    def __init__(self, parent, file_manager: FileManager):
        super().__init__(parent)
        self._file_manager = file_manager

        self._file_menu = self.addMenu("&File")

        action_save = QAction("&Save", self)
        action_save.triggered.connect(self._file_manager.save_file)
        self._file_menu.addAction(action_save)

        action_open = QAction("&Open", self)
        action_open.triggered.connect(self._file_manager.open_file)
        self._file_menu.addAction(action_open)


        action_undo = QAction("&Undo", self)
        action_undo.setShortcut(QKeySequence.StandardKey.Undo)
        action_undo.setIcon(QIcon(self.icons_catalog + "menu_undo.png"))
        action_undo.triggered.connect(self.signal_undo.emit)
        self.addAction(action_undo)

        action_redo = QAction("&Redo", self)
        action_redo.setShortcut(QKeySequence.StandardKey.Redo)
        action_redo.setIcon(QIcon(self.icons_catalog + "menu_redo.png"))
        action_redo.triggered.connect(self.signal_redo.emit)
        self.addAction(action_redo)