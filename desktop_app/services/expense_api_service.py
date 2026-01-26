import requests
from typing import List
from models.expense_model import Expense

# Base URL for backend API
BASE_URL = "http://127.0.0.1:8000"
TOKEN = None 

def set_token(token: str):
    """
    Set the global authentication token for API requests.

    Args:
        token (str): The authentication token used for secure API access.
    """
    global TOKEN
    TOKEN = token
    print(f"[DEBUG] Global TOKEN set: {TOKEN[:20]}...") # For debug purpose 

def get_headers():
    """
    Get the headers for making authenticated API requests.

    Returns:
        dict: A dictionary containing the 'Authorization' header with the Bearer token.

    Raises:
        Exception: If the authentication token has not been set.
    """
    if not TOKEN:
        raise Exception("Authentication token not set. ")
    return {"Authorization": f"Bearer {TOKEN}"}


def get_expenses() -> List[Expense]:
    """
    Fetch all expenses from the backend API.

    Returns:
        List[Expense]: A list of `Expense` objects retrieved from the API.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    response = requests.get(
        f"{BASE_URL}/expenses/", headers=get_headers()
    )
    response.raise_for_status() # Raise exception if request failed
    return [Expense.from_dict(e) for e in response.json()]


def create_expense(expense: Expense) -> Expense:
    """
    Create a new expense entry via the backend API.

    Args:
        expense (Expense): The `Expense` object to be created.

    Returns:
        Expense: The created `Expense` object returned by the API.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    response = requests.post(
        f"{BASE_URL}/expenses/", headers=get_headers(), json=expense.to_dict()
    )
    response.raise_for_status()
    return Expense.from_dict(response.json())


def update_expense(expense_id: int, expense: Expense) -> Expense:
    """
    Update an existing expense entry via the backend API.

    Args:
        expense_id (int): The ID of the expense to be updated.
        expense (Expense): The `Expense` object with updated values.

    Returns:
        Expense: The updated `Expense` object returned by the API.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    response = requests.put(
        f"{BASE_URL}/expenses/{expense_id}", headers=get_headers(), json=expense.to_dict()
    )
    response.raise_for_status()
    return Expense.from_dict(response.json())

def delete_expense(expense_id: int):
    """
    Delete an expense entry via the backend API.

    Args:
        expense_id (int): The ID of the expense to be deleted.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    response = requests.delete(f"{BASE_URL}/expenses/{expense_id}", headers=get_headers())
    response.raise_for_status()
