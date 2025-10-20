from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ------------------------------
# Base class for expense schemas
# ------------------------------
class ExpenseBase(BaseModel):
    """
    Base model for Expense, shared between create and read schemas.

    This base class includes common fields for both creating and reading expense data.
    
    Attributes:
        amount (float): The amount of the expense (must be a positive number).
        category (str): The category of the expense (e.g., "food", "transportation").
        description (Optional[str]): A brief description of the expense (optional).
        date (Optional[datetime]): The date when the expense occurred (optional). If not provided, defaults to the server’s current timestamp.
    """
    amount: float
    category: str
    description: Optional[str] = None
    date: Optional[datetime] = None  # frontend 'date'
class ExpenseCreate(ExpenseBase):
    """
    Schema for creating a new expense.

    This schema inherits from `ExpenseBase` and is used for validating the data 
    that is sent when creating a new expense record via an API request.

    No additional fields are required, and it utilizes the base fields for validation.
    """
    pass

class ExpenseRead(ExpenseBase):
    """
    Schema for reading an expense.

    This schema is used when retrieving an expense record from the database to send to the client.
    In addition to the fields from `ExpenseBase`, it also includes the `id` field (the unique identifier 
    for the expense) and ensures that the `date` field is required (i.e., it will not be `None`).
    
    Attributes:
        id (int): The unique identifier of the expense.
        date (datetime): The exact date and time when the expense occurred (cannot be `None`).
    """
    id: int
    date: datetime

    class Config:
        """
        Configuration for the schema's behavior.

        `orm_mode` is set to `True` to allow the schema to work seamlessly with ORM models (e.g., SQLAlchemy).
        This enables the model to convert database records into Pydantic models.
        """
        orm_mode = True
