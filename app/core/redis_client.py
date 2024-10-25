import redis
from app.core.config import config

redis_client = redis.Redis.from_url(config.REDIS_URL)
