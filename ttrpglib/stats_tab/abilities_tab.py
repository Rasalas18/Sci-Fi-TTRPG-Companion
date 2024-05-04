import os
import json
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QGridLayout,
    QLabel,
    QFrame,
    QVBoxLayout,
)
from PyQt5.QtGui import QPixmap
from ttrpglib.utility.css_import import load_css


class Ability_Table(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet("background-color: black;")

    def initUI(self):
        global buttons, clicked, enabled, output_dir

        output_dir = "data"

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Creazione del frame per il grid layout
        grid_frame = QFrame()
        grid_layout = QGridLayout(grid_frame)
        grid_layout.setSpacing(20)

        main_layout.addWidget(grid_frame, 9)
        main_layout.setSpacing(0)

        # Inizializza la matrice dei pulsanti e dello stato dei pulsanti
        buttons = [[None for _ in range(5)] for _ in range(6)]
        clicked, enabled = load_abilities()

        # Directory delle immagini
        image_directory = r"assets\icons"

        # Lista dei nomi delle immagini
        image_names = [
            "path_to_icon_1.png",
            "outlaw_icon.png",
            "path_to_icon_3.png",
            "path_to_icon_4.png",
            "wordsmith_icon.png",
        ]

        # Aggiungi una riga vuota prima della riga 1
        for j in range(5):  # Colonne
            image_label = QLabel()
            image_path = os.path.join(
                image_directory, image_names[j]
            )  # Costruisci il percorso completo dell'immagine
            pixmap = QPixmap(
                image_path
            )  # Specifica il percorso dell'immagine per questo pulsante

            # Controlla se l'immagine è stata caricata correttamente
            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    100, 100
                )  # Ridimensiona l'immagine alle dimensioni desiderate
                image_label.setPixmap(pixmap)  # Imposta l'immagine sull'etichetta
            else:
                print(f"Impossibile caricare l'immagine dal percorso: {image_path}\n")
                print(f"L'immagine deve essere 100x100 px")
                # Utilizza un'immagine di fallback o mostra un messaggio di errore

            grid_layout.addWidget(image_label, 0, j)

        for i in range(6):  # Righe
            for j in range(5):  # Colonne
                button = QPushButton(f"Button {i}-{j}")
                button.clicked.connect(lambda _, r=i, c=j: abi_button_click(r, c))

                # Imposta il ToolTip quando si passa col mouse sul button
                button.setToolTip(f"Tooltip per Button {i}-{j}")

                button.setStyleSheet(load_css("pushbutton.css"))
                grid_layout.addWidget(
                    button, i + 1, j
                )  # Aggiungi i bottoni dalla riga 1 in poi
                buttons[i][j] = button  # Salva il pulsante nella matrice dei pulsanti

                # Imposta lo stile del pulsante e l'abilitazione in base allo stato salvato
                abi_update_button_color(button, i, j)
                button.setEnabled(enabled[i][j])


def abi_button_click(row, col):
    clicked[row][col] = not clicked[row][col]  # Inverti lo stato del pulsante
    enabled[row][col] = True  # Imposta il pulsante come abilitato
    abi_update_button_color(buttons[row][col], row, col)

    # Disattiva gli altri pulsanti sulla stessa riga
    for c in range(5):
        if c != col:
            clicked[row][c] = False
            abi_update_button_color(buttons[row][c], row, c)
            buttons[row][c].setEnabled(False)  # Disabilita il pulsante
            enabled[row][c] = False  # Imposta il pulsante come disabilitato


def abi_update_button_color(button, row, col):
    row_clicked = any(clicked[row])

    if clicked[row][col]:
        button.setStyleSheet(
            """
            QPushButton {
                background-color: green;
                color: white;
                border: 1px solid white;
                border-radius: 10px;
                padding: 5px 5px;
            }

            QToolTip {
                background-color: green;
                color: white;
                border: 1px solid white;
                border-radius: 5px;
                padding: 5px;
            }
            """
        )
        button.setEnabled(False)

    elif not clicked[row][col] and row_clicked:
        button.setStyleSheet(
            """
            QPushButton {
                background-color: black;
                color: dark grey;
                border: 1px solid white;
                border-radius: 10px;
                padding: 5px 5px;
            }
            QToolTip {
                background-color: black;
                color: white;
                border: 1px solid white;
                border-radius: 5px;
                padding: 5px;
            }
            """
        )

    elif not clicked[row][col] and row_clicked is False:
        button.setStyleSheet(
            """
            QPushButton {
                background-color: black;
                color: white;
                border: 1px solid white;
                border-radius: 10px;
                padding: 5px 5px;
            }
            QToolTip {
                background-color: black;
                color: white;
                border: 1px solid white;
                border-radius: 5px;
                padding: 5px;
            }
            """
        )


def save_abilities():
    output_file = os.path.join(output_dir, "abilities.json")
    with open(output_file, "w") as f:
        json.dump({"clicked": clicked, "enabled": enabled}, f)


def load_abilities():
    output_file = os.path.join(output_dir, "abilities.json")
    try:
        with open(output_file, "r") as f:
            data = json.load(f)
            return data["clicked"], data["enabled"]
    except FileNotFoundError:
        return [[False for _ in range(5)] for _ in range(6)], [
            [True for _ in range(5)] for _ in range(6)
        ]
