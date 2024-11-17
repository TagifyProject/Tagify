extensions = {
    # docuemnts
    "docx": "assets/icons/docs.png",
    "doc": "assets/icons/docs.png",
    "odt": "assets/icons/docs.png",
    "pdf": "assets/icons/pdf.png",
    # presentations
    "pptx": "assets/icons/presentation.png",
    "ppt": "assets/icons/presentation.png",
    "odp": "assets/icons/presentation.png",
    # spreadsheets
    "xlsx": "assets/icons/spreadsheet.png",
    "xls": "assets/icons/spreadsheet.png",
    "ods": "assets/icons/spreadsheet.png",
}
image_extensions = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "ico"]


def parse_file_extension(file_path):
    ext = file_path.split(".")[-1]

    if ext in extensions:
        return extensions[ext]

    if ext in image_extensions:
        return file_path

    return "assets/icons/file.png"
