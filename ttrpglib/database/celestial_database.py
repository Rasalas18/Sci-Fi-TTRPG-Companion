import os
import sqlite3
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
)
from PyQt5.QtCore import Qt
from ttrpglib.utility.css_import import load_css


class Database(QWidget):
    def __init__(self, celestial_body):
        super().__init__()

        self.celestial_body = celestial_body.lower()

        database_dir = "data/database_out"
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)

        self.database_path = os.path.join(
            database_dir, f"database_{self.celestial_body}.db"
        )

        self.conn = sqlite3.connect(self.database_path)
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {celestial_body.capitalize()}
               (id INTEGER PRIMARY KEY,
               name TEXT NOT NULL,
               type TEXT NOT NULL,
               position TEXT NOT NULL,
               properties TEXT NOT NULL,
               system TEXT NOT NULL)"""
        )
        self.conn.commit()

        self.layout = QVBoxLayout()

        self.planet_table = QTableWidget()
        self.planet_table.setStyleSheet(load_css("QTableWidget.css"))
        self.planet_table.setColumnCount(5)
        self.planet_table.setHorizontalHeaderLabels(
            ["Nome", "Tipo", "Posizione", "Proprietà", "Sistema"]
        )
        self.load_database()
        self.planet_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.load_from_sql_button = QPushButton(
            f"Carica {celestial_body.capitalize()} da File SQL"
        )
        self.load_from_sql_button.setStyleSheet(load_css("QButton_data.css"))
        self.load_from_sql_button.clicked.connect(self.load_database_from_sql_file)

        self.remove_duplicates_button = QPushButton("Rimuovi Duplicati")
        self.remove_duplicates_button.setStyleSheet(load_css("QButton_data.css"))
        self.remove_duplicates_button.clicked.connect(self.remove_duplicate)

        self.layout.addWidget(self.planet_table)
        self.layout.addWidget(self.load_from_sql_button)
        self.layout.addWidget(self.remove_duplicates_button)

        self.setLayout(self.layout)
        self.planet_table.setSortingEnabled(True)

    def load_database(self):
        self.planet_table.setRowCount(0)
        self.cursor.execute(
            f"SELECT name, type, position, properties, system FROM {self.celestial_body.capitalize()}"
        )
        planets = self.cursor.fetchall()

        for row_num, planet in enumerate(planets):
            self.planet_table.insertRow(row_num)
            for col_num, data in enumerate(planet):
                item = QTableWidgetItem(data)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.planet_table.setItem(row_num, col_num, item)

    def load_database_from_sql_file(self):
        file_dialog = QFileDialog(self)
        filename, _ = file_dialog.getOpenFileName(
            self,
            f"Select SQL File for {self.celestial_body.capitalize()}",
            "",
            "SQL files (*.sql);;All files (*)",
        )
        if filename:
            with open(filename, "r") as file:
                sql_script = file.read()
                self.cursor.executescript(sql_script)
            self.conn.commit()
            self.load_database()
            QMessageBox.information(
                self,
                "Successo",
                f"{self.celestial_body.capitalize()} caricati dal file SQL con successo!",
            )

    def remove_duplicate(self):
        self.cursor.execute(
            f"""DELETE FROM {self.celestial_body.capitalize()}
               WHERE id NOT IN (SELECT MIN(id)
                                FROM {self.celestial_body.capitalize()}
                                GROUP BY LOWER(name), LOWER(type), LOWER(position), LOWER(properties), LOWER(system))"""
        )
        self.conn.commit()
        self.load_database()
        QMessageBox.information(
            self,
            "Successo",
            f"Duplicati di {self.celestial_body.capitalize()} rimossi con successo!",
        )
