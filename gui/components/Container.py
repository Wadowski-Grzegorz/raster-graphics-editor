from PyQt6.QtWidgets import QWidget, QHBoxLayout


class Container(QWidget):
    def __init__(self, name: str):
        super().__init__()

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
