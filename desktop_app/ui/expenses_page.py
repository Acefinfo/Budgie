# desktop_app/ui/expenses_page.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal

class ExpensesPage(QWidget):
    navigate_signal = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("💰 Expense Tracker Page"))
        btn_back = QPushButton("Back to Dashboard")
        btn_back.clicked.connect(lambda: self.navigate_signal.emit("dashboard"))
        layout.addWidget(btn_back)
        self.setLayout(layout)
