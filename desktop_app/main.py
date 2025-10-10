import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel

# --- Configuration ---
BACKEND_URL = "http://127.0.0.1:8000"  # Your FastAPI backend
REDIRECT_HOST = "127.0.0.1"
REDIRECT_PORT = 8081  # Must match GOOGLE_REDIRECT_URI in your .env

# --- Step 1: Temporary local server to capture callback ---
class OAuthHandler(BaseHTTPRequestHandler):
    jwt_token = None

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/callback":
            # Extract access_token from query params
            query = parse_qs(parsed_path.query)
            token = query.get("access_token")
            if token:
                OAuthHandler.jwt_token = token[0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h2>Login Successful! You can close this window.</h2>")
            else:
                self.send_response(400)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h2>Login Failed.</h2>")

def start_local_server():
    """Start a temporary HTTP server to wait for OAuth callback"""
    server = HTTPServer((REDIRECT_HOST, REDIRECT_PORT), OAuthHandler)
    server.handle_request()  # Handle a single request then stop
    return OAuthHandler.jwt_token

# --- Step 2: PySide6 GUI ---
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budgie - Login")
        self.setFixedSize(300, 150)

        self.layout = QVBoxLayout()
        self.label = QLabel("Click below to login with Google")
        self.button = QPushButton("Login with Google")
        self.button.clicked.connect(self.login_google)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.jwt_token = None

    # def login_google(self):
    #     self.label.setText("Opening Google Sign-in...")

    #     # Start local server thread to capture callback
    #     threading.Thread(target=self.wait_for_callback, daemon=True).start()


    #     # Open the backend Google login route in browser
    #     webbrowser.open(f"{BACKEND_URL}/auth/google/login")

    def login_google(self):
        self.label.setText("Opening Google Sign-in...")

        # Start local server thread first
        threading.Thread(target=self.wait_for_callback, daemon=True).start()

        # Then open Google login
        webbrowser.open(f"{BACKEND_URL}/auth/google/login")


    
    def wait_for_callback(self):
        token = start_local_server()
        if token:
            self.jwt_token = token
            self.label.setText("✅ Logged in successfully!")
            print(f"JWT Token: {token}")
        else:
            self.label.setText("❌ Login failed.")


# --- Run App ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
