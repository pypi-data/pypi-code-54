from redis.client import Redis

from sample_data_generator.dao.redis.key_schema import KeySchema


class RedisDaoBase:
    """Shared functionality for Redis DAO classes."""
    def __init__(self,
                 redis_client: Redis,
                 key_schema: KeySchema = None) -> None:
        self.redis: Redis = redis_client
        if key_schema is None:
            key_schema = KeySchema()
        self.key_schema = key_schema
