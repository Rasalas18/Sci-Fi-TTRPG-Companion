import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QTextEdit, QMessageBox,
)
from PyQt5.QtCore import Qt
from ttrpglib.utility.css_import import load_css


class InventoryTable(QWidget):
    def __init__(self):
        super().__init__()
        self.output_dir = "data"
        self.inventory = {}
        self.money = 0
        self.setStyleSheet("background-color: black;")
        self.load_inv()
        self.setup_ui()
        self.show_inv()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        inv_layout = QHBoxLayout()

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

        inv_layout.addWidget(self.obj_label)
        inv_layout.addWidget(self.obj_entry)
        inv_layout.addWidget(self.quantity_label)
        inv_layout.addWidget(self.quantity_entry)
        inv_layout.addWidget(self.add_button)
        inv_layout.addWidget(self.remove_button)
        self.layout.addLayout(inv_layout)

        self.inv_label = QLabel("Inventario:")
        self.inv_label.setStyleSheet("color: white; font-size: 10pt")
        self.inv_text = QTextEdit()
        self.inv_text.setStyleSheet("color: white; border: 1px solid white; font-size: 10pt")
        self.inv_text.setReadOnly(True)

        self.layout.addWidget(self.inv_label)
        self.layout.addWidget(self.inv_text)

        self.money_label = QLabel(f"Money: {self.money}")
        self.money_label.setStyleSheet("color: white; font-size: 10pt")
        self.money_label.setAlignment(Qt.AlignCenter)

        self.remove_1 = QPushButton("-1")
        self.remove_1.clicked.connect(lambda: self.update_money(-1))
        self.remove_1.setStyleSheet(load_css("QButton_removeMoney.css"))

        self.remove_10 = QPushButton("-10")
        self.remove_10.clicked.connect(lambda: self.update_money(-10))
        self.remove_10.setStyleSheet(load_css("QButton_removeMoney.css"))

        self.remove_100 = QPushButton("-100")
        self.remove_100.clicked.connect(lambda: self.update_money(-100))
        self.remove_100.setStyleSheet(load_css("QButton_removeMoney.css"))

        self.add_1 = QPushButton("+1")
        self.add_1.clicked.connect(lambda: self.update_money(1))
        self.add_1.setStyleSheet(load_css("QButton_addMoney.css"))

        self.add_10 = QPushButton("+10")
        self.add_10.clicked.connect(lambda: self.update_money(10))
        self.add_10.setStyleSheet(load_css("QButton_addMoney.css"))

        self.add_100 = QPushButton("+100")
        self.add_100.clicked.connect(lambda: self.update_money(100))
        self.add_100.setStyleSheet(load_css("QButton_addMoney.css"))

        left_bottom = QHBoxLayout()
        left_bottom.addWidget(self.remove_1)
        left_bottom.addWidget(self.remove_10)
        left_bottom.addWidget(self.remove_100)

        middle_bottom = QHBoxLayout()
        middle_bottom.addWidget(self.money_label)

        right_bottom = QHBoxLayout()
        right_bottom.addWidget(self.add_100)
        right_bottom.addWidget(self.add_10)
        right_bottom.addWidget(self.add_1)

        buttons_layout = QHBoxLayout()
        buttons_layout.addLayout(left_bottom)
        buttons_layout.addLayout(middle_bottom)
        buttons_layout.addLayout(right_bottom)
        self.layout.addLayout(buttons_layout)

    def update_money(self, amount):
        self.money += amount
        self.money_label.setText(f"Money: {self.money}")

    def add_object(self):
        obj = self.obj_entry.text()
        quantity_str = self.quantity_entry.text()
        if not quantity_str.isdigit():
            QMessageBox.critical(None, "Errore", "Inserisci una quantità valida.")
            return
        quantity_int = int(quantity_str)
        if obj in self.inventory:
            self.inventory[obj] += quantity_int
        else:
            self.inventory[obj] = quantity_int
        self.show_inv()

    def remove_object(self):
        obj = self.obj_entry.text()
        quantity_str = self.quantity_entry.text()
        if not quantity_str.isdigit():
            QMessageBox.critical(None, "Errore", "Inserisci una quantità valida.")
            return
        quantity_int = int(quantity_str)
        if obj in self.inventory:
            if self.inventory[obj] >= quantity_int:
                self.inventory[obj] -= quantity_int
                if self.inventory[obj] == 0:
                    del self.inventory[obj]
            else:
                QMessageBox.critical(None, "Errore", "La quantità specificata è maggiore della quantità presente nell'inventario.")
        else:
            QMessageBox.critical(None, "Errore", "L'obj specificato non è presente nell'inventario.")
        self.show_inv()

    def show_inv(self):
        inv_text = ""
        for obj, quantity in self.inventory.items():
            inv_text += f"{obj}: {quantity}\n"
        self.inv_text.setPlainText(inv_text)
        self.obj_entry.clear()
        self.quantity_entry.clear()

    def save_inv(self):
        output_file = os.path.join(self.output_dir, "inv.json")
        with open(output_file, "w") as f:
            json.dump({"inventory": self.inventory, "money": self.money}, f, indent=4)

    def load_inv(self):
        output_file = os.path.join(self.output_dir, "inv.json")
        try:
            with open(output_file, "r") as f:
                data = json.load(f)
                self.inventory = data.get("inventory", {})
                self.money = data.get("money", 0)
        except FileNotFoundError:
            self.inventory = {}
            self.money = 0
