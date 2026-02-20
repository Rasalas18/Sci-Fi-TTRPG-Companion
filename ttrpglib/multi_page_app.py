from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QStackedWidget,
    QMessageBox,
)
from PyQt5.QtCore import QTimer
from datetime import datetime
from ttrpglib.note_page import NotePage
from ttrpglib.map_page import MapPage
from ttrpglib.bounty_page import BountyPage
from ttrpglib.data_page import DataPage
from ttrpglib.stats_page import StatsPage
from ttrpglib.main_page import MainPage
from ttrpglib.utility.css_import import load_css_with_color

AUTOSAVE_INTERVAL = 5 * 1 * 1000


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
            button.setStyleSheet(load_css_with_color("QButton_MultiPage.css", "black"))
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

        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(AUTOSAVE_INTERVAL)

    def multi_update_button_color(self, current_button):
        for button in self.buttons:
            if button == current_button:
                button.setStyleSheet(load_css_with_color("QButton_MultiPage.css", "green"))
            else:
                button.setStyleSheet(load_css_with_color("QButton_MultiPage.css", "black"))

    def button_func(self, page_name):
        current_button = self.sender()
        self.multi_update_button_color(current_button)

        self.show_page(page_name)

    def show_page(self, page_name):
        index = list(self.pages.keys()).index(page_name)
        self.stacked_widget.setCurrentIndex(index)

    def closeEvent(self, event):
        message_box = QMessageBox()
        message_box.setWindowTitle("Conferma")
        message_box.setText("Vuoi salvare prima di chiudere?")
        message_box.setIcon(QMessageBox.Question)
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        response = message_box.exec_()

        if response == QMessageBox.Yes:
            stats_page = self.pages["Sheet"]
            stats_page.attr_interface.save_attr()
            stats_page.inventory_interface.save_inv()
            stats_page.skill_interface.save_skills()
            stats_page.traits_interface.save_traits()
            stats_page.save_background()
            self.pages["Note"].save_notes()
            for db in self.pages["Data"].databases:
                db.close_connection()
            event.accept()
        elif response == QMessageBox.No:
            for db in self.pages["Data"].databases:
                db.close_connection()
            event.accept()
        else:
            event.ignore()

    def autosave(self):
        stats_page = self.pages["Sheet"]
        stats_page.attr_interface.save_attr()
        stats_page.inventory_interface.save_inv()
        stats_page.skill_interface.save_skills()
        stats_page.traits_interface.save_traits()
        stats_page.save_background()
        self.pages["Note"].save_notes()
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[AUTOSAVE] Salvataggio automatico eseguito alle {timestamp}")
