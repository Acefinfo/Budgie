from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDateEdit, QDialogButtonBox, QMessageBox
from PySide6.QtCore import QDate
from datetime import datetime

# Popup dialogue for adding or editing an exxpense
class ExpenseDialog(QDialog):
    """
    A dialog window for adding or editing an expense entry. It provides input fields 
    for the amount, category, description, and date of the expense. The user can 
    either save the new or edited expense, or cancel the operation.

    Attributes:
        amount_input (QLineEdit): Input field for the expense amount.
        category_input (QLineEdit): Input field for the expense category.
        description_input (QLineEdit): Input field for the expense description.
        date_input (QDateEdit): Input field for the date of the expense.
        buttons (QDialogButtonBox): Buttons for confirming or canceling the action.
    """
    def __init__(self,parent = None, expense = None):
        """
        Initializes the dialog, either for adding a new expense or editing an existing one.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
            expense (Expense, optional): An existing expense object to edit. Defaults to None.
        """
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


        # If editing an existing expense, populate fields with its data
        if expense:
            self.amount_input.setText(str(expense.amount))
            self.category_input.setText(expense.category)
            self.description_input.setText(expense.description)
            self.date_input.setDate(QDate(expense.date.year, expense.date.month, expense.date.day))

    def get_data(self):
        """
        Retrieves the data entered in the input fields and validates it. 

        Returns:
            dict: A dictionary containing the expense data with keys 'amount', 'category', 
                  'description', and 'date'.
            
        Raises:
            QMessageBox.warning: If any of the required fields are missing or invalid.
        """
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