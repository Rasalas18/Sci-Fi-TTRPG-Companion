from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.QtGui import QFont


class LoginPage(QMainWindow):
    def __init__(self, login_success):
        super().__init__()

        self.setWindowTitle("Login")
        self.setStyleSheet("background-color: black; color: green;")

        self.login_success = login_success

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.label_username = QLabel("Username:")
        self.label_username.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.label_username)

        self.username_entry = QLineEdit()
        self.username_entry.setStyleSheet("color: white; border: 1px solid grey")
        self.username_entry.setFont(QFont("Arial", 12))
        layout.addWidget(self.username_entry)

        self.label_password = QLabel("Password:")
        self.label_password.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.label_password)

        self.password_entry = QLineEdit()
        self.password_entry.setStyleSheet("color: white; border: 1px solid grey")
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setFont(QFont("Arial", 12))
        layout.addWidget(self.password_entry)

        self.password_entry.returnPressed.connect(self.login)

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        credentials = {  # Credenziali Corrette
            "admin": "password",
            "Dave": "Rivera",
            "Jordan": "Alken",
            "Sydney": "Gulsvig",
            "Tavish": "Stasny",
        }

        if username in credentials and password == credentials[username]:
            self.login_success()
            self.close()
        else:
            QMessageBox.critical(
                self, "Login Error", "Invalid username or password", QMessageBox.Ok
            )
