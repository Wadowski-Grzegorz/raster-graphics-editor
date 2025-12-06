from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QDoubleSpinBox


class ValueField(QWidget):
    signal_value_changed = pyqtSignal(float)

    def __init__(self, text, value=1, min_v=0, max_v=100, suffix='', step=0.5):
        super().__init__()

        self._value = value
        self._text = text

        self.min_v = min_v
        self.max_v = max_v
        self.step = step

        self._moving = False
        self.old_x = 0

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel(self._text))

        self.spinbox = QDoubleSpinBox()
        self.spinbox.setValue(self._value)
        self.spinbox.setMinimum(self.min_v)
        self.spinbox.setMaximum(self.max_v)
        self.spinbox.setSuffix(suffix)
        self.spinbox.setSingleStep(self.step)
        self.spinbox.setDecimals(1)
        self.layout.addWidget(self.spinbox)

        self.spinbox.valueChanged.connect(self.value_changed)

    def value_changed(self, v):
        self._value = v
        self.signal_value_changed.emit(v)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._moving = True
            self.old_x = e.globalPosition().x()
            self.grabMouse()

    def mouseMoveEvent(self, e):
        if self._moving:
            dx = (e.globalPosition().x() - self.old_x) * self.step
            self.old_x = e.globalPosition().x()
            new_value = min(max(self._value + dx, self.min_v), self.max_v)
            self.spinbox.setValue(new_value)

    def mouseReleaseEvent(self, e):
        self._moving = False
        self.releaseMouse()

    def set_value_quiet(self, value):
        self.spinbox.blockSignals(True)
        self.spinbox.setValue(value)
        self.spinbox.blockSignals(False)

    def get_name(self):
        return self._text