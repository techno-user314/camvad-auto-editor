from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import (
    QFileDialog, QSpinBox, QWidget,
    QVBoxLayout, QPushButton,
    QSizePolicy, QLabel, QFormLayout,
)

class FileDropButton(QPushButton):
    def __init__(self, text="Drop a file here"):
        super().__init__(text)
        self.setAcceptDrops(True)
        self.setMinimumSize(250, 150)
        self.setMaximumSize(350, 225)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setStyleSheet("""
            QPushButton {
                border: 2px dashed #aaa;
                border-radius: 15px;
                background-color: #222;
                color: #ccc;
                font-size: 16px;
            }
            QPushButton:hover {
                border-color: #ff6600;
                color: white;
            }
        """)

        # Store the selected file path
        self.file_path = None

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            self.file_path = urls[0].toLocalFile()
            self.setText(f"Selected:\n{self.file_path.split('/')[-1]}")

    def mousePressEvent(self, event):
        # Allow clicking to open file dialog
        if event.button() == Qt.MouseButton.LeftButton:
            file_dialog = QFileDialog()
            path, _ = file_dialog.getOpenFileName(self, "Select File")
            if path:
                self.file_path = path
                self.setText(f"Selected:\n{self.file_path.split('/')[-1]}")
        super().mousePressEvent(event)

    def get_path(self):
        return self.file_path

class TimestampInput(QWidget):
    def __init__(self):
        super().__init__()
        self.setMaximumSize(250, 400)
        self.setStyleSheet("""
            QSpinBox {
                background-color: #222;
                border-radius: 2px;
                font-size: 14pt;
            }
        """)

        top_layout = QVBoxLayout()
        label_time = QLabel("Start processing file\nat timestamp: ")

        timestamp = QWidget()
        time_layout = QFormLayout()

        self.min_input = QSpinBox()
        self.min_input.setMinimum(0)
        self.min_input.setMaximum(59)
        self.min_input.setValue(0)

        self.sec_input = QSpinBox()
        self.sec_input.setMinimum(0)
        self.sec_input.setMaximum(59)
        self.sec_input.setValue(0)

        time_layout.addRow("Minutes", self.min_input)
        time_layout.addRow("Seconds", self.sec_input)
        timestamp.setLayout(time_layout)

        top_layout.addWidget(label_time)
        top_layout.addWidget(timestamp)
        self.setLayout(top_layout)