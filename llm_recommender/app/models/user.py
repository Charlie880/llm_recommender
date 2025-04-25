from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

# User model (formerly clients)
class User(Base):
    __tablename__ = "clients"  # Renamed table from 'users' to 'clients'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    feedbacks = relationship("Feedback", back_populates="client")  # Relationship with Feedback, no cascade delete
