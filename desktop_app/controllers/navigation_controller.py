from services import expense_api_service
from ui.dashboard import Dashboard
from ui.expenses_page import ExpensesPage
from ui.notes_page import NotesPage
from ui.chat_page import ChatPage

class NavigationController:
    """
    NavigationController manages the navigation flow between different pages of the application.
    It is responsible for displaying the appropriate page based on user interaction.
    
    Attributes:
        main_window (QMainWindow): The main window of the application where the pages are displayed.
        access_token (str): An authentication token used for secure access to the services.
    """
    def __init__(self, main_window, access_token):
        """
        Initializes the NavigationController with the main window and the access token.

        Args:
            main_window (QMainWindow): The main window of the application.
            access_token (str): The authentication token used to interact with services.
        """
        self.main_window = main_window
        self.access_token = access_token

    def show_dashboard(self):
        """
        Displays the dashboard page as the central widget in the main window.
        It also connects the navigation signal to the handler method for further navigation.
        """
        dashboard = Dashboard()
        dashboard.navigate_signal.connect(self.handle_navigation)
        self.main_window.setCentralWidget(dashboard)

    def handle_navigation(self, target):
        """
        Handles the navigation based on the selected target. This method determines 
        which page should be shown next.

        Args:
            target (str): The target page to navigate to. 
                          Can be one of the following values: "expenses", "notes", "chat", or others (defaults to dashboard).
        """
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
