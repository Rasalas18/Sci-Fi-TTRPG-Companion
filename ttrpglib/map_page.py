from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from ttrpglib.utility.css_import import load_css


class MapPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(load_css("QWidget.css"))

        layout = QVBoxLayout(self)
        label = QLabel("Pagina della Mappa", alignment=Qt.AlignCenter)
        label.setStyleSheet("color: green; font-size: 24px;")
        layout.addWidget(label)
