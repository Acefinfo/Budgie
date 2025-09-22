from db.database import Base, engine
from models.expense_db_model import Expense

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")
