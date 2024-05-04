from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
import os
from ttrpglib.utility.css_import import load_css


class NotePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(load_css("QWidget.css"))

        global output_dir, note

        output_dir = "data"

        layout = QVBoxLayout(self)
        self.note_text = QTextEdit()
        self.note_text.textChanged.connect(self.update_notes)
        self.note_text.setStyleSheet(load_css("QTextEdit.css"))
        layout.addWidget(self.note_text)

        note = load_notes()
        self.note_text.setText(note)

    def update_notes(self):
        global saved_note
        saved_note = self.note_text.toPlainText()


def save_notes():
    output_file = os.path.join(output_dir, "note.txt")
    with open(output_file, "w") as file:
        file.write(saved_note)


def load_notes():
    output_file = os.path.join(output_dir, "note.txt")
    try:
        with open(output_file, "r") as file:
            loaded_note = file.read()
            return loaded_note
    except FileNotFoundError:
        return ""
