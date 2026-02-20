import os
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QHBoxLayout,
    QLabel,
    QTextEdit,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from ttrpglib.stats_tab.attr_tab import AttrTable
from ttrpglib.stats_tab.inv_tab import InventoryTable
from ttrpglib.stats_tab.skills_tab import SkillTable
from ttrpglib.stats_tab.traits_tab import TraitsTable
from ttrpglib.utility.css_import import load_css


class StatsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(load_css("QWidget.css"))

        # Creazione dei layout di StatsPage
        layout_main = QVBoxLayout(self)
        layout_top = QHBoxLayout()
        layout_bottom = QVBoxLayout()
        # ----------------------------------------------
        # Layout Top
        # ----------------------------------------------

        # Aggiunta dei tab widget per layout_top e modifiche di stile
        tab_widget_left = QTabWidget()
        tab_widget_left.setTabShape(QTabWidget.Triangular)
        tab_widget_left.setStyleSheet(load_css("QTabWidget.css"))

        tab_widget_right = QTabWidget()
        tab_widget_right.setTabShape(QTabWidget.Triangular)
        tab_widget_right.setStyleSheet(load_css("QTabWidget.css"))

        # ----------------------------------------------
        # Tab Widget Left: Attr Tab
        # ----------------------------------------------

        attr_tab = QWidget()

        # Aggiunta del layout nella pagina "Attributes" e allineamento centrale dei widget
        attr_layout = QVBoxLayout(attr_tab)
        attr_layout.setAlignment(Qt.AlignCenter)

        self.attr_interface = AttrTable()
        attr_layout.addWidget(self.attr_interface)

        # ----------------------------------------------
        # Tab Widget Left: Image Tab
        # ----------------------------------------------

        image_tab = QWidget()

        # Aggiunta del layout nella pagina "Image" e allineamento centrale dei widget
        image_layout = QVBoxLayout(image_tab)
        image_layout.setAlignment(Qt.AlignCenter)

        # Aggiunta del frame nella pagina "Image" secondo il layout sopra
        image_label = QLabel()
        pixmap = QPixmap("assets/icons/pc_icon.jpg")

        # Ridimensiono l'immagine a 400x400 mantenendo l'aspect ratio
        scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)
        image_layout.addWidget(image_label)
        # ----------------------------------------------
        # Tab Widget Left: Inventory Tab
        # ----------------------------------------------

        inventory_tab = QWidget()

        # Aggiunta del layout nella pagina "Inventory" e allineamento centrale dei widget
        inventory_layout = QHBoxLayout(inventory_tab)
        inventory_layout.setAlignment(Qt.AlignCenter)

        # Includi l'interfaccia dell'inventario dalla classe Table di inv_tab.py
        self.inventory_interface = InventoryTable()
        inventory_layout.addWidget(self.inventory_interface)

        # ----------------------------------------------
        # Tab Widget Right: Skills
        # ----------------------------------------------

        skills_tab = QWidget()

        # Aggiunta del layout nella pagina "Skill"
        skill_layout = QHBoxLayout(skills_tab)

        # Includi l'interfaccia delle skill dalla classe Table di skills_tab.py
        self.skill_interface = SkillTable()
        skill_layout.addWidget(self.skill_interface)

        skills_tab.setFixedSize(450, 500)

        # ----------------------------------------------
        # Tab Widget Right: Traits
        # ----------------------------------------------

        traits_tab = QWidget()

        # Aggiunta del layout nella pagina "Traits"
        traits_layout = QHBoxLayout(traits_tab)

        # Includi l'interfaccia delle skill dalla classe Table di traits_tab.py
        self.traits_interface = TraitsTable()
        traits_layout.addWidget(self.traits_interface)

        # ----------------------------------------------
        # Tab Widgets and Layout Top
        # ----------------------------------------------

        # Aggiunta delle tab stats, image e inventory al tab_widget_left
        tab_widget_left.addTab(attr_tab, "Attributes")
        tab_widget_left.addTab(image_tab, "Image")
        tab_widget_left.addTab(inventory_tab, "Inventory")

        # Aggiunta delle tab skills e traits al tab_widget_right
        tab_widget_right.addTab(skills_tab, "Skills")
        tab_widget_right.addTab(traits_tab, "Traits")

        # Aggiunta dei tab widget a layout_top
        layout_top.addWidget(tab_widget_left)
        layout_top.addWidget(tab_widget_right)

        # ----------------------------------------------
        # Layout Bottom per background (scrollable)
        # ----------------------------------------------

        background_label = QLabel("Background")
        background_label.setStyleSheet(load_css("QLabel_down.css"))
        background_label.setAlignment(Qt.AlignCenter)

        # Definizione del QTextEdit
        self.background_text = QTextEdit()
        self.background_text.setStyleSheet(
            "color: white; font-size: 12pt; width: 400px; height: 100px"
        )

        # Aggiunge il QTextEdit scrollabile al layout_bottom
        layout_bottom.addWidget(background_label)
        layout_bottom.addWidget(self.background_text)

        self.output_dir = "data"
        self.background_text.setText(self.load_background())

        # ----------------------------------------------
        # Layout Main
        # ----------------------------------------------

        # Aggiunta dei layout alla finestra principale
        layout_main.addLayout(layout_top)
        layout_main.addLayout(layout_bottom)

    def save_background(self):

        output_file = os.path.join(self.output_dir, "background.txt")
        with open(output_file, "w") as file:
            file.write(self.background_text.toPlainText())

    def load_background(self):

        output_file = os.path.join(self.output_dir, "background.txt")
        try:
            with open(output_file, "r") as file:
                return file.read()
        except FileNotFoundError:
            return ""
