from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Expense:
    """
    A class representing a single expense entry with attributes like amount, description, 
    date, and category. This class supports conversion to and from dictionary format for 
    communication with backend services (e.g., API).

    Attributes:
        id (Optional[int]): The unique identifier for the expense. It's optional as it may not be 
                             set before the expense is saved to the database.
        amount (float): The amount of the expense.
        description (str): A description or note about the expense.
        date (datetime): The date and time when the expense was made.
        category (str): The category of the expense (e.g., 'Food', 'Transport').
    """

    id: Optional[int]
    amount: float
    description: str
    date: datetime
    category: str


    @staticmethod
    def from_dict(data: dict) -> "Expense":
        """
        Converts a dictionary (usually from backend JSON) into an Expense object.

        Args:
            data (dict): A dictionary containing the keys 'id', 'amount', 'category', 'description', 
                         and 'date'. The 'id' is optional and the 'description' defaults to an empty string 
                         if not provided.

        Returns:
            Expense: An instance of the Expense class.
        """
        return Expense(
            id=data.get("id"),
                amount=data.get("amount"),
                category=data.get("category"),
                description=data.get("description", ""),
                date=datetime.fromisoformat(data.get("date")),
        )

    def to_dict(self) -> dict:
        """
        Converts an Expense object into a dictionary, typically for sending to the backend.

        Returns:
            dict: A dictionary representation of the Expense object with keys 'amount', 'category', 
                  'description', and 'date' (formatted as an ISO string).
        """
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date.isoformat(),
        }