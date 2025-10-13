# desktop_app/controllers/navigation_controller.py
from ui.dashboard import Dashboard
from ui.expenses_page import ExpensesPage
from ui.notes_page import NotesPage
from ui.chat_page import ChatPage

class NavigationController:
    def __init__(self, main_window):
        self.main_window = main_window

    def show_dashboard(self):
        dashboard = Dashboard()
        dashboard.navigate_signal.connect(self.handle_navigation)
        self.main_window.setCentralWidget(dashboard)

    def handle_navigation(self, target):
        if target == "expenses":
            page = ExpensesPage()
        elif target == "notes":
            page = NotesPage()
        elif target == "chat":
            page = ChatPage()
        else:
            from ui.dashboard import Dashboard
            page = Dashboard()

        page.navigate_signal.connect(self.handle_navigation)
        self.main_window.setCentralWidget(page)
