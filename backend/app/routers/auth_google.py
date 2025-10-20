from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from starlette.requests import Request
import requests, os, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User

# Create an instance of the FastAPI APIRouter
router = APIRouter()

# Load environment variables
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Redirect to Google login page# Redirect to Google login page
@router.get("/login")
def login_google():
    """
    Redirects the user to the Google OAuth2 login page.

    This endpoint constructs a URL that redirects the user to Google's OAuth2 authentication page
    where the user will be prompted to log in and grant necessary permissions (email and profile).

    Returns:
        RedirectResponse: A redirection to Google's OAuth2 login page.
    """

    google_auth_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    auth_url = f"{google_auth_endpoint}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}&access_type=offline&prompt=consent"
    return RedirectResponse(auth_url)

# Endpoint to handle the callback from Google after user authorization
@router.get("/callback")
def callback_google(request: Request, db: Session = Depends(get_db)):
    """
    Handles the callback from Google after user authentication and authorization.

    Once the user logs in and grants consent, Google redirects to this endpoint with an authorization
    code. This code is then exchanged for tokens, the user's information is extracted, and a JWT token
    is issued for API access.

    Args:
        request (Request): The incoming request, containing query parameters from the redirect.
        db (Session): The SQLAlchemy database session used to interact with the database.

    Returns:
        RedirectResponse: A redirection to the desktop app with the generated JWT token as a query parameter.
    
    Raises:
        HTTPException: If no authorization code is found or if there is an issue obtaining the id_token from Google.
    """
    code = request.query_params.get("code") # Extract the authorization code from the query parameters
    if not code:
        raise HTTPException(status_code=400, detail="No code returned from Google")

    # Exchange the authorization code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    # Make a POST request to the Google token endpoint to exchange the authorization code for tokens
    token_resp = requests.post(token_url, data=data).json()
    id_token = token_resp.get("id_token")

    if not id_token:
        raise HTTPException(status_code=400, detail="Failed to get id_token from Google")

    # Decode the JWT id_token to extract the user’s information
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

    # Issue JWT token for our API
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_data = {"sub": user.email, "exp": datetime.utcnow() + access_token_expires}
    jwt_token = jwt.encode(jwt_data, SECRET_KEY, algorithm=ALGORITHM)

    # Redirect the user to the desktop app listener (port 5000) with the JWT token
    redirect_url = f"http://127.0.0.1:5000/callback?access_token={jwt_token}"
    return RedirectResponse(redirect_url)
