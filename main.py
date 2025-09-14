from datetime import datetime
import csv
import os

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

# View reports: monthly and yearly
def view_reports(expense):
    while True:
        print("\n--- Reports Menu ---")
        print("1. Full summary")
        print("2. Category Report")
        print("3. Monthly Report")
        print("4. Back to Main Menu")

        choice = input("Choose an option (1-4): ")
        if choice == "1":
            show_summary(expense)
        elif choice == "2":
            catefory_report(expense)
        elif choice == "3":
            monthly_report(expense)
        elif choice == "4":
            break   
        else:
            print("Invalid choice. Please try again.")  

        

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

        choice = input("Choose an option (1-4): ")

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
