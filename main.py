import sys
from PyQt5.QtWidgets import QApplication
from ttrpglib.login_page import LoginPage
from ttrpglib.multi_page_app import MultiPageApp


def main():
    def login_success():
        multi_page_app = MultiPageApp()
        multi_page_app.show()
        multi_page_app.setFixedSize(1152, 864)  # Imposta le dimensioni fisse
        # app_size = multi_page_app.size()
        # print("Dimensioni di MultiPageApp:", app_size.width(), "x", app_size.height())

    app = QApplication(sys.argv)
    login_page = LoginPage(login_success)
    login_page.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
