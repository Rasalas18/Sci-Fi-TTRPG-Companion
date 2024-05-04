import os
import pickle
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from ttrpglib.utility.css_import import load_css


class Inventory_Table(QWidget):
    def __init__(self):
        super().__init__()

        global inventory, money

        self.setStyleSheet("background-color: black;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.money = load_inv()
        money = self.money

        self.setup_ui()

        self.show_inv()

    def setup_ui(self):
        self.inv_layout = QHBoxLayout()

        self.obj_label = QLabel("Oggetto:")
        self.obj_label.setStyleSheet("color: white; font-size: 10pt")
        self.obj_entry = QLineEdit()
        self.obj_entry.setStyleSheet("color: white; border: 1px solid white")

        self.quantity_label = QLabel("Quantità:")
        self.quantity_label.setStyleSheet("color: white; font-size: 10pt")
        self.quantity_entry = QLineEdit()
        self.quantity_entry.setStyleSheet("color: white; border: 1px solid white")
        self.quantity_entry.setFixedWidth(30)

        self.add_button = QPushButton("Aggiungi")
        self.add_button.clicked.connect(self.add_object)
        self.add_button.setStyleSheet(load_css("QButton_inv.css"))
        self.remove_button = QPushButton("Rimuovi")
        self.remove_button.clicked.connect(self.remove_object)
        self.remove_button.setStyleSheet(load_css("QButton_inv.css"))

        self.inv_layout.addWidget(self.obj_label)
        self.inv_layout.addWidget(self.obj_entry)
        self.inv_layout.addWidget(self.quantity_label)
        self.inv_layout.addWidget(self.quantity_entry)
        self.inv_layout.addWidget(self.add_button)
        self.inv_layout.addWidget(self.remove_button)

        self.layout.addLayout(self.inv_layout)

        self.inv_label = QLabel("Inventario:")
        self.inv_label.setStyleSheet("color: white; font-size: 10pt")

        self.inv_text = QTextEdit()
        self.inv_text.setStyleSheet(
            "color: white; border: 1px solid white; font-size: 10pt"
        )
        self.inv_text.setReadOnly(True)

        self.layout.addWidget(self.inv_label)
        self.layout.addWidget(self.inv_text)

        left_bottom_layout = QHBoxLayout()

        self.remove_1 = QPushButton("-1")
        self.remove_1.clicked.connect(lambda: self.update_money(-1))
        self.remove_1.setStyleSheet(load_css("QButton_removeMoney.css"))

        self.remove_10 = QPushButton("-10")
        self.remove_10.clicked.connect(lambda: self.update_money(-10))
        self.remove_10.setStyleSheet(load_css("QButton_removeMoney.css"))

        self.remove_100 = QPushButton("-100")
        self.remove_100.clicked.connect(lambda: self.update_money(-100))
        self.remove_100.setStyleSheet(load_css("QButton_removeMoney.css"))

        left_bottom_layout.addWidget(self.remove_1)
        left_bottom_layout.addWidget(self.remove_10)
        left_bottom_layout.addWidget(self.remove_100)

        middle_bottom_layout = QHBoxLayout()

        self.money_label = QLabel(f"Money: {self.money}")
        self.money_label.setStyleSheet("color: white; font-size: 10pt")
        self.money_label.setAlignment(Qt.AlignCenter)

        right_bottom_layout = QHBoxLayout()

        self.add_100 = QPushButton("+100")
        self.add_100.clicked.connect(lambda: self.update_money(100))
        self.add_100.setStyleSheet(load_css("QButton_addMoney.css"))

        self.add_10 = QPushButton("+10")
        self.add_10.clicked.connect(lambda: self.update_money(10))
        self.add_10.setStyleSheet(load_css("QButton_addMoney.css"))

        self.add_1 = QPushButton("+1")
        self.add_1.clicked.connect(lambda: self.update_money(+1))
        self.add_1.setStyleSheet(load_css("QButton_addMoney.css"))

        middle_bottom_layout.addWidget(self.money_label)
        right_bottom_layout.addWidget(self.add_100)
        right_bottom_layout.addWidget(self.add_10)
        right_bottom_layout.addWidget(self.add_1)

        # Layout principale per i pulsanti in bottom
        buttons_layout = QHBoxLayout()
        buttons_layout.addLayout(left_bottom_layout)
        buttons_layout.addLayout(middle_bottom_layout)
        buttons_layout.addLayout(right_bottom_layout)

        self.layout.addLayout(buttons_layout)

    def update_money(self, amount):
        global money
        self.money += amount
        money = self.money
        self.money_label.setText(f"Money: {self.money}")

    def add_object(self):
        obj = self.obj_entry.text()
        quantity_str = self.quantity_entry.text()
        if (
            not quantity_str.isdigit()
        ):  # Controlla se l'input della quantità è un numero valido
            QMessageBox.critical(None, "Errore", "Inserisci una quantità valida.")
            return
        quantity_int = int(quantity_str)
        if obj in inventory:
            inventory[obj] += quantity_int
        else:
            inventory[obj] = quantity_int
        self.show_inv()

    def remove_object(self):
        obj = self.obj_entry.text()
        quantity_str = self.quantity_entry.text()
        if (
            not quantity_str.isdigit()
        ):  # Controlla se l'input della quantità è un numero valido
            QMessageBox.critical(None, "Errore", "Inserisci una quantità valida.")
            return
        quantity_int = int(quantity_str)
        if obj in inventory:
            if inventory[obj] >= quantity_int:
                inventory[obj] -= quantity_int
                if (
                    inventory[obj] == 0
                ):  # Se la quantità diventa 0, rimuovi completamente l'obj dall'inventario
                    del inventory[obj]
            else:
                QMessageBox.critical(
                    None,
                    "Errore",
                    "La quantità specificata è maggiore della quantità presente nell'inventario.",
                )
        else:
            QMessageBox.critical(
                None, "Errore", "L'obj specificato non è presente nell'inventario."
            )
        self.show_inv()

    def show_inv(self):
        inv_text = ""
        for obj, quantity in inventory.items():
            inv_text += f"{obj}: {quantity}\n"
        self.inv_text.setPlainText(inv_text)

        self.obj_entry.clear()
        self.quantity_entry.clear()


output_dir = "data"
inventory = {}


def save_inv():
    global output_dir, inventory, money
    output_file = os.path.join(output_dir, "inv.pickle")
    data_to_save = {
        "inventory": inventory,
        "money": money,  # Salva anche il valore del denaro
    }
    with open(output_file, "wb") as f:
        pickle.dump(data_to_save, f)


def load_inv():
    global output_dir, inventory, money
    output_file = os.path.join(output_dir, "inv.pickle")
    try:
        with open(output_file, "rb") as f:
            data = pickle.load(f)
            inventory = data["inventory"]
            money = data.get("money", 0)  # Imposta il valore del denaro, se presente
    except FileNotFoundError:
        return 0
    return money
