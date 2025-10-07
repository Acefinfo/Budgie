from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import create_access_token

router = APIRouter()

@router.post("/dev-login")
def dev_login(payload: UserCreate, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        user = User(email = payload.email,full_name = payload.full_name)
        db.add(user)
        db.commit()
        db.refresh(user)
    token = create_access_token({"sub":str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email}}

