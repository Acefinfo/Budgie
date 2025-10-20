from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import auth, expenses, auth_google

app = FastAPI(title="Budgie Api", version="1.0.0")
"""
The FastAPI instance is created here. It will serve as the main entry point for your API.
The `title` and `version` arguments are used to provide metadata about the API that can be seen 
on the auto-generated documentation page (Swagger UI).
"""

# Create tables on startup
@app.on_event("startup")
def startup_event():
    """
    This event handler is triggered when the FastAPI application starts up.
    It runs once and is used to initialize database tables by creating them based on the ORM models.

    - `Base.metadata.create_all(bind=engine)` will create all tables that are defined in the SQLAlchemy 
      ORM models based on the metadata created from the models. This is typically used in development.
    """
    Base.metadata.create_all(bind=engine)

# ------------------------------
# Include routers for routing API requests
# ------------------------------
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(auth_google.router, prefix="/auth/google", tags=["google_oauth"])
app.include_router(expenses.router, prefix="/expenses")
