from fastapi import Request, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_async_session
from app.models.user import User
from app.core.redis import get_token_from_redis
from app.core.config import settings

SECRET_KEY = settings.secret_key.get_secret_value()
ALGORITHM = settings.algorithm

async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
) -> User:
    # 🧠 Try token from header first
    auth_header = request.headers.get("Authorization")
    token = None

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[len("Bearer "):]
    else:
        # 🧁 Fallback to cookie
        token_cookie = request.cookies.get("access_token")
        if token_cookie and token_cookie.startswith("Bearer "):
            token = token_cookie[len("Bearer "):]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed token"
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    redis_token = get_token_from_redis(user.id)
    if redis_token != token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token mismatch or session expired")

    return user