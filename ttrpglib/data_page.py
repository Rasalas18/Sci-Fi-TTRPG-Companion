from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout
from ttrpglib.database.celestial_database import Database
from ttrpglib.utility.css_import import load_css


class DataPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Creazione di un layout verticale per la pagina dei dati
        data_layout = QHBoxLayout()

        # Creazione del QTabWidget
        tab_widget_data = QTabWidget()
        tab_widget_data.setTabShape(QTabWidget.Triangular)
        tab_widget_data.setStyleSheet(load_css("QTabWidget_data.css"))

        # Creazione e aggiunta delle schede (tabs) al QTabWidget
        moon_database = Database("lune")
        planet_database = Database("pianeti")
        spaceship_database = Database("navi")
        spacestation_database = Database("stazioni")

        # Aggiungo prima Pianeti e Lune per metterle a sinistra
        tab_widget_data.addTab(moon_database, "Lune")
        tab_widget_data.addTab(planet_database, "Pianeti")

        # Inserisci 3 tab vuote tra "Pianeti" e "Spaceship"
        for _ in range(6):
            empty_tab = QWidget()
            tab_widget_data.addTab(empty_tab, "")
            tab_widget_data.setTabEnabled(tab_widget_data.indexOf(empty_tab), False)

        tab_widget_data.addTab(spaceship_database, "Navi")
        tab_widget_data.addTab(spacestation_database, "Stazioni")

        # Aggiunta del QTabWidget al layout verticale
        data_layout.addWidget(tab_widget_data)

        # Impostazione del layout per la finestra
        self.setLayout(data_layout)


# finire stile QTableWidget e box quando carichi o rimuovi
