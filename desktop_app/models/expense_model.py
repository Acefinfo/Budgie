from dataclasses import dataclass
from typing import Optional
from datetime import datetime


# Dataclass representing a single expense entry
@dataclass
class Expense:
    id: Optional[int]
    amount: float
    description: str
    date: datetime
    category: str


    # Convert dictionary (from backend JSON) to Expense object
    @staticmethod
    def from_dict(data: dict) -> "Expense":
        return Expense(
            id=data.get("id"),
                amount=data.get("amount"),
                category=data.get("category"),
                description=data.get("description", ""),
                date=datetime.fromisoformat(data.get("date")),
        )

    # Convert Expense object to dictionary (for sending to backend)
    def to_dict(self) -> dict:
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date.isoformat(),
        }