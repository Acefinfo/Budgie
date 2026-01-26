from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Expense(Base):
    """
    The Expense class represents an expense record in the database.
    It contains details about the expense such as the amount spent,
    the category of the expense, a description, and the date when 
    the expense was created. Each expense is associated with a user 
    through a foreign key relationship.
    """
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="expenses")
