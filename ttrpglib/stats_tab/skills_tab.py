import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox
from ttrpglib.utility.css_import import load_css


class SkillTable(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet(load_css("QWidget.css"))

    def initUI(self):

        global checkboxes_states, checkboxes, output_dir

        output_dir = "data"

        checkboxes_states = load_skills()
        checkboxes = [None for _ in range(25)]

        main_layout = QHBoxLayout()

        skill_layout1 = QVBoxLayout()
        skills1 = [
            "Acrobatics",
            "Alien",
            "Athletics",
            "Constitution",
            "Diplomacy",
            "Drive",
            "Engineering",
            "Gambling",
            "Hacking",
            "History",
            "Insight",
        ]
        index = 0
        for i, skill in enumerate(skills1):
            checkbox = QCheckBox(skill)  # Collega la funzione di gestione dello stato
            checkbox.setStyleSheet(load_css("QCheckBox.css"))
            checkbox.clicked.connect(lambda _, pos=i: self.update_checkbox(pos))
            skill_layout1.addWidget(checkbox)
            checkboxes[i] = checkbox

            if checkboxes_states[i] is True:
                checkboxes[i].setChecked(True)
                # checkboxes[i].setStyleSheet(load_css("QCheckBox.css"))
            index = i

        main_layout.addLayout(skill_layout1)

        # Layout per le skill group 2
        skill_layout2 = QVBoxLayout()
        skills2 = [
            "Languages",
            "Manipulation",
            "Medic",
            "Melee",
            "Perception",
            "Performance",
            "Pilot",
            "Religion",
            "Science",
            "Shooting",
            "Sleight of Hand",
            "Stealth",
            "Survival",
            "Tech",
        ]
        for j, skill in enumerate(skills2):
            k = j + index + 1
            checkbox = QCheckBox(skill)  # Collega la funzione di gestione dello stato
            checkbox.setStyleSheet(load_css("QCheckBox.css"))
            checkbox.clicked.connect(lambda _, pos=k: self.update_checkbox(pos))
            skill_layout2.addWidget(checkbox)
            checkboxes[k] = checkbox

            if checkboxes_states[k] is True:
                checkboxes[k].setChecked(True)
                # checkboxes[k].setStyleSheet(load_css("QCheckBox.css"))

        main_layout.addLayout(skill_layout2)

        self.setLayout(main_layout)

    def update_checkbox(self, pos):
        global checkboxes_states
        checkboxes_states[pos] = not checkboxes_states[pos]


def save_skills():
    output_file = os.path.join(output_dir, "skills.json")
    with open(output_file, "w") as f:
        json.dump(checkboxes_states, f)


def load_skills():
    output_file = os.path.join(output_dir, "skills.json")
    try:
        with open(output_file, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return [False for _ in range(25)]
