import hashlib
import os

import yaml


class File:
    path: str
    title: str
    tags: list[str] = []
    sha256: str

    def __init__(self, path, title, tags=[], sha256=None):
        self.path = path
        self.title = title
        self.tags = tags

        if sha256 is None:
            with open(path, "rb") as f:
                self.sha256 = hashlib.sha256(f.read()).hexdigest()
        else:
            self.sha256 = sha256

    def __repr__(self):
        return f"File(path={self.path}, title={self.title})"


class Library:
    files: list[File] = []
    tags = []

    def __init__(self, folder):
        self.folder = folder

        if not os.path.exists(f"{folder}/.Tagify"):
            os.mkdir(os.path.join(self.folder, ".Tagify"))

        if os.path.exists(f"{folder}/.Tagify/db.yaml"):
            with open(f"{folder}/.Tagify/db.yaml", "r") as f:
                db = yaml.safe_load(f)

                if "files" not in db:
                    db["files"] = []

                if "tags" not in db:
                    db["tags"] = []

                self.files = [File(**file) for file in db["files"]]
                self.tags = db["tags"]

            self.save()

        with open(f"{folder}/.Tagify/db.yaml", "w") as f:
            yaml.safe_dump(
                {"files": [file.__dict__ for file in self.files], "tags": self.tags}, f
            )

    def add_tag(self, tag_name):
        if tag_name not in self.tags:
            self.tags.append(tag_name)
            self.save()

    def remove_tag(self, tag_name):
        self.tags = [tag for tag in self.tags if tag != tag_name]
        self.save()

    def add_file(self, file):
        self.files.append(file)
        self.save()

    def remove_file(self, file):
        self.files = [f for f in self.files if f.path != file.path]
        self.save()

    def save(self):
        with open(f"{self.folder}/.Tagify/db.yaml", "w") as f:
            yaml.safe_dump(
                {"files": [file.__dict__ for file in self.files], "tags": self.tags}, f
            )

    def add_tag_to_file(self, file, tag):
        for f in self.files:
            if f.path == file.path:
                if "tags" not in f.__dict__:
                    f.tags = []
                f.tags.append(tag)
                self.save()
                break

    def remove_tag_from_file(self, file, tag):
        for f in self.files:
            if f.path == file.path and "tags" in f.__dict__:
                f.tags.remove(tag)
                self.save()
                break

    def __repr__(self):
        return f"Library: {self.folder}, Files: {self.files}, Tags: {self.tags}"


current_library: Library = None


def open_library(folder: str):
    global current_library

    current_library = Library(folder)

    return current_library
