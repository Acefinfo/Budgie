from datetime import datetime
import csv
import os
import matplotlib.pyplot as plt

# Use a raw string to avoid unicode escape error
FILE_PATH = os.path.join(os.path.dirname(__file__), "expenses.csv")

# Save expenses to CSV file
def save_expense(expense):
    with open(FILE_PATH, mode="w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'amount', 'category'])
        writer.writeheader()  # Fixed typo here
        for exp in expense:
            writer.writerow(exp)

# Load expenses from CSV file
def load_expenses():
    expenses = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    expenses.append({
                        "date": row["date"],
                        "amount": float(row["amount"]),
                        "category": row["category"]
                    })
                except (ValueError, KeyError):
                    print(f"Skipping invalid row: {row}")
    return expenses



# Load existing expenses at the start
expenses = load_expenses()


def category_report(expense):
    if not expense:
        print("No expenses recorded.")
        return
    category_summary = {}
    for exp in expense:
        category_summary[exp['category']] = category_summary.get(exp['category'], 0) + exp['amount']
    print("\n--- Expense Summary by Category ---")
    for category, amount in category_summary.items():
        print(f"{category}: ${amount:.2f}")

def monthly_report(expense):
    if not expense:
        print("No expenses recorded.")
        return
    monthly_summary = {}
    for exp in expense:
        month = exp['date'][:7]  # Extract YYYY-MM
        monthly_summary[month] = monthly_summary.get(month, 0) + exp['amount']
    print("\n--- Monthly Expense Summary ---")
    for month, amount in sorted(monthly_summary.items()):
        print(f"{month}: ${amount:.2f}")
 
 # Category-wise pie chart
def category_pie_chart(expense):
    if not expense:
        print("No expenses recorded.")
        return
    category_summary = {}
    for exp in expense:
        category_summary[exp['category']] = category_summary.get(exp['category'], 0) + exp['amount']
    
    categories = list(category_summary.keys())
    amounts = list(category_summary.values())

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Category')
    plt.show()


# Monthly trend line chart
def monthly_trend_chart(expense):
    if not expense:
        print("No expenses recorded.")
        return
    monthly_summary = {}
    for exp in expense:
        month = exp['date'][:7]  # Extract YYYY-MM
        monthly_summary[month] = monthly_summary.get(month, 0) + exp['amount']
    
    months = sorted(monthly_summary.keys())
    amounts = [monthly_summary[month] for month in months]

    plt.figure(figsize=(10, 5))
    plt.plot(months, amounts, marker='o')
    plt.title('Monthly Expense Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Expense ($)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Add a new expense
def add_expense(expense):
    try:
        date = datetime.now().strftime("%Y-%m-%d")

        amount = float(input("Enter expense amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        
        category = input("Enter expense category: ").strip().title()
        
    
        expense.append({
            'date': date, 
            'amount': amount, 
            'category': category
        })
        print("Expense added successfully.")    
    except ValueError:
        print("Invalid input. Please enter a valid number for amount.")

# View all recorded expenses
def view_expenses(expense):
    if not expense:
        print("No expenses recorded.")
        return
    print("\n--- Recorded Expenses ---")
    for idx, exp in enumerate(expense, start=1):
        print(f"{idx}. Date: {exp['date']}, Category: {exp['category']}, Amount: ${exp['amount']:.2f}")

# Show summary: total, min, max, by category
def show_summary(expense):
    if not expense:
        print("No expenses recorded.")
        return
    
    total = sum(exp['amount'] for exp in expense)
    min_expense = min(exp['amount'] for exp in expense)
    max_expense = max(exp['amount'] for exp in expense)

    print(f"\nTotal Expenses: ${total:.2f}")
    print(f"Lowest Expense: ${min_expense:.2f}")
    print(f"Highest Expense: ${max_expense:.2f}")

    # Category breakdown
    category_summary = {}
    for exp in expense:
        category_summary[exp['category']] = category_summary.get(exp['category'], 0) + exp['amount']
    
    print("\n--- Expense Summary by Category ---")
    for category, amount in category_summary.items():
        print(f"{category}: ${amount:.2f}")

# View reports: monthly and category-wise
def view_reports(expense):
    while True:
        print("\n--- Reports Menu ---")
        print("1. Category Report")
        print("2. Monthly Report")
        print("3. Category Pie Chart")
        print("4. Monthly Trend Chart")
        print("5. Back to Main Menu")

        choice = input("Choose an option (1-5): ")
        if choice == "1":
            category_report(expense)
        elif choice == "2":
            monthly_report(expense)
        elif choice == "3":
            category_pie_chart(expense)
        elif choice == "4":
            monthly_trend_chart(expense)
        elif choice == "5":
            break

        # elif choice == "3":
        #     break   
        # else:
        #     print("Invalid choice. Please try again.")  

        

# Main loop
def main():
    global expenses  # Use the global loaded ex penses list

    while True:
        print("\n--- Expense Tracker Menu ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Summary")
        print("4. Reports")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == '1':
            add_expense(expenses)  
            save_expense(expenses)      
        elif choice == '2':
            view_expenses(expenses)          
        elif choice == '3':
            show_summary(expenses)
        elif choice == '4':
            view_reports(expenses)       
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break   
        else:
            print("Invalid choice. Please try again.")  

if __name__ == "__main__":
    main()
