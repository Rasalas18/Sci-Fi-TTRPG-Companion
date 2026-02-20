import os
import json
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton,
)
from PyQt5.QtCore import QSize
from ttrpglib.utility.css_import import load_css, load_css_with_color


class AttrTable(QWidget):
    def __init__(self):
        super().__init__()
        self.output_dir = "data"
        self.button_state = self.load_attr()
        self.buttons = [[None for _ in range(6)] for _ in range(4)]
        self.initUI()
        self.setStyleSheet(load_css("QWidget.css"))

    def initUI(self):
        attr_layout = QVBoxLayout()
        attr_layout.setContentsMargins(40, 0, 40, 0)
        attr_layout.setSpacing(30)

        label_texts = ["Strength", "Agility", "Intelligence", "Willpower"]
        attr_values = ["-2", "-1", "0", "1", "2", "3"]

        for i, text in enumerate(label_texts):
            frame = QFrame(self)
            attr_label = QLabel(text, self)
            attr_label.setStyleSheet("color: white; font-size: 12pt")

            button_layout = QHBoxLayout()
            button_layout.addWidget(attr_label)

            for j, value in enumerate(attr_values):
                button = QPushButton(f"{value}", self)
                button.clicked.connect(
                    lambda _, row=i, col=j: self.attr_button_click(row, col)
                )
                button.setFixedSize(QSize(50, 50))
                button_layout.addWidget(button)
                self.buttons[i][j] = button
                self.attr_update_button_color(button, i, j)

            frame.setLayout(button_layout)
            attr_layout.addWidget(frame)

        self.setLayout(attr_layout)

    def attr_button_click(self, row, col):
        self.button_state[row][col] = not self.button_state[row][col]
        self.attr_update_button_color(self.buttons[row][col], row, col)

    def attr_update_button_color(self, button, row, col):
        if self.button_state[row][col]:
            button.setStyleSheet(load_css_with_color("QButton_attr.css", "green"))
        else:
            button.setStyleSheet(load_css_with_color("QButton_attr.css", "black"))

    def save_attr(self):
        output_file = os.path.join(self.output_dir, "attr.json")
        with open(output_file, "w") as f:
            json.dump({"attributes": self.button_state}, f)

    def load_attr(self):
        output_file = os.path.join(self.output_dir, "attr.json")
        try:
            with open(output_file, "r") as f:
                data = json.load(f)
                return data["attributes"]
        except FileNotFoundError:
            return [[False for _ in range(6)] for _ in range(4)]
