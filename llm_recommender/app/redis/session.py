# app/redis/session.py
import aioredis
from jose import JWTError, jwt
from fastapi import HTTPException, status, Request
from app.core.config import settings

redis = aioredis.from_url(settings.redis_url, decode_responses=True)

SESSION_PREFIX = "session:"

def session_key(username: str) -> str:
    return f"{SESSION_PREFIX}{username}"

async def store_session_token(username: str, token: str, expires_in: int):
    await redis.setex(session_key(username), expires_in, token)

async def verify_session_token(username: str, incoming_token: str):
    stored_token = await redis.get(session_key(username))
    if not stored_token or stored_token != incoming_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session. Please log in again."
        )

async def clear_session(username: str):
    await redis.delete(session_key(username))