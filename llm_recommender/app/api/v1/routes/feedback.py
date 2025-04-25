from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.models.feedback import Feedback
from app.core.dependencies import get_current_user
from app.models.user import User
from app.db.session import get_async_session

router = APIRouter()

@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    new_feedback = Feedback(
        user_id=user.id,
        product_id=feedback_data.product_id,
        feedback=feedback_data.feedback,
    )
    session.add(new_feedback)
    await session.commit()
    await session.refresh(new_feedback)

    return new_feedback
