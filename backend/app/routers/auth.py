from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import create_access_token

router = APIRouter()

@router.post("/dev-login")
def dev_login(payload: UserCreate, db:Session = Depends(get_db)):
    """
    Development login route for creating or authenticating a user.

    This endpoint simulates a login process by creating a new user if one doesn't exist 
    or returning the existing user if the email already exists in the database. After 
    authenticating or creating the user, a JWT access token is generated for the user.

    Args:
        payload (UserCreate): A Pydantic model containing the email and full_name for the user.
        db (Session): The SQLAlchemy session used to interact with the database.

    Returns:
        dict: A dictionary containing the generated access token, token type, and the user's details (id and email).
    """
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        user = User(email = payload.email,full_name = payload.full_name)
        db.add(user)
        db.commit()
        db.refresh(user)
    token = create_access_token({"sub":str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email}}

