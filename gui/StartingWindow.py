from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDialog, QPushButton, QListWidget, QLabel

from dto.SelectableItem import SelectableItem
from resources import settings

from gui.components.ValueField import ValueField
from gui.components.SelectionMenu import SelectionMenu

class StartingWindow(QDialog):
    signal_initial_pulse = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        self._layout_main = QVBoxLayout()

        label = QLabel("Enter size")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout_main.addWidget(label)

        self._sizes = [
            [1280, 1024],
            [1080, 1920],
            [1920, 1080],
            [1280, 720],
            [1080, 1080],
            [100, 100]
        ]
        self._items = list()
        for i, item in enumerate(self._sizes):
            self._items.append(SelectableItem(i, f"{item[0]}x{item[1]}", None))
        self._suggested_list = SelectionMenu(
            self._items,
            self._set_from_item,
            show_name=True,
            horizontal=True
        )

        self._layout_fields = QHBoxLayout()
        self._width_field = ValueField(
            "width:",
            self._sizes[0][0],
            1,
            100000,
            step=1,
            decimals=0
        )
        self._width_field.signal_value_changed.connect(self._set_width)
        self._layout_fields.addWidget(self._width_field)

        self._height_field = ValueField(
            "height:",
            self._sizes[0][1],
            1,
            100000,
            step=1,
            decimals=0
        )
        self._height_field.signal_value_changed.connect(self._set_height)
        self._layout_fields.addWidget(self._height_field)

        self._layout_main.addWidget(self._suggested_list)
        self._layout_main.addLayout(self._layout_fields)

        button = QPushButton("Submit")
        button.clicked.connect(self._end)
        self._layout_main.addWidget(button)

        self.setLayout(self._layout_main)

    def _set_from_item(self, id: int):

        self._width_field.set_value(self._sizes[id][0])
        self._height_field.set_value(self._sizes[id][1])

    def _set_width(self, value):
        settings.layer_width = int(value)

    def _set_height(self, value):
        settings.layer_height = int(value)

    def _end(self):
        self.accept()
        self.signal_initial_pulse.emit()