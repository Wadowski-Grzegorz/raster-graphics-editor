
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from gui.Canvas import Canvas
from gui.FileManager import FileManager
from gui.Menu import Menu
from gui.tool.ToolsPanelsController import ToolsPanelsController
from gui.layer.LayersPanel import LayersPanel
from controlleres.Controller import Controller
from gui.palette.Palette import Palette
from gui.starting_window import Starting_window


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('app-TION')

        self.file_manager = FileManager()
        self.setMenuBar(Menu(self, self.file_manager))

        layout = QVBoxLayout()

        canvas = Canvas()
        layout.addWidget(canvas)

        palette = Palette()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, palette)

        layers_panel = LayersPanel()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, layers_panel)

        self.tools_panels_controller = ToolsPanelsController()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.tools_panels_controller.get_tools_panel())
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.tools_panels_controller.get_tools_settings_panel())

        starting_window = Starting_window()

        self.controller = Controller(
            canvas=canvas, palette=palette, tools_panels_controller=self.tools_panels_controller, image_caretaker=self.file_manager,
            layers_panel=layers_panel,
            starting_window=starting_window
        )

        starting_window.do()

        dummy = QWidget()
        dummy.setLayout(layout)
        self.setCentralWidget(dummy)

    def dragEnterEvent(self, e):
        if e.mimeData().hasImage:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasImage:
            e.setDropAction(Qt.DropAction.CopyAction)
            file_path = e.mimeData().urls()[0].toLocalFile()
            self.file_manager.read_image_order(file_path)

            e.accept()
        else:
            e.ignore()