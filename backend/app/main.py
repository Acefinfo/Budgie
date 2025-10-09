from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import auth, expenses, auth_google

app = FastAPI(title="Expense Tracker Api", version="1.0.0")

# Create tables on startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(auth_google.router, prefix="/auth/google", tags=["google_oauth"])
app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
