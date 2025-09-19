import csv
import os

# Directory for storing data
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FILE_PATH = os.path.join(DATA_DIR, "expenses.csv")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


def save_expense(expense):
    """
    Save a single expense record to CSV.
    - expense: [date, amount, category]
    CSV header: date,amount,category
    """
    file_exists = os.path.isfile(FILE_PATH)

    with open(FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["date", "amount", "category"])  # correct header
        writer.writerow(expense)


def load_expenses():
    """
    Load all expenses from CSV.
    Returns list of dicts: {"date": ..., "amount": ..., "category": ...}
    Skips invalid rows automatically.
    """
    expenses = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    expenses.append({
                        "date": row["date"],
                        "amount": float(row["amount"]),
                        "category": row["category"].title()
                    })
                except (ValueError, KeyError):
                    print(f"Skipping invalid row in CSV: {row}")
    return expenses


def overwrite_expenses(expenses):
    """Overwrite the entire CSV with the provided list of expenses."""
    with open(FILE_PATH, mode="w",newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "amount", "category"])
        writer.writeheader()
        for exp in expenses:
            writer.writerow(exp)
# This ensures after esiring or deliting the CSV gets updated 


def get_summary(expenses):
    """Return total, min, max of all expenses."""
    if not expenses:
        return 0, 0, 0
    amounts = [exp["amount"] for exp in expenses]
    return sum(amounts), min(amounts), max(amounts)


def get_category_summary(expenses):
    """Return total expenses grouped by category."""
    summary = {}
    for exp in expenses:
        summary[exp["category"]] = summary.get(exp["category"], 0) + exp["amount"]
    return summary


def get_monthly_summary(expenses):
    """Return total expenses grouped by month (YYYY-MM)."""
    summary = {}
    for exp in expenses:
        month = exp["date"][:7]
        summary[month] = summary.get(month, 0) + exp["amount"]
    return summary
