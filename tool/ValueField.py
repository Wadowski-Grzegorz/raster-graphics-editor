from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QDoubleSpinBox


class ValueField(QWidget):
    def __init__(self, text, value, min=0, max=100, suffix='%', step=1, parent=None):
        super(ValueField, self).__init__(parent)

        self._value = value
        self._text = text

        self.min = min
        self.max = max
        self.step = step

        self._moving = False
        self.old_x = 0

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel(self._text))

        self.spinbox = QDoubleSpinBox()
        self.spinbox.setValue(self._value)
        self.spinbox.setMinimum(self.min)
        self.spinbox.setMaximum(self.max)
        self.spinbox.setSuffix(suffix)
        self.spinbox.setSingleStep(self.step)
        self.spinbox.setDecimals(1)
        self.layout.addWidget(self.spinbox)

        self.spinbox.valueChanged.connect(self.value_changed)

    def value_changed(self):
        self._value = self.spinbox.value()
        print(self._value)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._moving = True
            self.old_x = e.globalPosition().x()
            self.grabMouse()

    def mouseMoveEvent(self, e):
        if self._moving:
            dx = (e.globalPosition().x() - self.old_x) * self.step
            self.old_x = e.globalPosition().x()
            new_value = min(max(self._value + dx, self.min), self.max)
            self.spinbox.setValue(new_value)

    def mouseReleaseEvent(self, e):
        self._moving = False
        self.releaseMouse()
