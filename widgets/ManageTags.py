from PySide6.QtWidgets import QDialog, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout

from lib.db import Library
from widgets.FlowLayout import FlowLayout


class ManageTags(QDialog):
    def __init__(self, library: Library):
        super().__init__()

        self.setWindowTitle("Manage Tags")

        self.library = library

        self.layout = QVBoxLayout()
        self.tags = FlowLayout()

        self.input_box_layout = QHBoxLayout()

        self.resize(400, 200)

        self.input_box = QLineEdit()
        self.add_tag_btn = QPushButton("+")

        self.input_box_layout.addWidget(self.input_box)
        self.input_box_layout.addWidget(self.add_tag_btn)

        self.add_tag_btn.clicked.connect(self.add_tag)

        tags = self.library.tags

        for tag in tags:
            tag_button = QPushButton(tag)
            tag_button.clicked.connect(lambda _, t=tag: self.remove_tag(t))
            self.tags.addWidget(tag_button)

        self.layout.addLayout(self.input_box_layout)
        self.layout.addLayout(self.tags)

        self.setLayout(self.layout)

    def add_tag(self):
        tag = self.input_box.text()
        if tag:
            self.library.add_tag(tag.lower())

            tag_button = QPushButton(tag)
            tag_button.clicked.connect(lambda _, t=tag: self.remove_tag(t))
            self.tags.addWidget(tag_button)
            self.input_box.clear()

    def remove_tag(self, tag):
        if self.file:
            self.library.remove_tag_from_file(self.file, tag)
        else:
            self.library.remove_tag(tag)
        for i in range(self.tags.count()):
            widget = self.tags.itemAt(i).widget()
            if widget.text() == tag:
                widget.setParent(None)
                break
