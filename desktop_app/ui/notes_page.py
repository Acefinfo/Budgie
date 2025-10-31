from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QTextEdit, QLineEdit, QMessageBox, QLabel, QFrame
from PySide6.QtCore import Signal, Qt
from services.notes_api_service import get_notes, create_note, update_note, delete_note
from models.note_model import Note


class NotesPage(QWidget):
    navigate_signal = Signal(str)  # Signal for NavigationController

    def __init__(self, token=None):
        super().__init__()
        self.token = token
        self.selected_note_id = None
        self.setWindowTitle("Notes")

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
            }
            QPushButton:hover {
                background-color: #5b5191;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 6px;
                background-color: #fafafa;
            }
            QListWidget {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)

        # --- Layout ---
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(30, 30, 30, 30)

        self.card = QFrame()
        self.card.setObjectName("MainCard")
        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(15)

        # --- Notes list ---
        self.notes_list = QListWidget()
        self.notes_list.setFixedWidth(320)
        self.notes_list.itemSelectionChanged.connect(self.load_selected_note)
        card_layout.addWidget(self.notes_list)

        # --- Editor fields ---
        card_layout.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Title")
        card_layout.addWidget(self.title_input)

        card_layout.addWidget(QLabel("Content:"))
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Write your note here...")
        card_layout.addWidget(self.content_input)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.refresh_btn = QPushButton("Refresh")
        self.back_btn = QPushButton("⬅ Back to Dashboard")
        for b in [self.add_btn, self.update_btn, self.delete_btn, self.refresh_btn, self.back_btn]:
            b.setCursor(Qt.PointingHandCursor)
            btn_layout.addWidget(b)
        card_layout.addLayout(btn_layout)

        outer_layout.addWidget(self.card)

        # --- Connect buttons ---
        self.add_btn.clicked.connect(self.add_note)
        self.update_btn.clicked.connect(self.edit_note)
        self.delete_btn.clicked.connect(self.delete_note)
        self.refresh_btn.clicked.connect(self.load_notes)
        self.back_btn.clicked.connect(lambda: self.navigate_signal.emit("dashboard"))

        # Load notes
        self.load_notes()

    # -------------------------- Existing logic intact --------------------------
    def load_notes(self):
        try:
            notes = get_notes()
            self.notes_list.clear()
            for n in notes:
                title = n.title if n.title else "(untitled)"
                self.notes_list.addItem(f"{n.id} - {title}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load notes: {e}")

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
