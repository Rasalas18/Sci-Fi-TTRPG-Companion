from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QTabWidget,
    QListWidget,
    QGridLayout,
    QFrame,
    QListWidgetItem,
)

from PyQt5.QtCore import Qt
from ttrpglib.utility.css_import import load_css


class DataPage(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet(load_css("QWidget.css"))

        # Layout orizzontale principale
        layout = QHBoxLayout(self)

        # Primo layout verticale
        v_layout1 = QVBoxLayout()

        # Crea la QListWidget e aggiungi gli elementi
        list_widget = QListWidget()
        list_widget.setStyleSheet(load_css("QList.css"))

        items = ["Pianeti", "Lune", "Asteroidi", "Stazioni Spaziali", "Navi Spaziali"]

        for item in items:
            item = QListWidgetItem(item)
            item.setTextAlignment(Qt.AlignHCenter)
            list_widget.addItem(item)

        # Aggiungi la QListWidget al layout verticale
        v_layout1.addWidget(list_widget)

        # Crea un frame per la griglia
        grid_frame = QFrame()
        grid_frame.setStyleSheet(load_css("QFrame.css"))

        # Crea un layout a griglia all'interno del frame
        grid_layout = QGridLayout(grid_frame)
        grid_layout.setSpacing(35)

        # Aggiungi QLabel a tutte le posizioni da (1, 1) a (5, 5)
        for i in range(4):
            for j in range(4):
                button = QPushButton(f"Button {i}-{j}")
                # button.clicked.connect()

                button.setStyleSheet(load_css("QButton_data.css"))
                grid_layout.addWidget(button, i, j)

        # Aggiungi il frame al layout verticale
        v_layout1.addWidget(grid_frame)

        # Aggiungi il primo layout verticale al layout orizzontale principale
        layout.addLayout(v_layout1)

        # Secondo layout verticale
        v_layout2 = QVBoxLayout()

        # Aggiungi un QTabWidget al secondo layout verticale
        tab_widget = QTabWidget()
        tab_widget.setTabsClosable(True)
        tab_widget.setTabShape(QTabWidget.Triangular)
        tab_widget.setStyleSheet(load_css("QTabWidget.css"))

        # Connessione del segnale tabCloseRequested
        tab_widget.tabCloseRequested.connect(self.close_tab)

        # Aggiungi le schede al QTabWidget
        tab1 = QWidget()
        tab2 = QWidget()

        tab_widget.addTab(tab1, "Tab 1")
        tab_widget.addTab(tab2, "Tab 2")

        v_layout2.addWidget(tab_widget)

        # Aggiungi il secondo layout verticale al layout orizzontale principale
        layout.addLayout(v_layout2)

    # Funzione per chiudere la scheda
    def close_tab(self, index):
        self.sender().removeTab(index)
