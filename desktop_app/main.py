import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from services import expense_api_service
from ui.login_window import LoginWindow
from controllers.navigation_controller import NavigationController

class MainApp(QMainWindow):
    """
    Main application window that serves as the entry point for the application. 
    It initializes the login screen and handles successful login events by 
    navigating to the dashboard.

    Signals:
        login_success (Signal): Emitted when the user successfully logs in, passing the OAuth access token.
    """
    def __init__(self):
        """
        Initializes the main application window.

        Sets up the window title, size, and layout. Initially, the `LoginWindow` is displayed 
        as the central widget. When the user logs in successfully, the `on_login_success` method 
        is called to handle navigation to the dashboard.
        """
        super().__init__()
        self.setWindowTitle("Budgie")
        self.resize(800, 600)

        self.login_window = LoginWindow()
        self.setCentralWidget(self.login_window)

        self.login_window.login_success.connect(self.on_login_success)


    def on_login_success(self, access_token):
        """
        This method is called when the user successfully logs in.

        It receives the access token from the login window, sets the token for the API service,
        and initializes the `NavigationController` to show the dashboard.

        Args:
            access_token (str): The OAuth access token received after a successful login.
        """
        expense_api_service.set_token(access_token) # Set the global token for the API service
        self.controller = NavigationController(self, access_token)  # Create the navigation controller
        self.controller.show_dashboard()


if __name__ == "__main__":
    """
    Entry point for the application. It creates the QApplication instance, 
    initializes the main application window, and starts the event loop.
    """
    app = QApplication(sys.argv)    # Create the application
    window = MainApp()  # Initialize the main window
    window.show()   # Display the window
    sys.exit(app.exec())    # Start the application event loop and handle exit
