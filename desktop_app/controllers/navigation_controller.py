from ui.dashboard import Dashboard
from ui.expenses_page import ExpensesPage
from ui.notes_page import NotesPage
from ui.chat_page import ChatPage

class NavigationController:
    def __init__(self, main_window,access_token):
        self.main_window = main_window
        self.access_token = access_token

        # Connect the log in suscess signal
        self.main_window.login_window.login_success.connect(self.on_login_success)

    def on_login_success(self, token):
        self.access_token = token
        print(f"[DEBUG] Token received: {self.access_token}")
        self.show_dashboard()



    def show_dashboard(self):
        dashboard = Dashboard()
        dashboard.navigate_signal.connect(self.handle_navigation)
        self.main_window.setCentralWidget(dashboard)

    def handle_navigation(self, target):
        if target == "expenses":
            page = ExpensesPage(token=self.access_token)
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
