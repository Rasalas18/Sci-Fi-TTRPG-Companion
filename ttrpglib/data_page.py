from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout
from ttrpglib.database.celestial_database import Database
from ttrpglib.utility.css_import import load_css


class DataPage(QWidget):
    def __init__(self):
        super().__init__()
        self.databases = []
        self.initUI()

    def initUI(self):

        # Creazione di un layout verticale per la pagina dei dati
        data_layout = QHBoxLayout()

        # Creazione del QTabWidget
        tab_widget_data = QTabWidget()
        tab_widget_data.setTabShape(QTabWidget.Triangular)
        tab_widget_data.setStyleSheet(load_css("QTabWidget_data.css"))

        moon_db = Database("luna")
        planets_db = Database("pianeta")
        ships_db = Database("nave")
        stations_db = Database("stazione")

        self.databases = [moon_db, planets_db, ships_db, stations_db]

        # Aggiungo databases
        tab_widget_data.addTab(moon_db, "Lune")
        tab_widget_data.addTab(planets_db, "Pianeti")
        tab_widget_data.addTab(ships_db, "Navi")
        tab_widget_data.addTab(stations_db, "Stazioni")

        # Aggiunta del QTabWidget al layout verticale
        data_layout.addWidget(tab_widget_data)

        # Impostazione del layout per la finestra
        self.setLayout(data_layout)
