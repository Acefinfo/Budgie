from controllers.expense_controller import (
    handle_add_expense, handle_view_expenses,
    handle_summary, handle_reports
)
from views.expense_view import show_menu


def main():
    """Main application loop."""
    while True:
        choice = show_menu()
        if choice == "1":
            handle_add_expense()
        elif choice == "2":
            handle_view_expenses()
        elif choice == "3":
            handle_summary()
        elif choice == "4":
            handle_reports()
        elif choice == "5":
            confirm = input("Are you sure you want to exit? (y/n): ").strip().lower()
            if confirm == 'y' or confirm == 'yes':
                print("Goodbye! See you next time. 👋")
                break


if __name__ == "__main__":
    main()
else:
    print("main.py imported as a module.")