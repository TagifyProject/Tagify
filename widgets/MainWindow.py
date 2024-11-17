# main_window.py
from PySide6.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QFileDialog,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtGui import QIcon, QAction

from widgets.Files import Files
from widgets.About import About
from widgets.MenuActions import MenuActions


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = QWidget()

        with open("assets/stylesheet.qss", "r") as f:
            self.widget.setStyleSheet(f.read())

        self.setWindowTitle("Tagify")
        icon = QIcon("assets/icon.ico")
        self.setWindowIcon(icon)
        self.resize(1300, 720)

        self.menubar = QMenuBar()

        self.file_menu = self.menubar.addMenu("File")
        self.edit_menu = self.menubar.addMenu("Edit")
        self.help_menu = self.menubar.addMenu("Help")

        self.manage_tags_action = QAction("Manage Tags", self)
        self.manage_tags_action.triggered.connect(self.open_manage_tags)
        self.edit_menu.addAction(self.manage_tags_action)

        self.open_library_action = QAction("Open Library", self)
        self.open_library_action.triggered.connect(self.open_library)
        self.file_menu.addAction(self.open_library_action)

        self.add_file_action = QAction("Add File", self)
        self.add_file_action.triggered.connect(self.open_file_dialog)
        self.file_menu.addAction(self.add_file_action)

        self.scan_folder_action = QAction("Scan Folder", self)
        self.scan_folder_action.triggered.connect(self.open_folder_dialog)
        self.file_menu.addAction(self.scan_folder_action)

        self.api_key_manager_action = QAction("API Key Manager", self)
        self.api_key_manager_action.triggered.connect(self.open_api_key_manager)
        self.edit_menu.addAction(self.api_key_manager_action)

        self.about_action = QAction("About", self)
        self.about = About()
        self.about_action.triggered.connect(self.about.exec)
        self.help_menu.addAction(self.about_action)

        self.setMenuBar(self.menubar)

        self.layout = QHBoxLayout()

        self.files = Files()

        self.layout.addWidget(self.files)

        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

        self.fileDialog = QFileDialog(caption="Select file")
        self.fileDialog.fileSelected.connect(self.add_file)

        self.scanFolderDialog = QFileDialog(caption="Select folder")
        self.scanFolderDialog.fileSelected.connect(self.scan_folder)
        self.scanFolderDialog.setFileMode(QFileDialog.FileMode.Directory)

        self.menu_actions = MenuActions(self)

    def open_api_key_manager(self):
        self.menu_actions.open_api_key_manager()

    def open_manage_tags(self):
        self.menu_actions.open_manage_tags()

    def open_library(self):
        self.menu_actions.open_library()

    def open_file_dialog(self):
        self.menu_actions.open_file_dialog()

    def open_folder_dialog(self):
        self.menu_actions.open_folder_dialog()

    def add_file(self, filename: str):
        self.menu_actions.add_file(filename)

    def scan_folder(self, folder: str):
        self.menu_actions.scan_folder(folder)
