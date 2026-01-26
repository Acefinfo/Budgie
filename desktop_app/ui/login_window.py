from PySide6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFrame
)
from PySide6.QtGui import QPixmap, QFont, QColor
from PySide6.QtCore import Signal, Qt, QEvent, QTimer
import webbrowser, threading, time, math
from utils.oauth_server import start_callback_server, OAuthCallbackHandler
import os


class HoverButton(QPushButton):
    """
    A custom QPushButton subclass that adds hover and press effects.

    This button visually responds when hovered, pressed, or released to 
    improve the user experience through color changes.
    """
    def __init__(self, text):
        """
        Initialize the HoverButton with specific colors and styles.

        Args:
            text (str): The text label displayed on the button.
        """
        super().__init__(text)

        # Define color states for default, hover, and pressed
        self.default_color = "#7b5fff"
        self.hover_color = "#9b7fff"
        self.pressed_color = "#4caf50"

        # Apply the initial button style
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.default_color};
                color: white;
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
                padding: 10px 20px;
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)   # Change cursor to a pointing hand on hover
        self.installEventFilter(self)   # Enable event filtering to detect mouse events

    def eventFilter(self, obj, event):
        """
        Detect and apply color changes for hover and press states.
        """
        if event.type() == QEvent.Enter:
            # When the mouse enters, use hover color
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.hover_color};
                    color: white;
                    border-radius: 10px;
                    font-size: 15px;
                    font-weight: bold;
                    padding: 10px 20px;
                }}
            """)
        elif event.type() == QEvent.Leave:
            # When the mouse leaves, return to default color
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.default_color};
                    color: white;
                    border-radius: 10px;
                    font-size: 15px;
                    font-weight: bold;
                    padding: 10px 20px;
                }}
            """)
        elif event.type() == QEvent.MouseButtonPress:
            # On click, apply pressed color
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.pressed_color};
                    color: white;
                    border-radius: 10px;
                    font-size: 15px;
                    font-weight: bold;
                    padding: 10px 20px;
                }}
            """)
        elif event.type() == QEvent.MouseButtonRelease:
            # On release, revert to hover color
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.hover_color};
                    color: white;
                    border-radius: 10px;
                    font-size: 15px;
                    font-weight: bold;
                    padding: 10px 20px;
                }}
            """)
        return super().eventFilter(obj, event)


class LoginWindow(QMainWindow):
    """
    LoginWindow provides the main interface for user authentication using Google OAuth.
    
    It includes:
    - A visually animated background with a smooth gradient.
    - A central login card containing the app logo, title, and a Google login button.
    - A signal (`login_success`) emitted once a user successfully authenticates.
    """
    login_success = Signal(str) # Signal emitted when login succeeds (emits access token)

    def __init__(self):
        """
        Initialize the LoginWindow and set up the entire user interface layout,
        including the animated background, login button, logo, and labels.
        """
        super().__init__()
        self.setWindowTitle("Login - Budgie")
        self.resize(700, 550)

        # Define six colors that will be used to animate the gradient background.
        # The colors transition smoothly to create a visually appealing motion effect.
        self.gradient_colors = [
            QColor(45, 32, 55),
            QColor(50, 36, 60),
            QColor(55, 40, 65),
            QColor(60, 45, 70),
            QColor(65, 50, 75),
            QColor(70, 55, 85)
        ]

         # --- MAIN UI SETUP ---

        # Create a central widget and layout that centers all content.
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # --- LOGIN CARD SETUP ---
        # The card widget acts as a container for the login form.
        self.card = QWidget()
        self.card.setFixedSize(420, 400)
        self.card.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.03);
                border-radius: 20px;
                border: none;
            }
        """)
        card_layout = QVBoxLayout()
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(20, 20, 20, 20)
        self.card.setLayout(card_layout)

        # --- APP LOGO SECTION ---
        self.logo_label = QLabel()
        current_dir = os.path.dirname(os.path.abspath(__file__))    # Dynamically resolve the path to the app logo image
        project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
        logo_path = os.path.join(project_root, "assets", "Budgie_Logo.png")
       
        # Attempt to load the logo image
        pixmap = QPixmap(logo_path)
        if pixmap.isNull():
            print(f"⚠️ Logo not found at: {logo_path}")
        else:
            # Resize and preserve aspect ratio of the logo
            pixmap = pixmap.scaled(
                120, 120, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setStyleSheet("background: transparent;")
        card_layout.addWidget(self.logo_label)

        # --- TITLE SECTION ---
        title_label = QLabel("Welcome to Budgie")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ffffff; background: transparent;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_label)

        # --- SUBTITLE SECTION ---
        self.label = QLabel("🔐 Please log in with Google")
        self.label.setFont(QFont("Segoe UI", 13))
        self.label.setStyleSheet("color: #c0c0c0; background: transparent;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.label)

        # --- DIVIDER LINE ---
        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet("""
            background-color: #7b5fff;
            border: none;
        """)
        card_layout.addWidget(line)

        # --- LOGIN BUTTON ---
        # Uses the custom HoverButton class for hover/click effects.
        self.login_btn = HoverButton("Login with Google")
        self.login_btn.setFixedWidth(220)
        # Connect button click to the login handler function
        self.login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- FOOTER LABEL ---
        footer_label = QLabel("© 2025 Budgie Inc.")
        footer_label.setFont(QFont("Segoe UI", 9))
        footer_label.setStyleSheet("color: #808080; background: transparent;")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(footer_label)

        # Add the complete card to the central layout
        main_layout.addWidget(self.card, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- BACKGROUND ANIMATION TIMER ---
        # A QTimer repeatedly triggers `animate_background()` to smoothly transition the gradient.
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_background)
        self.timer.start(30)    # Update every 30 milliseconds (~33 FPS)

    def animate_background(self):
        """
        Animate the background using a dynamic linear gradient that moves diagonally.

        This function is triggered by a QTimer to create a subtle "shifting light" effect.
        The gradient's position oscillates over time using a sine wave for smooth motion.
        """
        t = time.time() # Current timestamp for animation timing
        num_stops = len(self.gradient_colors)

        # Generate an oscillating offset value between 0 and 1
        # The sine wave ensures continuous smooth motion.
        offset = (math.sin(t * 0.2) + 1) / 2  # normalized 0..1

        # Define start and end points of the diagonal gradient
        x1, y1 = 0 - 0.2 + offset * 0.4, 0 - 0.2 + offset * 0.4
        x2, y2 = 1 - 0.2 + offset * 0.4, 1 - 0.2 + offset * 0.4

        # Calculate evenly spaced stop positions for each color
        stop_positions = [i / (num_stops - 1) for i in range(num_stops)]

        # Format the gradient stops into a CSS-style string
        gradient_stops = ",\n".join(
            f"stop:{stop_positions[i]:.3f} {self.gradient_colors[i].name()}"
            for i in range(num_stops)
        )

        # Apply the dynamically computed gradient to the window's background
        style = f"""
            QMainWindow {{
                background-color: qlineargradient(
                    x1:{x1:.3f}, y1:{y1:.3f},
                    x2:{x2:.3f}, y2:{y2:.3f},
                    {gradient_stops}
                );
            }}
        """
        self.setStyleSheet(style)

    def handle_login(self):
        """
        Handle the Google OAuth login process.

        Steps:
        1. Start a local callback server to listen for the OAuth redirect.
        2. Open the Google authentication URL in the user's default web browser.
        3. Wait asynchronously for the OAuth response containing the access token.
        4. Once received, shut down the server, update the UI, and emit the `login_success` signal.

        This method uses a background thread to avoid freezing the UI while waiting
        for the OAuth callback.
        """
        port = 5000
        server = start_callback_server(port)    # Start a local HTTP server to handle OAuth callback
        auth_url = f"http://127.0.0.1:8000/auth/google/login"
        webbrowser.open(auth_url)   # Open Google login page in the user's web browser
        self.label.setText("🌐 Waiting for Google login...")

        # Define background thread function to monitor OAuth callback
        def wait_for_callback():
            while OAuthCallbackHandler.access_token is None:    # Continuously check until the access token is available
                time.sleep(1)

            token = OAuthCallbackHandler.access_token   # Retrieve token once available
            server.shutdown() # Shut down the temporary callback server to free the port
            self.label.setText("✅ Login successful!")  # Update label to indicate successful login
            self.login_success.emit(token)   # Emit signal so other components (e.g., main app) can receive the token

        # Start the waiting loop in a separate daemon thread to avoid blocking the UI
        threading.Thread(target=wait_for_callback, daemon=True).start()
