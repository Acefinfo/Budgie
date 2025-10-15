from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.expense import Expense as ExpenseModel
from app.schemas import ExpenseCreate, ExpenseRead
from app.core.deps import get_db
from app.core.security import get_current_user

router = APIRouter()

# ------------------------------
# GET /expenses/ - list expenses
# ------------------------------
@router.get("/", response_model=List[ExpenseRead])
def list_expenses(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    List all expenses for the currently logged-in user.
    """
    expenses = db.query(ExpenseModel).filter(ExpenseModel.user_id == current_user.id).all()
    return expenses

# ------------------------------
# POST /expenses/ - create expense
# ------------------------------
@router.post("/", response_model=ExpenseRead)
def create_expense(expense_in: ExpenseCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Create a new expense for the currently logged-in user.
    """
    expense = ExpenseModel(
        user_id=current_user.id,
        amount=expense_in.amount,
        category=expense_in.category,
        description=expense_in.description,
        date=expense_in.date  # can be None → defaults to server timestamp
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

# ------------------------------
# PUT /expenses/{expense_id} - update expense
# ------------------------------
@router.put("/{expense_id}", response_model=ExpenseRead)
def update_expense(expense_id: int, expense_in: ExpenseCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Update an existing expense. Only allowed if expense belongs to current user.
    """
    expense = db.query(ExpenseModel).filter(
        ExpenseModel.id == expense_id,
        ExpenseModel.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.amount = expense_in.amount
    expense.category = expense_in.category
    expense.description = expense_in.description
    if expense_in.date:
        expense.date = expense_in.date

    db.commit()
    db.refresh(expense)
    return expense

# ------------------------------
# DELETE /expenses/{expense_id} - delete expense
# ------------------------------
@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Delete an expense. Only allowed if expense belongs to current user.
    """
    expense = db.query(ExpenseModel).filter(
        ExpenseModel.id == expense_id,
        ExpenseModel.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return
