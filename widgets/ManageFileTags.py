from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from lib.db import File, Library


class ManageFileTags(QDialog):
    def __init__(self, library: Library, file: File):
        super().__init__()

        self.setWindowTitle("Manage File Tags")

        self.library = library
        self.file = file

        self.setWindowTitle("Manage File Tags")
        self.resize(400, 300)

        self.layout = QVBoxLayout()

        self.current_tags_label = QLabel("Current Tags")
        self.current_tags_list = QListWidget()
        self.available_tags_label = QLabel("Available Tags")
        self.available_tags_list = QListWidget()

        self.add_tag_btn = QPushButton("Add Tag")
        self.remove_tag_btn = QPushButton("Remove Tag")

        self.add_tag_btn.clicked.connect(self.add_tag)
        self.remove_tag_btn.clicked.connect(self.remove_tag)

        self.layout.addWidget(self.current_tags_label)
        self.layout.addWidget(self.current_tags_list)
        self.layout.addWidget(self.available_tags_label)
        self.layout.addWidget(self.available_tags_list)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.add_tag_btn)
        self.button_layout.addWidget(self.remove_tag_btn)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

        self.load_tags()

    def load_tags(self):
        self.current_tags_list.clear()
        self.available_tags_list.clear()

        for tag in self.file.tags:
            item = QListWidgetItem(tag)
            self.current_tags_list.addItem(item)

        for tag in self.library.tags:
            if tag not in self.file.tags:
                item = QListWidgetItem(tag)
                self.available_tags_list.addItem(item)

    def add_tag(self):
        selected_items = self.available_tags_list.selectedItems()
        for item in selected_items:
            tag = item.text()
            self.library.add_tag_to_file(self.file, tag)
        self.load_tags()

    def remove_tag(self):
        selected_items = self.current_tags_list.selectedItems()
        for item in selected_items:
            tag = item.text()
            self.library.remove_tag_from_file(self.file, tag)
        self.load_tags()
