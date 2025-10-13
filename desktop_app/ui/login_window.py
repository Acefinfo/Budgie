# desktop_app/ui/login_window.py
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Signal
import webbrowser, threading, time
from utils.oauth_server import start_callback_server, OAuthCallbackHandler

class LoginWindow(QMainWindow):
    login_success = Signal(str)  # emit token string

    def __init__(self):
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
        port = 5000
        server = start_callback_server(port)
        auth_url = f"http://127.0.0.1:8000/auth/google/login"
        webbrowser.open(auth_url)
        self.label.setText("🌐 Waiting for Google login...")

        def wait_for_callback():
            while OAuthCallbackHandler.access_token is None:
                time.sleep(1)
            token = OAuthCallbackHandler.access_token
            server.shutdown()
            self.label.setText("✅ Login successful!")
            self.login_success.emit(token)

        threading.Thread(target=wait_for_callback, daemon=True).start()
