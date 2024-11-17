# widgets/MenuActions.py
import os

from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)

import lib.db as db
from lib.config import config
from lib.db import File
from lib.generate_tags import generate_tags
from widgets.ApiKeyManager import ApiKeyManager
from widgets.ManageTags import ManageTags


class TaggingOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Tagging Options")

        self.setWindowTitle("Tagging Options")
        self.layout = QVBoxLayout()

        self.ai_tagging_checkbox = QCheckBox("Enable AI Tagging")
        self.ai_tagging_checkbox.setChecked(True)  # Default to enabled

        self.layout.addWidget(self.ai_tagging_checkbox)

        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def is_ai_tagging_enabled(self):
        return self.ai_tagging_checkbox.isChecked()


class MenuActions:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ai_tagging_enabled = True
        self.main_window.apiKeyManager = ApiKeyManager()

    def open_api_key_manager(self):
        self.main_window.apiKeyManager.exec()

    def open_manage_tags(self):
        if db.current_library:
            self.main_window.manageTags = ManageTags(library=db.current_library)
            self.main_window.manageTags.exec()

    def open_library(self):
        dialog = QFileDialog(caption="Select folder")
        dialog.setFileMode(QFileDialog.FileMode.Directory)

        if dialog.exec():
            folder = dialog.selectedFiles()[0]
            library = db.open_library(folder)
            self.main_window.files.update_library(library)
            config.set_library(folder)

    def open_file_dialog(self):
        if db.current_library:
            options_dialog = TaggingOptionsDialog(self.main_window)

            if config.api_key or config.provider == "g4f":
                if options_dialog.exec():
                    self.ai_tagging_enabled = options_dialog.is_ai_tagging_enabled()
                    self.main_window.fileDialog.exec()
            else:
                self.ai_tagging_enabled = False
                self.main_window.fileDialog.exec()

    def open_folder_dialog(self):
        if db.current_library:
            self.main_window.scanFolderDialog.exec()

    def add_file(self, filename: str):
        file = File(filename, os.path.basename(filename))

        for existing in db.current_library.files:
            if existing.path == file.path:
                return

            if existing.sha256 == file.sha256:
                return

        # Check if AI tagging is enabled
        if self.ai_tagging_enabled:
            file.tags = generate_tags(filename)
        else:
            file.tags = []

        db.current_library.add_file(file)
        self.main_window.files.refresh_view()

    def scan_folder(self, folder: str):
        files = os.listdir(folder)
        for file in files:
            print(f"Found file: {file}")
