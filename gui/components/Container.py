from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel


class Container(QWidget):
    def __init__(self, name: str='', idx: int=0):
        super().__init__()

        self._idx = idx
        self._name = name
        self._widgets = {}

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)

    def add_widget(self, widget: QWidget, name: str):
        self._widgets[name] = widget
        self._layout.addWidget(widget)

    def set_widget_value(self, name: str, value):
        self._widgets[name].set_value_quiet(value)

    def get_name(self):
        return self._name

    def get_id(self):
        return self._idx

    def get_widgets(self):
        return self._widgets.values()

    # def sizeHint(self):
    #     w, h = 0, 0
    #     for widget in self._widgets.values():
    #         w += widget.sizeHint().width()
    #         h = max(h, widget.sizeHint().height())
    #
    #     return QSize(w, h)