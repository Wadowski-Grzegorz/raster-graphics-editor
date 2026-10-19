from PyQt6 import QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar

from gui.FileManager import FileManager


class Menu(QMenuBar):
    signal_undo = QtCore.pyqtSignal()
    signal_redo = QtCore.pyqtSignal()

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
        action_undo.triggered.connect(self.signal_undo.emit)
        self.addAction(action_undo)

        action_redo = QAction("&Redo", self)
        action_redo.triggered.connect(self.signal_redo.emit)
        self.addAction(action_redo)