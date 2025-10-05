import sys
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import (
    QApplication, QWidget, QStackedWidget,
    QVBoxLayout, QGraphicsDropShadowEffect,
    QHBoxLayout, QPushButton, QSizePolicy,
    QLabel, QTextBrowser
)

from ui_common import HBox, VBox
from custom_widgets import FileDropButton, TimestampInput

from editor import Editor

# === Settings ===
# Landing Page
class LandingPage(QWidget):
    def __init__(self):
        super().__init__()
        label_container = HBox()
        label_container.setStyleSheet("font-size: 25pt; font-weight: bold;")
        label_container.add_stretch(1)
        label_container.add_widget(QLabel("Welcome to CamVAD!"), stretch=1)
        label_container.add_stretch(1)

        button_container = HBox()
        buttons = [QPushButton("Quick Start"),
                   QPushButton("Website"),
                   QPushButton("User Guide")]
        for button in buttons:
            button_container.add_widget(button, stretch=1)

        layout_0 = VBox()
        layout_0.add_widget(label_container)
        layout_0.add_widget(button_container)
        layout_0.add_widget(QTextBrowser())

        layout = QHBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(layout_0, stretch=16)
        layout.addStretch(1)

# Audio file selection page
class FileSelectionPage(QWidget):
    def __init__(self):
        super().__init__()
        audio_containers = [HBox(), HBox()]
        self.buttons = [FileDropButton("Browse or Drop\nAudio Files"),
                        FileDropButton("Browse or Drop\nAudio Files")]
        for i, audio_container in enumerate(audio_containers):
            audio_container.setStyleSheet("QLabel { max-width: 200px; }")
            audio_container.add_widget(QLabel(f"Mic for Person #{i + 1}"), stretch=1)
            audio_container.add_widget(self.buttons[i], stretch=1)
            audio_container.add_stretch(1)

        layout_0 = VBox()
        title = QLabel("Select audio files")
        title.setStyleSheet("QLabel { font-size: 18pt; font-weight: bold;}")
        layout_0.add_widget(title)
        for audio_container in audio_containers:
            layout_0.add_widget(audio_container)

        layout = QHBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(layout_0, stretch=16)
        layout.addStretch(1)

    def get_filepaths(self):
        return [button.get_path() for button in self.buttons]

# Settings for voice detection
class VADSettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        label_container = QWidget()
        label_layout = QHBoxLayout(label_container)
        overview_label = QLabel("Coming Soon")
        overview_label.setStyleSheet("font-size: 25pt; font-weight: bold;")
        label_layout.addStretch(1)
        label_layout.addWidget(overview_label, stretch=2)
        label_layout.addStretch(1)

        layout.addWidget(label_container)

# Settings for editing style
class EditorSettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        label_container = QWidget()
        label_layout = QHBoxLayout(label_container)
        overview_label = QLabel("Coming Soon")
        overview_label.setStyleSheet("font-size: 25pt; font-weight: bold;")
        label_layout.addStretch(1)
        label_layout.addWidget(overview_label, stretch=2)
        label_layout.addStretch(1)

        layout.addWidget(label_container)

# Creation page
class CreateEditPage(QWidget):
    def __init__(self, create_function):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        self.create = QPushButton("Start Editing")
        self.create.clicked.connect(create_function)
        self.create.setStyleSheet("""
            QPushButton {
                background-color: #ff6600;
                font-weight: bold;
                font-size: 22px;
                color: white;
                border-radius: 10px;
                max-width: 250px;
            }
            QPushButton:hover {
                background-color: #ff8822;
            }
        """)

        layout.addWidget(self.create)
        self.setLayout(layout)

# === Main Layout ===
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CamVAD - Automated Multicam Editor")
        self.resize(1200, 675)
        self.setStyleSheet("""
            background-color: #222;
            color: white;
            font-size: 16pt;
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 25)
        main_layout.setSpacing(0)

        logo = QSvgWidget()
        logo.load("../assets/images/logo.svg")
        logo.setStyleSheet("border: 2px solid #444; margin: 5px; border-radius: 15px;")

        # Sidebar with custom buttons
        self.sidebar = QWidget()
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(5)
        sidebar_layout.addWidget(logo, stretch=3)

        self.buttons = []
        tab_names = ["Overview",
                     "Select Files",
                     "Voice Detection",
                     "Editing Style",
                     "Create Edit"]
        for i, name in enumerate(tab_names):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.setStyleSheet(self.button_style(False))
            btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(8)
            shadow.setOffset(2, 2)
            btn.setGraphicsEffect(shadow)

            self.buttons.append(btn)
            sidebar_layout.addWidget(btn, stretch=2)

        main_layout.addWidget(self.sidebar, 1)

        # Pages
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("""
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                background-color: #333;
                """)
        self.pages.setContentsMargins(25, 25, 25, 25)

        self.pages.addWidget(LandingPage())
        self.files = FileSelectionPage()
        self.pages.addWidget(self.files)
        self.pages.addWidget(VADSettingsPage())
        self.pages.addWidget(EditorSettingsPage())
        self.pages.addWidget(CreateEditPage(self.make_edit))

        main_layout.addWidget(self.pages, stretch=5)

        self.setLayout(main_layout)
        self.switch_page(0)  # start on main page

    def button_style(self, selected):
        if selected:
            return """
            QPushButton {
                font-weight: bold;
                font-size: 22px;
                padding-left: 20px;
                background-color: #ff6600;
                color: white;
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                border-right: 2px solid #333;
            }
            """
        else:
            return """
            QPushButton {
                font-weight: bold;
                font-size: 14px;
                padding-left: 20px;
                background-color: #333;
                color: white;
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                border-right: 5px solid #222;
            }
            QPushButton:hover {
                background-color: #555;
            }
            """

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)
        # Update button styles
        for i, btn in enumerate(self.buttons):
            btn.setStyleSheet(self.button_style(i == index))
            btn.setChecked(i == index)

    def make_edit(self):
        path1, path2 = self.files.get_filepaths()
        edit = Editor(None)
        edit.load_audio(path1, path2)
        edit.process_audio()
        edit.export_cuts()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())