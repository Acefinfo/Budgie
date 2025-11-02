from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QFrame,
    QGraphicsBlurEffect, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal, Qt, QPropertyAnimation
from services import expense_api_service
from models.expense_model import Expense
from ui.expense_page.expense_dialog import ExpenseDialog
from ui.expense_page.expense_charts_widget import ChartWidget


class ExpensesPage(QWidget):
    navigate_signal = Signal(str)

    def __init__(self, token=None):
        super().__init__()
        self.token = token
        self.setWindowTitle("Expenses")

        # --- Global Dark Mode Style ---
        self.setStyleSheet("""
            QWidget {
                background-color: #0f0f12;
                color: #eaeaea;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QFrame#MainCard {
                background-color: rgba(30, 30, 40, 0.75);  /* Semi-transparent dark glass */
                border-radius: 14px;
                padding: 20px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #5a4ea3, stop:1 #453c6e);
                color: #ffffff;
                border-radius: 8px;
                padding: 8px 18px;
                font-weight: 600;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #6d60c5, stop:1 #5b5191);
            }
            QTableWidget {
                background-color: rgba(40, 40, 50, 0.8);
                border-radius: 10px;
                gridline-color: #2e2e3a;
                color: #eaeaea;
                font-size: 14px;
                selection-background-color: #453c6e;
                selection-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #1d1b27;
                color: #c9c9d6;
                font-weight: 600;
                border: none;
                padding: 6px 10px;
                text-transform: uppercase;
            }
            QTableWidget::item:hover {
                background-color: rgba(100, 90, 160, 0.25);
            }
            QScrollBar:vertical {
                background: transparent;
                width: 10px;
                margin: 0px 3px 0 3px;
            }
            QScrollBar::handle:vertical {
                background: rgba(120, 120, 150, 0.3);
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(120, 120, 150, 0.5);
            }
        """)

        # --- Layout ---
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(30, 30, 30, 30)

        # --- Glass Card ---
        self.card = QFrame()
        self.card.setObjectName("MainCard")

        # Apply real blur and shadow for glassy depth
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(20)
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(25)
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(5)
        shadow_effect.setColor(QColor(0, 0, 0, 160))

        # Combine blur + shadow visually
        self.card.setGraphicsEffect(blur_effect)
        self.card.setGraphicsEffect(shadow_effect)

        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(15)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
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
            border-radius: 10px;
            background-color: rgba(40, 40, 50, 0.85);
        """)
        card_layout.addWidget(self.charts)

        outer_layout.addWidget(self.card)

        # --- Smooth fade-in animation ---
        self.fade_anim = QPropertyAnimation(self.card, b"windowOpacity")
        self.fade_anim.setDuration(700)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

        # --- Signals ---
        self.add_btn.clicked.connect(self.add_expense)
        self.edit_btn.clicked.connect(self.edit_expense)
        self.delete_btn.clicked.connect(self.delete_expense)
        self.back_btn.clicked.connect(lambda: self.navigate_signal.emit("dashboard"))

        # --- Load Data ---
        self.load_expenses()

    # --- Logic remains unchanged ---
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

            # --- Amount column: bold + right aligned ---
            amount_item = QTableWidgetItem(f"{e.amount:.2f}")
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            font = amount_item.font()
            font.setBold(True)
            amount_item.setFont(font)
            self.table.setItem(i, 3, amount_item)

            # --- Description column ---
            self.table.setItem(i, 4, QTableWidgetItem(e.description))

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
