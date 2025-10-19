# desktop_app/ui/login_window.py
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Signal
import webbrowser, threading, time
from utils.oauth_server import start_callback_server, OAuthCallbackHandler

class LoginWindow(QMainWindow):
    """
    A window that allows the user to log in using Google OAuth. It opens a browser for the user 
    to authenticate with Google, waits for the authentication callback, and then emits a signal 
    with the OAuth access token.

    Signals:
        login_success (Signal): Emitted when the login is successful, passing the OAuth token.
    """
    login_success = Signal(str)  # Emit the token string on successful login

    def __init__(self):
        """
        Initializes the LoginWindow and sets up the UI components.

        The UI contains a label and a button. When the user clicks the 'Login with Google' button, 
        the OAuth authentication flow begins.
        """
        super().__init__()
        self.setWindowTitle("Login - Expense Tracker")
        self.resize(400, 250)

        layout = QVBoxLayout()
        self.label = QLabel("🔐 Please log in with Google")
        self.login_btn = QPushButton("Login with Google")
        self.login_btn.clicked.connect(self.handle_login)

        layout.addWidget(self.label)
        layout.addWidget(self.login_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle_login(self):
        """
        Handles the login process. It starts a callback server, opens the authentication URL in 
        the user's default web browser, and listens for the callback containing the OAuth token.

        Once the token is received, it updates the UI and emits the `login_success` signal.
        """
        port = 5000
        server = start_callback_server(port)
        auth_url = f"http://127.0.0.1:8000/auth/google/login"
        webbrowser.open(auth_url)
        self.label.setText("🌐 Waiting for Google login...")

        def wait_for_callback():
            """
            Waits for the OAuth callback to receive the access token. Once the token is obtained, 
            it shuts down the server, updates the UI, and emits the login_success signal.
            """
            while OAuthCallbackHandler.access_token is None:
                time.sleep(1)   # Poll every second for the token
            token = OAuthCallbackHandler.access_token
            server.shutdown()    # Shutdown the server after receiving the token
            self.label.setText("✅ Login successful!")
            self.login_success.emit(token)

        threading.Thread(target=wait_for_callback, daemon=True).start() # Run the callback listener in a separate thread
