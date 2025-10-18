import requests
from typing import List
from models.expense_model import Expense

# Base URL for backend API
BASE_URL = "http://127.0.0.1:8000"
TOKEN = None 

# Set token once user logs in
def set_token(token: str):
    global TOKEN
    TOKEN = token

def get_headers():
    if not TOKEN:
        raise Exception("Authentication token not set. ")
    return {"Authorization": f"Bearer {TOKEN}"}


def get_expenses() -> List[Expense]:
    response = requests.get(
        f"{BASE_URL}/expenses/", headers=get_headers()
    )
    response.raise_for_status() # Raise exception if request failed
    return [Expense.from_dict(e) for e in response.json()]

#Create a new expense entry
def create_expense(expense: Expense) -> Expense:
    response = requests.post(
        f"{BASE_URL}/expenses/", headers=get_headers(), json=expense.to_dict()
    )
    response.raise_for_status()
    return Expense.from_dict(response.json())

# Update an existing expense entry
def update_expense(expense_id: int, expense: Expense) -> Expense:
    response = requests.put(
        f"{BASE_URL}/expenses/{expense_id}", headers=get_headers(), json=expense.to_dict()
    )
    response.raise_for_status()
    return Expense.from_dict(response.json())

# Delete an expense
def delete_expense(expense_id: int):
    response = requests.delete(f"{BASE_URL}/expenses/{expense_id}", headers=get_headers())
    response.raise_for_status()
