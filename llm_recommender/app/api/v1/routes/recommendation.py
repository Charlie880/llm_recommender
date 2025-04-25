from fastapi import APIRouter, Body, Depends, HTTPException
from app.schemas.recommend import RecommendRequest, RecommendResponse
from app.services.recommender import generate_recommendations
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.models.user import User
from app.core.redis import redis_client
import hashlib
import json

router = APIRouter(prefix="/recommend", tags=["Recommendations"])

@router.post("/", response_model=RecommendResponse)
async def recommend_products(
    payload: RecommendRequest,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user)
):
    """
    Generate product recommendations based on the user's query. Uses Redis caching for repeat requests.

    Args:
        payload (RecommendRequest): The recommendation request containing the query.
        db (AsyncSession): The database session dependency.
        user (User): The currently authenticated user.

    Returns:
        RecommendResponse: A response containing the list of recommended products.
    """
    # Build Redis cache key (hash the query for safety)
    query_str = payload.query.strip().lower()
    query_hash = hashlib.sha256(query_str.encode()).hexdigest()
    redis_key = f"user:{user.id}:recommend:{query_hash}"

    # Try to fetch from Redis cache
    cached = redis_client.get(redis_key)
    if cached:
        try:
            recommendations = json.loads(cached)
            return {"recommendations": recommendations}
        except json.JSONDecodeError:
            pass  # If something weird happens, just fall back to fresh gen

    # If not in cache, generate recommendations
    recommendations = await generate_recommendations(payload, db)

    # Store in Redis with TTL (5 minutes)
    redis_client.setex(redis_key, 300, json.dumps(recommendations))

    return {"recommendations": recommendations}