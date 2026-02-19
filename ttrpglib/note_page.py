from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
import os
from ttrpglib.utility.css_import import load_css


class NotePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(load_css("QWidget.css"))

        self.output_dir = "data"

        layout = QVBoxLayout(self)
        self.note_text = QTextEdit()
        self.note_text.setStyleSheet(load_css("QTextEdit.css"))
        layout.addWidget(self.note_text)

        self.note_text.setText(self.load_notes())

    def save_notes(self):
        output_file = os.path.join(self.output_dir, "note.txt")
        with open(output_file, "w") as file:
            file.write(self.note_text.toPlainText())

    def load_notes(self):
        output_file = os.path.join(self.output_dir, "note.txt")
        try:
            with open(output_file, "r") as file:
                return file.read()
        except FileNotFoundError:
            return ""
