from services import expense_api_service
from ui.dashboard import Dashboard
from ui.expenses_page import ExpensesPage
from ui.notes_page import NotesPage
from ui.chat_page import ChatPage

class NavigationController:
    def __init__(self, main_window, access_token):
        self.main_window = main_window
        self.access_token = access_token

    def show_dashboard(self):
        dashboard = Dashboard()
        dashboard.navigate_signal.connect(self.handle_navigation)
        self.main_window.setCentralWidget(dashboard)

    def handle_navigation(self, target):
        if target == "expenses":
            page = ExpensesPage(token=self.access_token)  # optional: token argument can be removed
            page.navigate_signal.connect(self.handle_navigation)
            self.main_window.setCentralWidget(page)
        elif target == "notes":
            page = NotesPage()
        elif target == "chat":
            page = ChatPage()
        else:
            from ui.dashboard import Dashboard
            page = Dashboard()

        page.navigate_signal.connect(self.handle_navigation)
        self.main_window.setCentralWidget(page)
