from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    note: Optional[str] = None

class ExpenseRead(BaseModel):
    id: int
    user_id: int
    amount: float
    category: str
    note: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
