from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDateEdit, QDialogButtonBox, QMessageBox
from PySide6.QtCore import QDate
from datetime import datetime

# Popup dialogue for adding or editing an exxpense
class ExpenseDialog(QDialog):
    def __init__(self,parent = None, expense = None):
        super().__init__(parent)
        self.setWindowTitle("Expense" + (" Edit" if expense else " Add"))
        # self.setWindowTitle("Add / Edit Expense")


        self.layout = QFormLayout(self)

        # Input fiends
        self.amount_input = QLineEdit()
        self.category_input = QLineEdit()
        self.description_input = QLineEdit()
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate()) # Default to today


        # Add fields to layout
        self.layout.addRow("Amount:", self.amount_input)
        self.layout.addRow("Category:", self.category_input)
        self.layout.addRow("Description:", self.description_input)
        self.layout.addRow("Date:", self.date_input)


        # OK and Cancle buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)


        # If editing an existing expense
        if expense:
            self.amount_input.setText(str(expense.amount))
            self.category_input.setText(expense.category)
            self.description_input.setText(expense.description)
            self.date_input.setDate(QDate(expense.date.year, expense.date.month, expense.date.day))

    def get_data(self):
        amount_text = self.amount_input.text().strip()

        if not amount_text:
            QMessageBox.warning(self, "Missing data","Please enter an amount before adding expense.")
            return None
        
        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid input", "Amount must be a valid number.")
        
        category = self.category_input.text().strip()
        if not category:
            QMessageBox.warning(self, "Missing Data", "Please enter a category.")
            return None

        return {
        "amount": amount,
        "category": category,
        "description": self.description_input.text().strip(),
        "date": datetime.combine(
            self.date_input.date().toPython(),
            datetime.min.time()
        ),
                    
    }