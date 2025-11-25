import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from gui.Canvas import Canvas
from gui.Palette import Palette
from gui.Layers_panel import Layers_panel
from data.Layers import Layers
from Controller import Controller
from gui.tool.Tools_panel import Tools_panel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('app-TION')

        layout = QVBoxLayout()

        layers = Layers()

        canvas = Canvas()
        layout.addWidget(canvas)

        palette = Palette()
        layout.addLayout(palette)

        layers_panel = Layers_panel()
        tools_panel = Tools_panel()

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, layers_panel)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, tools_panel)

        self.controller = Controller(canvas=canvas, palette=palette,
                                layers=layers, layers_panel=layers_panel)
        dummy = QWidget()
        dummy.setLayout(layout)

        self.setCentralWidget(dummy)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    app.exec()