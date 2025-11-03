from services import expense_api_service
from ui.dashboard import Dashboard
from ui.expenses_page import ExpensesPage
from ui.notes_page import NotesPage


class NavigationController:
    """
    NavigationController manages the navigation flow between different pages of the application.
    It is responsible for displaying the appropriate page in the main window based on user actions.

    The controller listens for user interactions that trigger page changes, and handles displaying the
    respective UI components accordingly.

    Attributes:
        main_window (QMainWindow): The main window of the application where the pages will be displayed.
        access_token (str): An authentication token used to securely interact with the services.
    """
    def __init__(self, main_window, access_token):
        """
        Initializes the NavigationController with the main window and the access token.

        The main window is where different UI components (pages) are set as the central widget. 
        The access token is used for authentication with services, like fetching user-specific data.

        Args:
            main_window (QMainWindow): The main window instance where different pages will be shown.
            access_token (str): The authentication token to access secure services.
        """
        self.main_window = main_window  # Stores the reference to the main window
        self.access_token = access_token # Stores the access token for secure service access

    def show_dashboard(self):
        """
        Displays the Dashboard page as the central widget in the main window.

        The dashboard serves as the starting point of the application and allows the user to navigate 
        to other sections (such as expenses, notes, and chat) via signals connected to this handler.

        This method also connects the `navigate_signal` emitted from the dashboard to the `handle_navigation` 
        method, which is responsible for determining the next page to show based on the navigation signal.
        """
        dashboard = Dashboard() # Create an instance of the Dashboard page
        dashboard.navigate_signal.connect(self.handle_navigation)   # Connect the dashboard's navigation signal to the handler
        self.main_window.setCentralWidget(dashboard)    # Set the Dashboard as the central widget in the main window

    def handle_navigation(self, target):
        """
        Handles navigation to a new page based on the selected target.

        This method listens for navigation signals emitted from other pages (Dashboard, Expenses, Notes, etc.)
        and displays the appropriate page in the main window based on the `target` argument.

        The `target` can be:
        - "expenses": Displays the ExpensesPage.
        - "notes": Displays the NotesPage.
        - "chat": Displays the ChatPage.
        - Others (default): Displays the Dashboard page.

        Args:
            target (str): The target page to navigate to. This determines which page will be shown next.
        """
        if target == "expenses":
             # Create and display the Expenses page with the token for service access
            page = ExpensesPage(token=self.access_token)  # token argument may be removed if not needed
            page.navigate_signal.connect(self.handle_navigation)  # Connect the page's navigation signal to the handler
            self.main_window.setCentralWidget(page)  # Set ExpensesPage as the central widget

        elif target == "notes":
            # Create and display the Notes page with the token for service access
            page = NotesPage(token=self.access_token)  # token argument may be removed if not needed
            page.navigate_signal.connect(self.handle_navigation)  # Connect the page's navigation signal to the handler
            self.main_window.setCentralWidget(page)  # Set NotesPage as the central widget
        
        
        else:
            # Default to displaying the Dashboard page if the target is unrecognized
            from ui.dashboard import Dashboard  # Ensure Dashboard is available for import
            page = Dashboard()  # Create and display the Dashboard page
            page.navigate_signal.connect(self.handle_navigation)  # Connect the dashboard's navigation signal to the handler
            self.main_window.setCentralWidget(page)  # Set Dashboard as the central widget