from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import lib.db as db
from widgets.FlowLayout import FlowLayout
from widgets.Thumbnail import Thumbnail


class Files(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)  # Minimize spacing between elements
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Header section
        self.header_layout = QVBoxLayout()
        self.header_layout.setSpacing(10)  # Spacing between header elements

        self.newLibraryDialog = QFileDialog(caption="Select folder")
        self.newLibraryDialog.setFileMode(QFileDialog.FileMode.Directory)
        self.newLibraryDialog.fileSelected.connect(self.add_library)

        self.large_font = QFont()
        self.large_font.setPointSize(16)

        # Search section
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter by tags")
        self.filter_input.setFont(self.large_font)

        self.search_button = QPushButton("Filter")
        self.search_button.setFont(self.large_font)
        self.search_button.clicked.connect(self.filter_files)

        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.filter_input)
        self.search_layout.addWidget(self.search_button)

        self.header_layout.addLayout(self.search_layout)

        # Content section with FlowLayout
        self.content_widget = QWidget()
        self.flow_layout = FlowLayout()
        self.flow_layout.setSpacing(10)
        self.content_widget.setLayout(self.flow_layout)

        # Main layout assembly
        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.content_widget, 1)  # Add stretch factor

        self.setLayout(self.layout)

    def add_library(self, folder: str):
        library = db.open_library(folder)
        self.update_library(library)

    def update_library(self, library):
        for i, file in enumerate(library.files):
            thumbnail = Thumbnail(file)
            self.flow_layout.addWidget(thumbnail)

    def refresh_view(self):
        for i in reversed(range(self.flow_layout.count())):
            widget = self.flow_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for file in db.current_library.files:
            thumbnail = Thumbnail(file)
            self.flow_layout.addWidget(thumbnail)

    def filter_files(self):
        filter_text = self.filter_input.text().lower()
        for i in range(self.flow_layout.count()):
            widget = self.flow_layout.itemAt(i).widget()
            if isinstance(widget, Thumbnail):
                if filter_text == "":
                    widget.setVisible(True)
                else:
                    file_tags = [
                        tag.lower() for tag in widget.file.__dict__.get("tags", [])
                    ]
                    widget.setVisible(filter_text in file_tags)
