import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("Database_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256") # Retrieve the ALGORITHM from the environment. If not set, defaults to "HS256" (HMAC-SHA256)

# Retrieve the ACCESS_TOKEN_EXPIRE_MINUTES from the environment, with a default of 30 minutes
# This value controls how long the access token is valid before it expires
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))