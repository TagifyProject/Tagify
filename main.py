# main.py
import sys

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

import lib.db as db
from lib.config import config
from widgets.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    splash = QSplashScreen(QPixmap("assets/icon.ico"))

    splash.show()

    last_library = config.library

    window = MainWindow()

    if last_library:
        db.open_library(last_library)
        window.files.update_library(db.current_library)

    window.show()

    splash.finish(window)

    sys.exit(app.exec())
