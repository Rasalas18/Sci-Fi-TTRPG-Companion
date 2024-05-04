import os
import json
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QLabel,
    QPushButton,
)
from PyQt5.QtCore import QSize
from ttrpglib.utility.css_import import load_css


class Attr_Table(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet(load_css("QWidget.css"))

    def initUI(self):

        global output_dir, button_state, buttons

        output_dir = "data"
        button_state = load_attr()

        buttons = [[None for _ in range(6)] for _ in range(4)]

        # Layout principale verticale
        attr_layout = QVBoxLayout()
        attr_layout.setContentsMargins(40, 0, 40, 0)
        attr_layout.setSpacing(30)

        label_texts = ["Strength", "Agility", "Intelligence", "Willpower"]
        attr_values = ["-2", "-1", "0", "1", "2", "3"]

        # Aggiungi 4 frame allineati verticalmente
        for text in label_texts:
            i = label_texts.index(text)

            frame = QFrame(self)

            attr_label = QLabel(text, self)
            attr_label.setStyleSheet("color: white; font-size: 12pt")

            button_layout = QHBoxLayout()
            button_layout.addWidget(attr_label)

            for value in attr_values:
                j = attr_values.index(value)
                button = QPushButton(f"{value}", self)
                button.clicked.connect(
                    lambda _, row=i, col=j: self.attr_button_click(row, col)
                )
                button.setFixedSize(QSize(50, 50))
                button_layout.addWidget(button)
                buttons[i][j] = button

                self.attr_update_button_color(button, i, j)

            frame.setLayout(button_layout)
            attr_layout.addWidget(frame)

        self.setLayout(attr_layout)
        self.setWindowTitle("QtWidget con Frames e Pulsanti")

    def attr_button_click(self, row, col):
        global button_state
        button_state[row][col] = not button_state[row][col]
        self.attr_update_button_color(buttons[row][col], row, col)

    def attr_update_button_color(self, button, row, col):

        if button_state[row][col]:
            button.setStyleSheet(load_css("QButton_attr_green.css"))
        else:
            button.setStyleSheet(load_css("QButton_attr_black.css"))


def save_attr():
    output_file = os.path.join(output_dir, "attr.json")
    with open(output_file, "w") as f:
        json.dump({"attributes": button_state}, f)


def load_attr():
    output_file = os.path.join(output_dir, "attr.json")
    try:
        with open(output_file, "r") as f:
            data = json.load(f)
            return data["attributes"]
    except FileNotFoundError:
        return [[False for _ in range(6)] for _ in range(4)]
