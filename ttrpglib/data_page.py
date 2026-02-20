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

        self.databases = [Database("luna"), Database("pianeta"), Database("nave"), Database("stazione")]

        # Aggiungo databases
        tab_widget_data.addTab(Database("luna"), "Lune")
        tab_widget_data.addTab(Database("pianeta"), "Pianeti")
        tab_widget_data.addTab(Database("nave"), "Navi")
        tab_widget_data.addTab(Database("stazione"), "Stazioni")

        # Aggiunta del QTabWidget al layout verticale
        data_layout.addWidget(tab_widget_data)

        # Impostazione del layout per la finestra
        self.setLayout(data_layout)
