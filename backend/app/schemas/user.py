from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    This schema is used when validating the data sent by the client for creating a new user.

    Attributes:
        email (str): The email address of the user. Must be unique.
        full_name (Optional[str]): The full name of the user. This is optional.
    """
    email: str
    full_name: Optional[str] = None

class UserRead(BaseModel):
    """
    Schema for reading user data.

    This schema is used when sending a user’s data back to the client after fetching it from the database.
    
    Attributes:
        id (int): The unique identifier for the user.
        email (str): The email address of the user.
        full_name (Optional[str]): The full name of the user. This is optional.
        picture (Optional[str]): A URL or string pointing to the user’s profile picture. This is optional.
        created_at (datetime): The timestamp when the user was created (e.g., account creation time).
    """
    id: int
    email: str
    full_name: Optional[str] = None
    picture: Optional [str] = None
    created_at : datetime

class Config:
    """
        Configuration for Pydantic's behavior with ORM models.
        
        `orm_mode = True` tells Pydantic to treat the model as an ORM model, allowing it to work with 
        databases (like SQLAlchemy models) by automatically converting database rows into Pydantic models.
        """
    orm_mode = True