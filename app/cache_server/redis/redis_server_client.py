import logging

from fastapi import Depends

from app.cache_server.server_client import CacheServerClient
from app.cache_server.connector import Connector
from app.cache_server.redis.redis_connector import RedisConnector

logger = logging.getLogger(__name__)


class RedisServerClient(CacheServerClient):
    def __init__(self, connector: Connector = Depends(RedisConnector)) -> None:
        super().__init__()
        self._connector = connector

    async def set_key_value_with_expiry_time(self,
                                             key: str,
                                             value: int = 1,
                                             expires_in_second: int = 60) -> None:
        async with self._connector as redis:
            logger.debug("Setting key-value in redis.")
            await redis.set(key, value, expire=expires_in_second)

    async def get_value_by_key(self, key: str) -> bytes:
        try:
            async with self._connector as redis:
                logger.debug("Getting value from redis by key.")
                value = await redis.get(key)
            return value
        except Exception as excep:
            logger.exception(excep)
            raise

    async def increment_value_by_key(self, key: str) -> None:
        async with self._connector as redis:
            logger.debug("Incrementing key's value in Redis.")
            await redis.incr(key)

    async def key_exists(self, key: str) -> int:
        async with self._connector as redis:
            logger.debug("Checking if key exists in Redis.")
            return await redis.exists(key)
