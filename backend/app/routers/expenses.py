from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db
from app.core.security import get_current_user
from app.schemas.expense import ExpenseCreate, ExpenseRead
from app.models.expense import Expense

router = APIRouter()

@router.post("/", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(expense_in: ExpenseCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    expense = Expense(user_id=current_user.id, **expense_in.dict())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

@router.get("/", response_model=List[ExpenseRead])
def list_expenses(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Expense).filter(Expense.user_id == current_user.id).order_by(Expense.created_at.desc()).all()