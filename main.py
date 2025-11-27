import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from core.Paint import Paint
from gui.Canvas import Canvas
from gui.LayersPanel import LayersPanel
from data.Layers import Layers
from Controller import Controller
from gui.palette.Palette import Palette
from gui.starting_window import Starting_window
from gui.tool.ToolsPanel import ToolsPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('app-TION')

        layout = QVBoxLayout()

        layers = Layers()

        canvas = Canvas(layers)
        layout.addWidget(canvas)

        palette = Palette()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, palette)

        layers_panel = LayersPanel(layers)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, layers_panel)

        tools_panel = ToolsPanel()
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, tools_panel)

        paint = Paint()

        starting_window = Starting_window()

        self.controller = Controller(canvas=canvas, palette=palette, tools_panel=tools_panel,
                                     layers=layers, layers_panel=layers_panel, paint=paint,
                                     starting_window=starting_window)

        starting_window.do()

        dummy = QWidget()
        dummy.setLayout(layout)
        self.setCentralWidget(dummy)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    app.exec()