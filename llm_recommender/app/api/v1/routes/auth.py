from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Import select function
from app.models.user import User
from app.core.config import settings
from app.core.redis import set_token_in_redis  # Import the Redis function
from passlib.context import CryptContext  # Import CryptContext for password hashing

router = APIRouter()

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

# Configuration
SECRET_KEY = settings.secret_key.get_secret_value()
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


class AuthInput(BaseModel):
    username: str
    password: str


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
async def login_user(
    data: AuthInput,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
):
    # Check if user exists
    result = await session.execute(select(User).where(User.username == data.username))
    user = result.scalars().first()

    # Existing user - verify password
    if user:
        if not pwd_context.verify(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
            )
    # New user - create account
    else:
        hashed_password = pwd_context.hash(data.password)
        user = User(username=data.username, hashed_password=hashed_password)
        session.add(user)
        await session.commit()
        await session.refresh(user)

    # Generate token
    token_data = {"sub": user.username}
    access_token = create_access_token(
        data=token_data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Save token to Redis with TTL and user_id
    set_token_in_redis(access_token, user.id, ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    # Save token to cookie (session) with secure flag
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="Lax",
        secure=True,  # Set True in production with HTTPS
    )

    return {
        "message": "Authentication successful",
        "username": user.username,
        "access_token": access_token,
    }
