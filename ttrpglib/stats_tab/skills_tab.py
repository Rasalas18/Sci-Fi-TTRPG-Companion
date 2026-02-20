import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox
from ttrpglib.utility.css_import import load_css


class SkillTable(QWidget):
    def __init__(self):
        super().__init__()
        self.output_dir = "data"
        self.checkboxes = [None for _ in range(25)]
        self.checkboxes_states = self.load_skills()
        self.initUI()
        self.setStyleSheet(load_css("QWidget.css"))

    def initUI(self):
        main_layout = QHBoxLayout()

        skill_layout1 = QVBoxLayout()
        skills1 = [
            "Acrobatics", "Alien", "Athletics", "Constitution", "Diplomacy",
            "Drive", "Engineering", "Gambling", "Hacking", "History", "Insight",
        ]

        for i, skill in enumerate(skills1):
            checkbox = QCheckBox(skill)
            checkbox.setStyleSheet(load_css("QCheckBox.css"))
            checkbox.clicked.connect(lambda _, pos=i: self.update_checkbox(pos))
            skill_layout1.addWidget(checkbox)
            self.checkboxes[i] = checkbox
            if self.checkboxes_states[i]:
                self.checkboxes[i].setChecked(True)

        main_layout.addLayout(skill_layout1)

        skill_layout2 = QVBoxLayout()
        skills2 = [
            "Languages", "Manipulation", "Medic", "Melee", "Perception",
            "Performance", "Pilot", "Religion", "Science", "Shooting",
            "Sleight of Hand", "Stealth", "Survival", "Tech",
        ]

        for j, skill in enumerate(skills2):
            k = j + len(skills1)
            checkbox = QCheckBox(skill)
            checkbox.setStyleSheet(load_css("QCheckBox.css"))
            checkbox.clicked.connect(lambda _, pos=k: self.update_checkbox(pos))
            skill_layout2.addWidget(checkbox)
            self.checkboxes[k] = checkbox
            if self.checkboxes_states[k]:
                self.checkboxes[k].setChecked(True)

        main_layout.addLayout(skill_layout2)
        self.setLayout(main_layout)

    def update_checkbox(self, pos):
        self.checkboxes_states[pos] = not self.checkboxes_states[pos]

    def save_skills(self):
        output_file = os.path.join(self.output_dir, "skills.json")
        with open(output_file, "w") as f:
            json.dump(self.checkboxes_states, f)

    def load_skills(self):
        output_file = os.path.join(self.output_dir, "skills.json")
        try:
            with open(output_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return [False for _ in range(25)]
