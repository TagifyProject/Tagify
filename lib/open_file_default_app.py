import os
import subprocess


def open_file_with_default_app(filepath):
    if os.name == "nt":  # Windows
        os.startfile(filepath)
    elif os.name == "posix":  # Linux, macOS
        subprocess.Popen(["open", filepath])
