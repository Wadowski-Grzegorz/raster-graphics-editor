from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from gui.Canvas import Canvas
from gui.FileManager import FileManager
from gui.Menu import Menu
from gui.tool.ToolPanelsManager import ToolPanelsManager
from gui.layer.LayerPanel import LayerPanel
from gui.palette.Palette import Palette
from gui.StartingWindow import StartingWindow


class MainWindow(QMainWindow):
    def __init__(self, event_provider):
        super().__init__()
        self.event_provider = event_provider
        self._controller = None

        self.setWindowTitle('raster graphics editor')
        self.layout = QVBoxLayout()

        self.file_manager = FileManager()
        self.setMenuBar(Menu(self, self.file_manager))


        self.canvas = Canvas(event_provider)
        self.layout.addWidget(self.canvas)

        self.palette = Palette()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.palette)

        self.layer_panel = LayerPanel(event_provider)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.layer_panel)

        self.tool = ToolPanelsManager(event_provider, self.canvas)
        self.starting_window = StartingWindow()

        self.dummy = QWidget()
        self.dummy.setLayout(self.layout)
        self.setCentralWidget(self.dummy)

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

    def set_controller(self, controller):
        self._controller = controller
        self.file_manager.set_controller(controller)
        self.canvas.set_controller(controller)
        self.tool.set_controller(controller)
        self.layer_panel.set_controller(controller)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.tool.get_tool_panel())
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.tool.get_tool_settings_panel())
        self.starting_window.do()