from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QStackedWidget,
    QMessageBox,
)
from ttrpglib.note_page import NotePage, save_notes
from ttrpglib.map_page import MapPage
from ttrpglib.bounty_page import BountyPage
from ttrpglib.data_page import DataPage
from ttrpglib.stats_page import StatsPage, save_stats
from ttrpglib.main_page import MainPage
from ttrpglib.utility.css_import import load_css


class MultiPageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Page App")
        self.setStyleSheet("background-color: black;")

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: black;")

        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        nav_layout = QHBoxLayout()
        layout.addLayout(nav_layout)

        self.buttons = []
        button_labels = ["Home", "Sheet", "Note", "Map", "Data", "Bounty"]

        for label in button_labels:
            button = QPushButton(label)
            button.setStyleSheet(load_css("QButton_MultiPage_black.css"))
            button.clicked.connect(lambda checked, label=label: self.button_func(label))
            nav_layout.addWidget(button)
            self.buttons.append(button)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        self.pages = {
            "Note": NotePage(),
            "Map": MapPage(),
            "Bounty": BountyPage(),
            "Data": DataPage(),
            "Sheet": StatsPage(),
            "Home": MainPage(),
        }

        for page_name, page in self.pages.items():
            self.stacked_widget.addWidget(page)

        self.show_page("Home")
        self.multi_update_button_color(self.buttons[0])

    def multi_update_button_color(self, current_button):
        for button in self.buttons:
            if button == current_button:
                button.setStyleSheet(load_css("QButton_MultiPage_green.css"))
            else:
                button.setStyleSheet(load_css("QButton_MultiPage_black.css"))

    def button_func(self, page_name):
        current_button = self.sender()
        self.multi_update_button_color(current_button)

        self.show_page(page_name)

    def show_page(self, page_name):
        index = list(self.pages.keys()).index(page_name)
        self.stacked_widget.setCurrentIndex(index)

    def closeEvent(self, event):
        self.save_on_close()

    def save_on_close(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("Conferma")
        message_box.setText("Vuoi salvare prima di chiudere?")
        message_box.setIcon(QMessageBox.Question)
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        response = message_box.exec_()

        if response == QMessageBox.Yes:  # Aggiungi qui altri saving
            save_notes()
            save_stats()
            self.close()
        elif response == QMessageBox.No:
            self.close()
