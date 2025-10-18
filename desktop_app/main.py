# desktop_app/main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from services import expense_api_service
from ui.login_window import LoginWindow
from controllers.navigation_controller import NavigationController

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budgie")
        self.resize(800, 600)

        self.login_window = LoginWindow()
        self.setCentralWidget(self.login_window)

        self.login_window.login_success.connect(self.on_login_success)

    # def on_login_success(self, access_token):
    #     self.controller = NavigationController(self, access_token)
    #     self.controller.show_dashboard()
    
    def on_login_success(self, access_token):
        expense_api_service.set_token(access_token)
        self.controller = NavigationController(self, access_token)
        self.controller.show_dashboard()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
