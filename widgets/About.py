from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout


class About(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")

        self.layout = QVBoxLayout()

        self.resize(300, 200)

        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("assets/logo_optimized.png"))
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.large_font = QFont()
        self.large_font.setPointSize(20)

        self.projectName = QLabel("Tagify")
        self.projectName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.projectName.setFont(self.large_font)

        self.author = QLabel("Made with ❤️ and 🐍 by JustZvan")
        self.author.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.license_text = QLabel(
            "This project is licensed under the GNU General Public License v3.0"
        )

        self.layout.addWidget(self.logo)
        self.layout.addWidget(self.projectName)
        self.layout.addWidget(self.author)
        self.layout.addWidget(self.license_text)

        self.setLayout(self.layout)
