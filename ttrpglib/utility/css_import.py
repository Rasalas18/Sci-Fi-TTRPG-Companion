import os

css_dir = "assets/style_css"


def load_css(file_name):
    file_path = os.path.join(css_dir, file_name)
    with open(file_path, "r") as file:
        return file.read()
