from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QFrame
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Signal, Qt
from services import expense_api_service
from models.expense_model import Expense
from ui.expense_page.expense_dialog import ExpenseDialog
from ui.expense_page.expense_charts_widget import ChartWidget


class ExpensesPage(QWidget):
    navigate_signal = Signal(str)  # Signal for navigation

    def __init__(self, token=None):
        super().__init__()
        self.token = token
        self.setWindowTitle("Expenses")

        # --- Global Style ---
        self.setStyleSheet("""
            QWidget {
                background-color: #f2f4f7;
                color: #000;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QFrame#MainCard {
                background-color: #ffffff;
                border-radius: 14px;
                padding: 20px;
                border: 1px solid rgba(0, 0, 0, 0.06);
            }
            QPushButton {
                background-color: #453c6e;
                color: #ffffff;
                border-radius: 8px;
                padding: 6px 16px;
                font-weight: 600;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5b5191;
            }
            QTableWidget {
                background-color: #ffffff;
                border-radius: 8px;
                gridline-color: #e0e0e0;
                color: #000;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #453c6e;
                color: #ffffff;
                font-weight: bold;
                border: none;
                height: 30px;
            }
            QTableWidget::item:selected {
                background-color: #d6d3ea;
                color: #000;
            }
        """)

        # --- Layout ---
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(30, 30, 30, 30)

        self.card = QFrame()
        self.card.setObjectName("MainCard")
        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(15)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Description", "Amount"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        card_layout.addWidget(self.table)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.back_btn = QPushButton("⬅ Back to Dashboard")
        for btn in [self.add_btn, self.edit_btn, self.delete_btn, self.back_btn]:
            btn.setCursor(Qt.PointingHandCursor)
            btn_layout.addWidget(btn)
        card_layout.addLayout(btn_layout)

        # --- Chart ---
        self.charts = ChartWidget()
        self.charts.setStyleSheet("""
            border-radius: 8px;
            background-color: white;
        """)
        card_layout.addWidget(self.charts)

        outer_layout.addWidget(self.card)

        # --- Signals ---
        self.add_btn.clicked.connect(self.add_expense)
        self.edit_btn.clicked.connect(self.edit_expense)
        self.delete_btn.clicked.connect(self.delete_expense)
        self.back_btn.clicked.connect(lambda: self.navigate_signal.emit("dashboard"))

        # --- Load Data ---
        self.load_expenses()

    # --- Existing logic unchanged ---
    def load_expenses(self):
        try:
            expenses = expense_api_service.get_expenses()
            self.populate_table(expenses)
            self.charts.update_chart(expenses)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load expenses: {e}")

    def populate_table(self, expenses):
        self.table.setRowCount(len(expenses))
        for i, e in enumerate(expenses):
            self.table.setItem(i, 0, QTableWidgetItem(str(e.id)))
            self.table.setItem(i, 1, QTableWidgetItem(e.date.strftime("%Y-%m-%d")))
            self.table.setItem(i, 2, QTableWidgetItem(e.category))
            self.table.setItem(i, 3, QTableWidgetItem(e.description))
            self.table.setItem(i, 4, QTableWidgetItem(f"{e.amount:.2f}"))

    def get_selected_expense_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Select", "Please select an expense.")
            return None
        return int(self.table.item(row, 0).text())

    def add_expense(self):
        dialog = ExpenseDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if data is None:
                return
            expense = Expense(id=None, **data)
            try:
                expense_api_service.create_expense(expense)
                self.load_expenses()
                QMessageBox.information(self, "Success", "Expense added successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to add expense: {e}")

    def edit_expense(self):
        expense_id = self.get_selected_expense_id()
        if not expense_id:
            return
        try:
            expenses = expense_api_service.get_expenses()
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
