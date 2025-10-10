from controllers.expense_controller import (
    handle_add_expense, handle_view_expenses,
    handle_summary, handle_reports, handle_edit_expenses,handle_delete_expenses
)
from views.expense_view import show_menu, show_expense_menu

def main():
    """Main application loop."""
    while True:
        choise = show_menu()

        if choise == "1":
            handle_add_expense()

        elif choise == "2":
            while True:
                show_expense_menu()
                sub_choise = input("Choose (1-4): ")

                if sub_choise == "1":
                    handle_view_expenses()
                elif sub_choise == "2":
                    # expenses = load_expenses()
                    handle_edit_expenses()
                elif sub_choise == "3":
                    # expenses = load_expenses()
                    handle_delete_expenses()    
                elif sub_choise == "4":
                    break
                else:
                    print("❌ Invalid choice. Please try again.")

        elif choise == "3":
            handle_summary()
        
        elif choise == "4":
            handle_reports()
        
        elif choise == "5":
            confirm = input("Are you sure you want to exit? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                print("Goodbye! See you next time. 👋")
                break

        
                

if __name__ == "__main__":
    main()
else:
    print("main.py imported as a module.")