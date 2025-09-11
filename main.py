from datetime import datetime


def add_expense(expense):
    try:
        date = datetime.now().strftime("%Y-%m-%d")

        amount = float(input("Enter expense amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        
        category = input("Enter expense category: ")
        expense.append({
            'date': date, 
            'amount': amount, 
            'category': category
        })
        print("Expense added successfully.")    
    except ValueError:
        print("Invalid input. Please enter a valid number for amount.")


def view_expenses(expense):
    if not expense:
        print("No expenses recorded.")
        return
    print("\n--- Recorded Expenses ---")
    for idx, exp in enumerate(expense, start=1):
        print(f"{idx}. Date:{exp['date']}, Category:{exp['category']}, Amount: ${exp['amount']:.2f}")


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

    # Category breaksown
    category_summary = {}
    for exp in expense:
        category_summary[exp['category']] = category_summary.get(exp['category'], 0) + exp['amount']
    print("\n--- Expense Summary by Category ---")
    for category, amount in category_summary.items():
        print(f"{category}: ${amount:.2f}")




def main():
    expense = []


    while True:
        print("\n--- Expense Tracker Menu ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show summary")
        print("4. Exit")

        chouse = input("Choose an option (1-4): ")

        if chouse == '1':
            add_expense(expense)        
        elif chouse == '2':
            view_expenses(expense)          
        elif chouse == '3':
            show_summary(expense)       
        elif chouse == '4':
            print("Exiting the program. Goodbye!")
            break   
        else:
            print("Invalid choice. Please try again.")  

if __name__ == "__main__":
    main()