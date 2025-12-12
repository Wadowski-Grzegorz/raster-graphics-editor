from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit


class EditableName(QWidget):
    def __init__(self, name="", fun=None, idx=None):
        super().__init__()
        self.fun = fun
        self.idx = idx
        self.layout = QVBoxLayout(self)
        self.editable_line = QLineEdit(name)
        self.editable_line.setReadOnly(True)
        self.layout.addWidget(self.editable_line)

        self.editable_line.mousePressEvent = self.editing_start
        self.editable_line.editingFinished.connect(self.editing_end)

        self.setStyleSheet("""
            background: transparent;
            border: none;
            padding: 0px;
        """)

    def editing_start(self, event):
        self.editable_line.setReadOnly(False)
        self.editable_line.setFocus()
        self.editable_line.selectAll()

    def editing_end(self):
        self.editable_line.setReadOnly(True)
        text = self.editable_line.text()

        if self.fun:
            if self.idx:
                self.fun(self.idx, text)
            else:
                self.fun()
