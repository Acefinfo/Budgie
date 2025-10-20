from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.deps import get_db
from app.models.user import User

# OAuth2 scheme (temporary, for dev we use auth/dev-login to get tokens)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/dev-login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token containing the given data and an expiration time.

    Parameters:
        data (dict): The data to include in the payload of the JWT.
        expires_delta (Optional[timedelta]): The expiration time of the token.
            If not provided, it defaults to the configured `ACCESS_TOKEN_EXPIRE_MINUTES`.

    Returns:
        str: The encoded JWT token as a string.
    """

    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Dependency to retrieve the current user from the database by decoding the JWT token.

    This function decodes the JWT token, retrieves the user ID or email (sub),
    and returns the corresponding user object from the database.

    Parameters:
        token (str): The OAuth2 token, passed automatically by FastAPI using the OAuth2PasswordBearer dependency.
        db (Session): The SQLAlchemy session, provided via the dependency injection system.

    Returns:
        User: The user object corresponding to the JWT's subject (ID or email).
    
    Raises:
        HTTPException: If the token is invalid or the user is not found in the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

   
    user = None
    try:
        user_id = int(sub)
        user = db.query(User).filter(User.id == user_id).first()
    except ValueError:
        # If not a number, assume it's an email (Google login case)
        user = db.query(User).filter(User.email == sub).first()

    if not user:
        raise credentials_exception

    return user


    
