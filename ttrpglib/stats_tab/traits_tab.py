import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QTextEdit
from ttrpglib.utility.css_import import load_css


class Traits_Table(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet(load_css("QWidget.css"))

    def initUI(self):

        global output_dir, trait_1, trait_2

        output_dir = "data"

        trait_1, trait_2 = load_traits()

        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()

        self.descriptions = {
            "Tratto": "",
            "Alien DNA": "Ti sei sottoposto volontariamente ad un esperimento che combina DNA umano con quello alieno. Di conseguenza, hai più salute e sei più incline alle modifiche organiche del tuo corpo, ma gli oggetti di cura ed il cibo non sono molto efficaci su di te.",
            "Dream House": "Sei il proprietario di una casa di lusso su un pianeta paradisiaco! Purtroppo però la casa è accompagnata da un mutuo di 125.000 crediti che deve essere pagato a rate mensili.",
            "Kid Stuff": "I tuoi genitori sono vivi e vegeti e puoi andarli a trovare a casa loro. Ogni settimana, però, devi inviare il 2% dei tuoi guadagni a loro.",
            "Spaced": "Il tuo corpo si è acclimatato allo spazio e alla microgravità. Sei più agile e scattante quando sei nello spazio, ma hai difficoltà sulla terra ferma. (Non può essere combinato con Terra Firma)",
            "Terra Firma": "Non ti sei mai abituato allo spazio e alla microgravità. Sei più agile e scattante sulla terra ferma, ma hai difficoltà nello spazio. (Non può essere combinato con Spaced)",
            "Wanted": "Qualcuno ha messo una taglia sulla tua testa e ormai la voce si è sparsa. Sei ricercato dai cacciatori di taglie, che potrebbero presentarti per catturarti, o peggio, ucciderti. Di conseguenza, sai bene come nasconderti per passare una notte sicura.",
        }

        # Primo layout
        combo_traits1 = QComboBox()
        combo_traits1.setStyleSheet(load_css("QComboBox.css"))
        for key in self.descriptions.keys():
            combo_traits1.addItem(key)

        combo_traits1.currentTextChanged.connect(
            lambda text: self.show_descr(text, descr_traits1)
        )
        combo_traits1.currentTextChanged.connect(
            lambda temp_trait1=combo_traits1.currentText(): self.update_trait(
                1, temp_trait1
            )
        )

        descr_traits1 = QTextEdit()
        descr_traits1.setStyleSheet(load_css("QTextEdit.css"))
        descr_traits1.setReadOnly(True)

        layout1.addWidget(combo_traits1)
        layout1.addWidget(descr_traits1)

        combo_traits1.setCurrentText(trait_1)
        self.show_descr(trait_1, descr_traits1)

        # Secondo layout
        combo_traits2 = QComboBox()
        combo_traits2.setStyleSheet(load_css("QComboBox.css"))

        for key in self.descriptions.keys():
            combo_traits2.addItem(key)

        combo_traits2.currentTextChanged.connect(
            lambda text: self.show_descr(text, descr_traits2)
        )
        combo_traits2.currentTextChanged.connect(
            lambda temp_trait2=combo_traits2.currentText(): self.update_trait(
                2, temp_trait2
            )
        )

        descr_traits2 = QTextEdit()
        descr_traits2.setStyleSheet(load_css("QTextEdit.css"))
        descr_traits2.setReadOnly(True)

        layout2.addWidget(combo_traits2)
        layout2.addWidget(descr_traits2)

        combo_traits2.setCurrentText(trait_2)
        self.show_descr(trait_2, descr_traits2)

        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)

        self.setLayout(main_layout)

    def show_descr(self, text, textbox):
        desc = self.descriptions.get(text, "Descrizione non trovata")
        # Imposta il testo nella QTextEdit con la descrizione ottenuta
        textbox.setText(desc)

    def update_trait(self, index, new_trait):
        global trait_1, trait_2
        if index == 1:
            trait_1 = new_trait
        elif index == 2:
            trait_2 = new_trait


def save_traits():
    output_file = os.path.join(output_dir, "traits.json")
    traits = {"Trait 1": trait_1, "Trait 2": trait_2}

    with open(output_file, "w") as f:
        json.dump(traits, f, indent=4)


def load_traits():
    output_file = os.path.join(output_dir, "traits.json")
    empty_traits = {"Trait 1": "null", "Trait 2": "null"}

    try:
        with open(output_file, "r") as f:

            data = json.load(f)
            trait_1 = data.get("Trait 1")
            trait_2 = data.get("Trait 2")

            return trait_1, trait_2
    except FileNotFoundError:
        return empty_traits
