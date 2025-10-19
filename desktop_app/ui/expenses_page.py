# # desktop_app/ui/expenses_page.py
# from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
# from PySide6.QtCore import Signal

# class ExpensesPage(QWidget):
#     navigate_signal = Signal(str)

#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         layout.addWidget(QLabel("💰 Expense Tracker Page"))
#         btn_back = QPushButton("Back to Dashboard")
#         btn_back.clicked.connect(lambda: self.navigate_signal.emit("dashboard"))
#         layout.addWidget(btn_back)
#         self.setLayout(layout)



from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
import requests
from services import expense_api_service
from models.expense_model import Expense
from ui.expense_page.expense_dialog import ExpenseDialog
from ui.expense_page.expense_charts_widget import ChartWidget
from datetime import datetime
from PySide6.QtCore import Signal
from services import expense_api_service

# Main expense page 

class ExpensesPage(QWidget):
    navigate_signal = Signal(str)

    def __init__(self, token=None):
        super().__init__()
        self.token = token
        self.setWindowTitle("Expense Tracker")
        self.layout = QVBoxLayout(self)

        # Filter/ Serch bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Filter by category...")
        self.search_box.textChanged.connect(self.load_expenses)
        self.layout.addWidget(self.search_box)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Description", "Amount"])
        self.layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        self.layout.addLayout(btn_layout)

        # Chart 
        self.charts = ChartWidget()
        self.layout.addWidget(self.charts)

        # Connect buttons to actions
        self.add_btn.clicked.connect(self.add_expense)
        self.edit_btn.clicked.connect(self.edit_expense)
        self.delete_btn.clicked.connect(self.delete_expense)

        # Load expenses initially
        self.load_expenses()
    
    
    # Fetch expenses from backend and apply filter
    # def load_expenses(self):
    #     if not self.token:
    #         QMessageBox.warning(self, "Error", "Authentication token not set")
    #         return

    #     headers = {"Authorization": f"Bearer {self.token}"}
    #     try:
    #         response = requests.get("http://127.0.0.1:8000/expenses/", headers=headers)
    #         if response.status_code == 200:
    #             data = response.json()
    #             # populate your table or chart here
    #         else:
    #             QMessageBox.warning(self, "Error", f"Failed to load expenses: {response.text}")
    #     except Exception as e:
    #         QMessageBox.warning(self, "Error", f"Failed to connect to backend: {e}")
    def load_expenses(self):   
        try:
            # Fetch expenses from backend
            expenses = expense_api_service.get_expenses()

            # Populate table
            self.populate_table(expenses)

            # Update chart
            self.charts.update_chart(expenses)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load expenses: {e}")


    # Fill table with expense data
    def populate_table(self, expenses):
        self.table.setRowCount(len(expenses))
        for i, e in enumerate(expenses):
            self.table.setItem(i, 0, QTableWidgetItem(str(e.id)))
            self.table.setItem(i, 1, QTableWidgetItem(e.date.strftime("%Y-%m-%d")))
            self.table.setItem(i, 2, QTableWidgetItem(e.category))
            self.table.setItem(i, 3, QTableWidgetItem(e.description))
            self.table.setItem(i, 4, QTableWidgetItem(f"{e.amount:.2f}"))

    # Get currently selected expense ID from table
    def get_selected_expense_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Select", "Please select an expense.")
            return None
        return int(self.table.item(row, 0).text())
    
    # Add a new expense
    # def add_expense(self):
    #     dialog = ExpenseDialog(self)
    #     data = dialog.get_data()
    #     expense = Expense(id=None,**data)
    #     expense_api_service._create_expense()
    #     self.load_expenses()
    
    def add_expense(self):
        dialog = ExpenseDialog(self)

        if dialog.exec():  # Wait for OK
            data = dialog.get_data()
            if data is None:
                return

            expense = Expense(id=None, **data)

            try:
                expense_api_service.create_expense(expense)  # ✅ just one argument
                self.load_expenses()
                QMessageBox.information(self, "Success", "Expense added successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to add expense: {e}")


    # Edit selected expense
    def edit_expense(self):
        expense_id = self.get_selected_expense_id()
        if not expense_id:
            return

        try:
            expenses = expense_api_service.get_expenses()  # <-- Corrected here
            expense = next((e for e in expenses if e.id == expense_id), None)

            if not expense:
                QMessageBox.warning(self, "Error", "Expense not found.")
                return

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
        expense_id = self.get_selected_expense_id()
        if not expense_id:
            return
        
        confirm = QMessageBox.question(self, "Confirm", "Delete this expense?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            expense_api_service.delete_expense(expense_id)
            self.load_expenses()
        


