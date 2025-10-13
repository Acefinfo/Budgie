# desktop_app/ui/chat_page.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal

class ChatPage(QWidget):
    navigate_signal = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("💬 Chat Page"))
        btn_back = QPushButton("Back to Dashboard")
        btn_back.clicked.connect(lambda: self.navigate_signal.emit("dashboard"))
        layout.addWidget(btn_back)
        self.setLayout(layout)
