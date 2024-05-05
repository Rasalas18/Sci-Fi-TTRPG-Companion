import sys
import os
import re
import sqlite3
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QInputDialog,
    QFileDialog,
)
from PyQt5.QtCore import Qt


class Planet_Database(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Example")
        self.setGeometry(100, 100, 600, 400)

        database_dir = "data"
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)

        self.database_path = os.path.join(database_dir, "database.db")

        self.conn = sqlite3.connect(self.database_path)
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Planet
                            (id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            type TEXT NOT NULL)"""
        )
        self.conn.commit()

        self.layout = QVBoxLayout()

        self.planet_table = QTableWidget()
        self.planet_table.setColumnCount(2)
        self.planet_table.setHorizontalHeaderLabels(["Nome", "Tipo"])
        self.load_planet()
        self.planet_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.add_button = QPushButton("Aggiungi Pianeta")
        self.add_button.clicked.connect(self.add_planet)

        self.load_from_sql_button = QPushButton("Carica Pianeti da File SQL")
        self.load_from_sql_button.clicked.connect(self.load_planet_from_sql_file)

        self.save_to_sql_button = QPushButton("Salve Pianeti in File SQL")
        self.save_to_sql_button.clicked.connect(self.save_database_to_sql_file)

        self.remove_duplicates_button = QPushButton("Rimuovi Duplicati")
        self.remove_duplicates_button.clicked.connect(self.remove_duplicate_planet)

        self.layout.addWidget(self.planet_table)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.load_from_sql_button)
        self.layout.addWidget(self.save_to_sql_button)
        self.layout.addWidget(self.remove_duplicates_button)

        self.setLayout(self.layout)
        self.planet_table.setSortingEnabled(True)

    def load_planet(self):
        self.planet_table.setRowCount(0)
        self.cursor.execute("SELECT name, type FROM Planet")
        planet = self.cursor.fetchall()

        for row_num, planet in enumerate(planet):
            self.planet_table.insertRow(row_num)
            for col_num, data in enumerate(planet):
                item = QTableWidgetItem(data)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.planet_table.setItem(row_num, col_num, item)

    def add_planet(self):
        nome, ok = QInputDialog.getText(
            self, "Inserisci nome", "Inserisci il nome del pianeta: "
        )
        if ok:
            tipo, ok = QInputDialog.getText(
                self, "Inserisci tipo", "Inserisci il tipo del pianeta:"
            )
            if ok:
                if nome and tipo:
                    nome = nome.lower()
                    tipo = tipo.lower()

                    if re.match(r"^[a-zA-Z\s]+$", nome) and re.match(
                        r"^[a-zA-Z\s]+$", tipo
                    ):
                        self.cursor.execute(
                            "SELECT * FROM Planet WHERE LOWER(name) = ? AND LOWER(type) = ?",
                            (nome, tipo),
                        )
                        existing_planet = self.cursor.fetchone()
                        if existing_planet:
                            QMessageBox.warning(
                                self, "Errore", "Pianeta è già presente nel database!"
                            )
                        else:
                            self.cursor.execute(
                                "INSERT INTO Planet (name, type) VALUES (?, ?)",
                                (nome, tipo),
                            )
                            self.conn.commit()
                            QMessageBox.information(
                                self, "Successo", "Pianeta aggiunto con successo!"
                            )
                            self.load_planet()
                    else:
                        QMessageBox.warning(self, "Errore", "Nome o Tipo non valido!")
                else:
                    QMessageBox.warning(
                        self, "Errore", "Inserire sia nome che tipo del pianeta!"
                    )

    def load_planet_from_sql_file(self):
        file_dialog = QFileDialog(self)
        filename, _ = file_dialog.getOpenFileName(
            self,
            "Select SQL File",
            "",
            "SQL files (*.sql);;All files (*)",
        )
        if filename:
            with open(filename, "r") as file:
                sql_script = file.read()
                self.cursor.executescript(sql_script)
            self.conn.commit()
            self.load_planet()
            QMessageBox.information(
                self,
                "Successo",
                "Pianeti caricati dal file SQL con successo!",
            )

    def save_database_to_sql_file(self):
        file_dialog = QFileDialog(self)
        filename, _ = file_dialog.getSaveFileName(
            self,
            "Save SQL File",
            "",
            "SQL files (*.sql);;All files (*)",
        )
        if filename:
            with open(filename, "w") as file:
                for line in self.conn.iterdump():
                    file.write(f"{line}\n")
            QMessageBox.information(
                self,
                "Successo",
                "Database salvato sul file SQL con successo!",
            )

    def remove_duplicate_planet(self):
        self.cursor.execute(
            """DELETE FROM Planet
               WHERE id NOT IN (SELECT MIN(id)
                                FROM Planet
                                GROUP BY LOWER(name), LOWER(type))"""
        )
        self.conn.commit()
        self.load_planet()
        QMessageBox.information(
            self,
            "Successo",
            "Duplicati rimossi con successo!",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Planet_Database()
    window.show()
    sys.exit(app.exec_())
