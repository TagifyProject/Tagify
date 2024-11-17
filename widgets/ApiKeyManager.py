from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from lib.config import config


class ApiKeyManager(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("API Key Manager")

        self.layout = QVBoxLayout()

        self.provider = QComboBox()
        self.provider.addItems(["Mistral.AI", "G4F"])
        self.provider.currentIndexChanged.connect(self.save_provider)

        self.api_key_label = QLabel("API Key:")
        self.api_key_input = QLineEdit(config.api_key)

        self.api_key_layout = QHBoxLayout()
        self.api_key_layout.addWidget(self.api_key_label)
        self.api_key_layout.addWidget(self.api_key_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_key)

        self.layout.addWidget(self.provider)
        self.layout.addLayout(self.api_key_layout)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def save_provider(self):
        provider = self.provider.currentIndex()

        if provider == 0:
            provider = "mistral"
        else:
            provider = "g4f"

        config.set_provider(provider)

    def save_key(self):
        key = self.api_key_input.text()

        if not key and self.provider.currentIndex() == 0:
            QMessageBox.critical(self, "Error", "API Key cannot be empty")

            return

        config.set_api_key(key)

        self.close()
