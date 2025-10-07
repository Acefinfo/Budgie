from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    full_name: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    picture: Optional [str] = None
    created_at : datetime

class Config:
    orm_mode = True