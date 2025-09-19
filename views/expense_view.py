import matplotlib.pyplot as plt


def show_menu():
    """Display main menu and return user's choice."""
    print("\n--- Expense Tracker Menu ---")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Show Summary")
    print("4. Reports")
    print("5. Exit")
    choise = input("Choose (1-5): ")

    if choise in ["1", "2", "3", "4", "5"]:
        return choise
    print("Invalid choice. Please try again.")   

def show_expenses(expenses):
    """Display all recorded expenses."""
    print("\n--- Recorded Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
    else:
        for i, exp in enumerate(expenses, 1):
            print(f"{i}. Date: {exp['date']}, Category: {exp['category']}, Amount: ${exp['amount']:.2f}")

def show_expense_menu():
    print("\n--- Expenses Menu ---")
    print("1. View all expenses")
    print("2. Edit an expense")
    print("3. Delete an expense")
    print("4. Back to Main Menu")

def show_summary(total, lowest, highest):
    """Display summary of all expenses."""
    print(f"\nTotal Expenses: ${total:.2f}")
    print(f"Lowest Expense: ${lowest:.2f}")
    print(f"Highest Expense: ${highest:.2f}")


def show_reports_menu():
    """Display reports menu and return user's choice."""
    print("\n--- Reports Menu ---")
    print("1. Category Report")
    print("2. Monthly Report")
    print("3. Category Pie Chart")
    print("4. Monthly Trend Chart")
    print("5. Back to Main Menu")
    return input("Choose (1-5): ")


def show_category_report(summary):
    """Display expenses grouped by category."""
    print("\n--- Expense Summary by Category ---")
    for cat, amt in summary.items():
        print(f"{cat}: ${amt:.2f}")


def show_monthly_report(summary):
    """Display expenses grouped by month."""
    print("\n--- Monthly Expense Summary ---")
    for month, amt in summary.items():
        print(f"{month}: ${amt:.2f}")


def plot_category_pie(summary):
    """Plot a category-wise pie chart (popup only)."""
    if not summary:
        print("No data to plot.")
        return

    labels = list(summary.keys())
    sizes = list(summary.values())

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Expenses by Category")
    plt.show()


def plot_monthly_trend(summary):
    """Plot a monthly expense trend chart (popup only)."""
    if not summary:
        print("No data to plot.")
        return

    months = list(summary.keys())
    amounts = list(summary.values())

    plt.figure(figsize=(8, 5))
    plt.plot(months, amounts, marker="o")
    plt.title("Monthly Expense Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount ($)")
    plt.grid(True)
    plt.show()
