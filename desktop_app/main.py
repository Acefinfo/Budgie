# desktop_app/main.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
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

    def on_login_success(self, code):
        self.controller = NavigationController(self)
        self.controller.show_dashboard()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
