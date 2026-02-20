import os

css_dir = "assets/style_css"


def load_css(file_name):
    file_path = os.path.join(css_dir, file_name)
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"[WARNING] File CSS non trovato: {file_path}")
        return ""


def load_css_with_color(file_name, background_color):
    css = load_css(file_name)
    return css + f"\nQPushButton {{ background-color: {background_color}; }}"
