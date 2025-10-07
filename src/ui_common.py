from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
)

class VBox(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

    def add_widget(self, widget, stretch=0):
        self.layout.addWidget(widget, stretch=stretch)

    def add_stretch(self, stretch):
        self.layout.addStretch(stretch)


class HBox(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)

    def add_widget(self, widget, stretch=0):
        self.layout.addWidget(widget, stretch=stretch)

    def add_stretch(self, stretch):
        self.layout.addStretch(stretch)
