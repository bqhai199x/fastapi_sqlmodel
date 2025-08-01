import redis
from app.core.config import settings

pool = redis.ConnectionPool.from_url(settings.REDIS_URL, max_connections=10, decode_responses=True)
cache = redis.Redis(connection_pool=pool)
