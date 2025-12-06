
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from core.tool.ToolManager import ToolManager
from gui.Canvas import Canvas
from gui.ImageCaretaker import ImageCaretaker
from gui.layersPanel.LayersPanel import LayersPanel
from Controller import Controller
from gui.palette.Palette import Palette
from gui.starting_window import Starting_window
from gui.tool.ToolsPanel import ToolsPanel
from gui.tool.ToolsSettingsPanel import ToolsSettingsPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('app-TION')

        self.image_caretaker = ImageCaretaker()

        layout = QVBoxLayout()

        canvas = Canvas()
        layout.addWidget(canvas)

        palette = Palette()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, palette)

        layers_panel = LayersPanel()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, layers_panel)

        tools_panel = ToolsPanel()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, tools_panel)

        tool_settings_panel = ToolsSettingsPanel()
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, tool_settings_panel)

        tool_manager = ToolManager()

        starting_window = Starting_window()

        self.controller = Controller(
            canvas=canvas, palette=palette, _, image_caretaker=self.image_caretaker,
            layers_panel=layers_panel, tool_manager=tool_manager,
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
            self.image_caretaker.read_image(file_path)

            e.accept()
        else:
            e.ignore()