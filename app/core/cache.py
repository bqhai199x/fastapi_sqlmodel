import redis
from app.core.config import settings
import uuid

pool = redis.ConnectionPool.from_url(settings.REDIS_URL, max_connections=10, decode_responses=True)
cache = redis.Redis(connection_pool=pool)


def save_token(username: str, token: str, session_id: str, refresh: bool = False) -> str:
    token_id = str(uuid.uuid4())
    token_type = "refresh" if refresh else "access"
    ex_time = settings.REFRESH_TOKEN_EXPIRE_MINUTES if refresh else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    cache.set(f"token:{username}:{token_type}:{session_id}:{token_id}", token, ex=ex_time * 60)
    return token_id


def verify_token(username: str, refresh: bool = False) -> bool:
    token_type = "refresh" if refresh else "access"
    token_key = f"token:{username}:{token_type}:*"
    for key in cache.scan_iter(token_key):
        if cache.exists(key):
            return True
    return False


def remove_user_access_tokens(username: str) -> None:
    token_keys = cache.scan_iter(f"token:{username}:*")
    for key in token_keys:
        cache.delete(key)


def remove_device_tokens(username: str, session_id: str) -> None:
    token_keys = cache.scan_iter(f"token:{username}:*:{session_id}:*")
    for key in token_keys:
        cache.delete(key)