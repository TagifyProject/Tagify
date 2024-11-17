from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QSizePolicy, QMenu
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

from lib.open_file_default_app import open_file_with_default_app
from lib.parse_file_extension import parse_file_extension
from lib.db import File

import lib.db as db
import subprocess
from widgets.ManageFileTags import ManageFileTags


class Thumbnail(QWidget):
    def __init__(self, file: File):
        super().__init__()

        self.filename = file.path
        self.title = file.title
        self.file = file

        self.main_layout = QVBoxLayout()

        self.thumbnail_img = QImage(parse_file_extension(self.filename))
        self.thumbnail_img = self.thumbnail_img.scaled(
            70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        self.rightClickMenu = QMenu()

        self.rightClickMenu.addAction("Open in explorer").triggered.connect(
            self.open_in_explorer
        )
        self.rightClickMenu.addAction("Remove from Tagify").triggered.connect(
            self.remove_file
        )
        self.rightClickMenu.addAction("Manage Tags").triggered.connect(self.manage_tags)

        self.image_label = QLabel()
        self.image_label.setObjectName("thumbnailImage")
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.image_label.setFixedSize(100, 100)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(QPixmap.fromImage(self.thumbnail_img))

        if len(self.title) > 10:
            self.title = self.title[:10] + "..."

        self.title_label = QLabel(self.title)
        self.title_label.setMaximumWidth(100)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.title_label)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setLayout(self.main_layout)

    def mouseDoubleClickEvent(self, event):
        open_file_with_default_app(self.filename)
        return super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        self.rightClickMenu.exec(event.globalPos())
        return super().contextMenuEvent(event)

    def open_in_explorer(self):
        command = f'explorer /select,"{self.filename.replace("/", "\\")}"'
        subprocess.run(command, shell=True)

    def remove_file(self):
        db.current_library.remove_file(self.file)
        self.close()

    def manage_tags(self):
        self.manageTags = ManageFileTags(library=db.current_library, file=self.file)
        self.manageTags.exec()
