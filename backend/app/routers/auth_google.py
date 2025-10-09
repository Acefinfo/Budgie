from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from starlette.requests import Request
import requests, os, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User

router = APIRouter()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Redirect to Google login page
@router.get("/login")
def login_google():
    google_auth_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    auth_url = f"{google_auth_endpoint}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}&access_type=offline&prompt=consent"
    return RedirectResponse(auth_url)

# Callback endpoint
@router.get("/callback")
def callback_google(request: Request, db: Session = Depends(get_db)):
    code= request.query_params.get("code")
    if not code:
        raise HTTPException(status_code= 400, detail= "No code returned from Google")
    
    #Exchange code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    data={
        "code" : code,
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET,
        "redirect_uri" : REDIRECT_URI,
        "grant_type" : "authorization_code"
    }

    token_resp = requests.post(token_url, data= data).json()
    
    id_token = token_resp.get("id_token")
    if not id_token:
        raise HTTPException(status_code = 400, detail = "Failded to get id_token from Google")
    
    # Decode user info
    payload = jwt.decode(id_token, options={"verify_signature": False})
    email = payload.get("email")
    name = payload.get("name")

    # Check DB for user, create if not exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, full_name=name)
        db.add(user)
        db.commit()
        db.refresh(user)

    # Issue Jwt token forr our API
    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_data = {"sub": user.email, "exp": datetime.utcnow() + access_token_expires}
    jwt_token = jwt.encode(jwt_data, SECRET_KEY, algorithm=ALGORITHM)

    return{"access_token": jwt_token, "token_type": "bearer", "user": {"email": user.email, "name": name}}




