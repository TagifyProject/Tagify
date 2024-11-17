import os

import yaml


class Config:
    def __init__(self):
        self.config_path = os.path.join(os.environ["APPDATA"], "Tagify", "config.yaml")
        self.library = ""
        self.api_key = ""
        self.provider = "mistral"  # Default to "mistral"
        self._ensure_config_exists()
        self._load_config()

    def _ensure_config_exists(self):
        if not os.path.exists(os.path.dirname(self.config_path)):
            os.makedirs(os.path.dirname(self.config_path))

        if not os.path.exists(self.config_path):
            with open(self.config_path, "w") as f:
                yaml.safe_dump({"library": "", "api_key": "", "provider": "mistral"}, f)

    def _load_config(self):
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)
            self.library = config.get("library", "")
            self.api_key = config.get("api_key", "")
            self.provider = config.get("provider", "mistral")

    def set_library(self, library: str):
        self.library = library
        self._save_config()

    def set_api_key(self, api_key: str):
        self.api_key = api_key
        self._save_config()

    def set_provider(self, provider: str):
        if provider in ["mistral", "g4f"]:
            self.provider = provider
            self._save_config()
        else:
            raise ValueError("Provider must be either 'mistral' or 'g4f'")

    def _save_config(self):
        with open(self.config_path, "w") as f:
            yaml.safe_dump(
                {
                    "library": self.library,
                    "api_key": self.api_key,
                    "provider": self.provider,
                },
                f,
            )


config = Config()
