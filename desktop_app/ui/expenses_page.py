from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
import requests
from services import expense_api_service
from models.expense_model import Expense
from ui.expense_page.expense_dialog import ExpenseDialog
from ui.expense_page.expense_charts_widget import ChartWidget
from datetime import datetime
from PySide6.QtCore import Signal
from services import expense_api_service


class ExpensesPage(QWidget):
    """
    The ExpensesPage class represents the expense management page in the application. 
    It displays a list of expenses in a table, provides functionality to add, edit, and delete expenses, 
    and shows a chart visualization of expenses.
    """

    navigate_signal = Signal(str)   # Signal for navigation between pages (like dashboard)

    def __init__(self, token=None):
        """
        Initializes the ExpensesPage widget.
        
        Args:
            token (str, optional): An optional authentication token.
        """
        super().__init__()
        self.token = token
        self.setWindowTitle("Expense")  # Sets the window title
        self.layout = QVBoxLayout(self) # Main vertival layout of the page

        # Table setup: Create a table to display expense data
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID","Date", "Category", "Description", "Amount"])
        self.layout.addWidget(self.table)   # Add table to the layout

        # Buttons layout: Create buttons for Add, Edit, Delete, and Back to Dashboard
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.back_btn = QPushButton("⬅ Back to Dashboard")

        # Add buttons to the button layout
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.back_btn)
        self.layout.addLayout(btn_layout)    # Add button layout to the main layout

        # Chart widget: Add the chart to visualize expenses
        self.charts = ChartWidget()
        self.layout.addWidget(self.charts)

        # Connect button actions to their respective methods
        self.add_btn.clicked.connect(self.add_expense)
        self.edit_btn.clicked.connect(self.edit_expense)
        self.delete_btn.clicked.connect(self.delete_expense)
        self.back_btn.clicked.connect(lambda: self.navigate_signal.emit("dashboard"))

        # Load the list of expenses when the page is initialized
        self.load_expenses()
    

    def load_expenses(self):  
        """
        Fetches the list of expenses from the backend and updates the table and chart.
        If an error occurs while fetching the data, an error message is displayed.
        """ 
        try:
            # Fetch expenses from backend
            expenses = expense_api_service.get_expenses()
            # Populate table
            self.populate_table(expenses)
            # Update chart
            self.charts.update_chart(expenses)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load expenses: {e}")


 
    def populate_table(self, expenses):
        """
        Populates the table widget with the expense data.
        
        Args:
            expenses (list): List of expense objects to display.
        """
        self.table.setRowCount(len(expenses))   # Set the number of rows in the table
        for i, e in enumerate(expenses):
            # Set data in each table cell for each expense
            self.table.setItem(i, 0, QTableWidgetItem(str(e.id)))
            self.table.setItem(i, 1, QTableWidgetItem(e.date.strftime("%Y-%m-%d")))
            self.table.setItem(i, 2, QTableWidgetItem(e.category))
            self.table.setItem(i, 3, QTableWidgetItem(e.description))
            self.table.setItem(i, 4, QTableWidgetItem(f"{e.amount:.2f}"))

    def get_selected_expense_id(self):
        """
        Retrieves the ID of the currently selected expense in the table.
        
        Returns:
            int: The ID of the selected expense, or None if no expense is selected.
        """
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Select", "Please select an expense.")
            return None
        return int(self.table.item(row, 0).text())
    
# ==============================================
#
#       CRUD FUNCTIONALITY
#
# ==============================================

    def add_expense(self):
        """
        Opens a dialog to add a new expense. If successful, the expense is added 
        to the backend and the table is reloaded with the updated list of expenses.
        """
        dialog = ExpenseDialog(self)    # Open the ExpenseDialog to add a new expense

        if dialog.exec():    # Wait for the user to confirm the action (OK)
            data = dialog.get_data()
            if data is None:
                return

            expense = Expense(id=None, **data)  # Create a new Expense object with the entered data

            try:
                # Send the new expense data to the backend
                expense_api_service.create_expense(expense) 
                self.load_expenses()    # Reload expenses after adding
                QMessageBox.information(self, "Success", "Expense added successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to add expense: {e}")

    def edit_expense(self):
        """
        Opens a dialog to edit the selected expense. If successful, the changes are
        sent to the backend and the list of expenses is updated.
        """
        expense_id = self.get_selected_expense_id() # Get the selected expense ID
        if not expense_id:
            return

        try:
            # Fetch all expenses from the backend
            expenses = expense_api_service.get_expenses() 
            # Find the expense to edit by matching its ID
            expense = next((e for e in expenses if e.id == expense_id), None)

            if not expense:
                QMessageBox.warning(self, "Error", "Expense not found.")
                return

            # Open the ExpenseDialog to edit the selected expense
            dialog = ExpenseDialog(self, expense)
            if dialog.exec():
                data = dialog.get_data()
                updated_expense = Expense(id=expense_id, **data)
                expense_api_service.update_expense(expense_id, updated_expense)
                QMessageBox.information(self, "Success", "Expense updated successfully!")
                self.load_expenses()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to edit expense: {e}")
        
    def delete_expense(self):
        """
        Deletes the selected expense after confirming with the user. 
        If successful, the list of expenses is reloaded.
        """
        expense_id = self.get_selected_expense_id()
        if not expense_id:
            return
        
        # Show a confirmation dialog before deleting
        confirm = QMessageBox.question(self, "Confirm", "Delete this expense?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            expense_api_service.delete_expense(expense_id)
            self.load_expenses()
        


