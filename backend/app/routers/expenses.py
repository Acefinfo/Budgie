from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.expense import Expense as ExpenseModel
from app.schemas import ExpenseCreate, ExpenseRead
from app.core.deps import get_db
from app.core.security import get_current_user

# Create an instance of the FastAPI APIRouter
router = APIRouter()

# ------------------------------
# GET /expenses/ - list expenses
# ------------------------------
@router.get("/", response_model=List[ExpenseRead])
def list_expenses(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Retrieve a list of all expenses for the currently logged-in user.

    This endpoint fetches all expenses associated with the current user's ID.
    
    Args:
        db (Session): The database session, injected by FastAPI's `Depends` mechanism.
        current_user (User): The currently authenticated user, fetched using the `get_current_user` dependency.

    Returns:
        List[ExpenseRead]: A list of `ExpenseRead` schemas representing the user's expenses.
    
    Raises:
        HTTPException: If the current user is not authenticated, the exception will be triggered.
    """
    expenses = db.query(ExpenseModel).filter(ExpenseModel.user_id == current_user.id).all()
    return expenses

# ------------------------------
# POST /expenses/ - create expense
# ------------------------------
@router.post("/", response_model=ExpenseRead)
def create_expense(expense_in: ExpenseCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Create a new expense entry for the currently logged-in user.

    This endpoint allows a user to create a new expense record. The user must be authenticated, and 
    the expense will be associated with their ID.

    Args:
        expense_in (ExpenseCreate): The expense data that the user submits, validated via the `ExpenseCreate` schema.
        db (Session): The database session, injected via `Depends`.
        current_user (User): The currently logged-in user, fetched from the `get_current_user` dependency.

    Returns:
        ExpenseRead: A representation of the created expense (including details like amount, category, description, and date).
    
    Raises:
        HTTPException: If the current user is not authenticated, an exception will be raised.
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
    Update an existing expense record. Only allowed if the expense belongs to the current authenticated user.

    This endpoint allows a user to update the details of an existing expense. The update will only be applied
    if the expense belongs to the logged-in user. 

    Args:
        expense_id (int): The ID of the expense to be updated.
        expense_in (ExpenseCreate): The new expense data to be updated, validated using the `ExpenseCreate` schema.
        db (Session): The database session, injected by FastAPI.
        current_user (User): The currently authenticated user, provided by the `get_current_user` dependency.

    Returns:
        ExpenseRead: The updated expense data after modification.
    
    Raises:
        HTTPException: If the expense is not found, or if it does not belong to the current user, a 404 error is raised.
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
    Delete an existing expense record. Only allowed if the expense belongs to the current authenticated user.

    This endpoint allows a user to delete an expense, but only if it belongs to them. If the expense is not found,
    or it doesn’t belong to the logged-in user, a 404 error will be raised.

    Args:
        expense_id (int): The ID of the expense to be deleted.
        db (Session): The database session, injected via `Depends`.
        current_user (User): The currently logged-in user, injected using the `get_current_user` dependency.

    Returns:
        None: This endpoint does not return any content, only a `204 No Content` status code upon successful deletion.
    
    Raises:
        HTTPException: If the expense is not found or does not belong to the current user, a 404 error is raised.
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
