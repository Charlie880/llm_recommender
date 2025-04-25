import redis
from app.core.config import settings

# Create a Redis client (adjust this based on your Redis setup)
redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True,
)


def set_token_in_redis(token: str, user_id: int, expiration: int):
    try:
        # Store the token in Redis with a TTL (Time To Live)
        redis_client.setex(f"user_token:{user_id}", expiration, token)
    except redis.RedisError as e:
        print(f"Error setting token in Redis: {e}")


def get_token_from_redis(user_id: int):
    try:
        token = redis_client.get(f"user_token:{user_id}")
        if token is None:
            return None  # Token expired or missing
        return token
    except redis.RedisError as e:
        print(f"Error retrieving token from Redis: {e}")
        return None


def delete_token_from_redis(user_id: int):
    try:
        # Delete the token from Redis (on logout or session expiration)
        redis_client.delete(f"user_token:{user_id}")
    except redis.RedisError as e:
        print(f"Error deleting token from Redis: {e}")


def verify_token_in_redis(token: str, user_id: int) -> bool:
    # Retrieve the token from Redis
    redis_token = get_token_from_redis(user_id)
    if redis_token is None or redis_token != token:
        return False  # Token is invalid or expired
    return True
