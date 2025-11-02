from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QTextEdit, QLineEdit, QMessageBox, QLabel, QFrame, QGraphicsBlurEffect, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
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

        # --- Global Dark Mode Style (matching ExpensesPage) ---
        self.setStyleSheet("""
            QWidget {
                background-color: #0f0f12;
                color: #eaeaea;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QFrame#MainCard {
                background-color: rgba(30,30,40,0.75);
                border-radius: 14px;
                padding: 20px;
                border: 1px solid rgba(255,255,255,0.05);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #5a4ea3, stop:1 #453c6e);
                color: #ffffff;
                border-radius: 8px;
                padding: 8px 18px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #6d60c5, stop:1 #5b5191);
            }
            QLineEdit, QTextEdit {
                border: 1px solid #2e2e3a;
                border-radius: 8px;
                padding: 6px;
                background-color: rgba(40,40,50,0.8);
                color: #eaeaea;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #6d60c5;
                background-color: rgba(50,50,65,0.85);
            }
            QListWidget {
                background-color: rgba(40,40,50,0.8);
                border-radius: 8px;
                border: 1px solid #2e2e3a;
                color: #eaeaea;
            }
            QListWidget::item:hover {
                background-color: rgba(100,90,160,0.25);
            }
            QListWidget::item:selected {
                background-color: #453c6e;
                color: #ffffff;
            }
            QFrame#Divider {
                background-color: #2e2e3a;
                max-width: 1px;
            }
        """)

        # --- Layout ---
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(30, 30, 30, 30)

        # --- Main Card ---
        self.card = QFrame()
        self.card.setObjectName("MainCard")

        # Blur + shadow effect for glassy depth
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(20)
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(25)
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(5)
        shadow_effect.setColor(QColor(0, 0, 0, 160))

        self.card.setGraphicsEffect(blur_effect)
        self.card.setGraphicsEffect(shadow_effect)

        card_layout = QHBoxLayout(self.card)
        card_layout.setSpacing(20)

        # --- Left Panel: Notes List ---
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Notes"))
        self.notes_list = QListWidget()
        self.notes_list.setFixedWidth(300)
        self.notes_list.itemSelectionChanged.connect(self.load_selected_note)
        left_panel.addWidget(self.notes_list)
        card_layout.addLayout(left_panel)

        # --- Divider ---
        divider = QFrame()
        divider.setObjectName("Divider")
        card_layout.addWidget(divider)

        # --- Right Panel: Note Details ---
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Title")
        right_panel.addWidget(self.title_input)

        right_panel.addWidget(QLabel("Content:"))
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Write your note here...")
        right_panel.addWidget(self.content_input)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.clear_btn = QPushButton("Clear")  # Replaces Refresh button
        self.back_btn = QPushButton("⬅ Back to Dashboard")
        for b in [self.add_btn, self.update_btn, self.delete_btn, self.clear_btn, self.back_btn]:
            b.setCursor(Qt.PointingHandCursor)
            btn_layout.addWidget(b)
        right_panel.addLayout(btn_layout)

        card_layout.addLayout(right_panel)
        outer_layout.addWidget(self.card)

        # --- Connect Buttons ---
        self.add_btn.clicked.connect(self.add_note)
        self.update_btn.clicked.connect(self.edit_note)
        self.delete_btn.clicked.connect(self.delete_note)
        self.clear_btn.clicked.connect(self.clear_note_details)  # Connect clear button
        self.back_btn.clicked.connect(lambda: self.navigate_signal.emit("dashboard"))

        # Load notes
        self.load_notes()

    # -------------------------- Logic --------------------------
    def clear_note_details(self):
        """Clear right panel inputs and deselect note safely"""
        self.title_input.clear()
        self.content_input.clear()
        self.selected_note_id = None

        # Deselect the note without triggering load_selected_note
        self.notes_list.blockSignals(True)
        self.notes_list.clearSelection()
        self.notes_list.blockSignals(False)

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
            self.clear_note_details()
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
            self.clear_note_details()
            self.load_notes()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to delete note: {e}")
