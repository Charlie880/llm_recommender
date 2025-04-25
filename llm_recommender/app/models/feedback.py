from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Feedback(Base):
    __tablename__ = "feedback"  # Feedback table

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("clients.id"), nullable=False)  # ForeignKey reference to clients
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)  # ForeignKey reference to products
    feedback = Column(Text, nullable=False)  # Add this column for feedback text
    timestamp = Column(DateTime, default=datetime.utcnow)  # Timestamp default to current UTC time

    client = relationship("User", back_populates="feedbacks")  # Relationship with User (clients)
    product = relationship("Product", back_populates="feedbacks")  # Relationship with Product