from datetime import datetime
from models.expense_model import (
    save_expense, load_expenses, get_summary,
    get_category_summary, get_monthly_summary
)
from views.expense_view import (
    show_expenses, show_summary, show_reports_menu,
    show_category_report, show_monthly_report,
    plot_category_pie, plot_monthly_trend
)


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
        if category:
            break
        print("❌ Category cannot be empty.")

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
