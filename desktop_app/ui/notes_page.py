from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
import requests
from services import expense_api_service
from models.expense_model import Expense
from ui.expense_page.expense_dialog import ExpenseDialog
from ui.expense_page.expense_charts_widget import ChartWidget
from datetime import datetime
from PySide6.QtCore import Signal
from services import expense_api_service


from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QTextEdit, QLineEdit, QMessageBox, QLabel
)
from PySide6.QtCore import Signal
from services.notes_api_service import get_notes, create_note, update_note, delete_note
from models.note_model import Note


class NotesPage(QWidget):
    """
    NotesPage allows users to manage their notes: view, add, edit, delete.
    The layout matches ExpensesPage style for easier navigation integration.
    """

    navigate_signal = Signal(str)  # Signal for NavigationController

    def __init__(self, token=None):
        """
        Initialize the NotesPage.

        Args:
            token (str, optional): Authentication token, passed from NavigationController.
        """
        super().__init__()
        self.token = token
        self.selected_note_id = None

        self.setWindowTitle("Notes")
        self.layout = QVBoxLayout(self)  # Main vertical layout (like ExpensesPage)

        # --- Notes list ---
        self.notes_list = QListWidget()
        self.notes_list.setFixedWidth(320)
        self.notes_list.itemSelectionChanged.connect(self.load_selected_note)
        self.layout.addWidget(self.notes_list)

        # --- Editor fields ---
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Title")
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Write your note here...")
        self.layout.addWidget(QLabel("Title:"))
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(QLabel("Content:"))
        self.layout.addWidget(self.content_input)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.refresh_btn = QPushButton("Refresh")
        self.back_btn = QPushButton("⬅ Back to Dashboard")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.back_btn)
        self.layout.addLayout(btn_layout)

        # --- Connect buttons ---
        self.add_btn.clicked.connect(self.add_note)
        self.update_btn.clicked.connect(self.edit_note)
        self.delete_btn.clicked.connect(self.delete_note)
        self.refresh_btn.clicked.connect(self.load_notes)
        self.back_btn.clicked.connect(lambda: self.navigate_signal.emit("dashboard"))

        # Load notes on init
        self.load_notes()

    # --------------------------
    # Load notes from backend
    # --------------------------
    def load_notes(self):
        try:
            notes = get_notes()
            self.notes_list.clear()
            for n in notes:
                title = n.title if n.title else "(untitled)"
                self.notes_list.addItem(f"{n.id} - {title}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load notes: {e}")

    # --------------------------
    # Load selected note into editor
    # --------------------------
    def load_selected_note(self):
        selected = self.notes_list.currentItem()
        if not selected:
            self.selected_note_id = None
            self.title_input.clear()
            self.content_input.clear()
            return

        try:
            note_id = int(selected.text().split(" - ")[0])
        except Exception:
            return

        try:
            notes = get_notes()
            note = next((n for n in notes if n.id == note_id), None)
            if note:
                self.selected_note_id = note.id
                self.title_input.setText(note.title)
                self.content_input.setText(note.content)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load note: {e}")

    # --------------------------
    # CRUD Methods
    # --------------------------
    def add_note(self):
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        if not title:
            QMessageBox.warning(self, "Validation Error", "Title cannot be empty")
            return
        try:
            create_note(title, content)
            QMessageBox.information(self, "Success", "Note added successfully!")
            self.title_input.clear()
            self.content_input.clear()
            self.load_notes()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add note: {e}")

    def edit_note(self):
        if not self.selected_note_id:
            QMessageBox.warning(self, "Warning", "Select a note first")
            return
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        try:
            update_note(self.selected_note_id, title, content)
            QMessageBox.information(self, "Success", "Note updated successfully!")
            self.load_notes()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update note: {e}")

    def delete_note(self):
        if not self.selected_note_id:
            QMessageBox.warning(self, "Warning", "Select a note first")
            return
        confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this note?")
        if confirm != QMessageBox.Yes:
            return
        try:
            delete_note(self.selected_note_id)
            QMessageBox.information(self, "Deleted", "Note deleted successfully!")
            self.title_input.clear()
            self.content_input.clear()
            self.load_notes()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to delete note: {e}")