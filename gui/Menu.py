from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar

from gui.FileManager import FileManager


class Menu(QMenuBar):
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