from pydantic import BaseModel
from datetime import datetime

class FeedbackCreate(BaseModel):
    product_id: int
    feedback: str

class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    feedback: str
    timestamp: datetime

    class Config:
        orm_mode = True
