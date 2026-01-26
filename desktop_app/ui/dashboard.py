from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal

class Dashboard(QWidget):
    navigate_signal = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🏠 Dashboard"))

        btn_expenses = QPushButton("Expenses")
        btn_notes = QPushButton("Notes")

        btn_expenses.clicked.connect(lambda: self.navigate_signal.emit("expenses"))
        btn_notes.clicked.connect(lambda: self.navigate_signal.emit("notes"))


        layout.addWidget(btn_expenses)
        layout.addWidget(btn_notes)


        self.setLayout(layout)
