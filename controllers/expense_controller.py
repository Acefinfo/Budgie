from datetime import datetime
from models.expense_model import (
    save_expense, load_expenses, get_summary,
    get_category_summary, get_monthly_summary,overwrite_expenses
)
from views.expense_view import (
    show_expenses, show_summary, show_reports_menu,
    show_category_report, show_monthly_report,
    plot_category_pie, plot_monthly_trend,show_expense_menu)


def handle_add_expense():
    """Handle user input for adding a new expense."""
    while True:
        try:
            amount = float(input("Enter expense amount: "))
            if amount <= 0:
                print("❌ Amount cannot be negative or zero.")
                continue
            break
        except ValueError:
            print("❌ Invalid amount. Please enter a number.")
        
    while True:
        category = input("Enter expense category: ").strip().title()
        if len(category)<1:
            print("❌ Category cannot be empty.")
        elif len(category)>20:
            print("❌ Category too long (max 20 characters).")
        else:
            break

    date = datetime.now().strftime("%Y-%m-%d")
    save_expense([date, amount, category])
    print("✅ Expense added successfully.")
        

def handle_view_expenses():
    """Load and display all expenses."""
    expenses = load_expenses()
    show_expenses(expenses)


def handle_summary():
    """Load expenses and display summary stats."""
    expenses = load_expenses()
    total, lowest, highest = get_summary(expenses)
    show_summary(total, lowest, highest)


def handle_reports():
    """Handle reports menu and plotting."""
    expenses = load_expenses()

    while True:
        choice = show_reports_menu()
        if choice == "1":
            show_category_report(get_category_summary(expenses))
        elif choice == "2":
            show_monthly_report(get_monthly_summary(expenses))
        elif choice == "3":
            plot_category_pie(get_category_summary(expenses))
        elif choice == "4":
            plot_monthly_trend(get_monthly_summary(expenses))
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def handle_edit_expenses(expenses):
    if not expenses:
        print("No expenses to edit.")
        return
    
    show_expense_menu()
    try:
        index = int(input("Enter the number of expense you want to edit:"))-1
        if index < 0 or index >= len(expenses):
            print("Invalid index.")
            return
        expense = expenses[index]
        print(f"Editinf:{expense}")

        new_amount = input(f"Enter new amount (leave balan to keep same anount as before:").strip()
        new_category = input(f"Enter new category (leave blank to keep same category as before:").strip().title()

        if new_amount:
            try:
                new_amount = float(new_amount)
                if new_amount <= 0:
                    print("Amount must be positive.")
                    return
                expense["amount"] = new_amount
            except ValueError:
                print("Invalid amount entered.")
                return
        if new_category:
            expense["category"] = new_category
        
        overwrite_expenses(expenses)
        print("Expense updated successfully.")
    
    except ValueError:
        print("Invalid input. Please enter a number.")

def handle_delete_expenses(expenses):
    if not expenses:
        print("No expenses to delete.")
        return
    
    show_expense_menu()
    try:
        index = int(input("Enter the number of expense you want to delete:"))-1
        if index < 0 or index >= len(expenses):
            print("Invalid index.")
            return
        confirm = input(f"Are you sure you want to delete {expenses[index]}? (y/n):").strip().lower()
        if confirm  == "y" or "yes":
            expenses.pop(index)
            overwrite_expenses(expenses)
            print("Expense deleted successfully.")
        else:
            print("Deletion cancelled.")
    except ValueError:
        print("Invalid input. Please enter a number.")