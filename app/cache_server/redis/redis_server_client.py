from typing import NoReturn
import logging

from fastapi import Depends

from app.cache_server.server_client import CacheServerClient
from app.cache_server.connector import Connector
from app.cache_server.redis.redis_connector import RedisConnector

logger = logging.getLogger(__name__)


class RedisServerClient(CacheServerClient):
    def __init__(self, connector: Connector = Depends(RedisConnector)) -> NoReturn:
        super().__init__()
        self.connector = connector   

    async def set_key_value(self, key: str, value: int = 1, expires_in_second: int = 60)-> NoReturn:
        async with self.connector as redis:                        
            await redis.set(key, value, expire=expires_in_second)

    async def get_value_by_key(self, key: str)-> str:
        try:
            async with self.connector as redis:                
                logger.info(f"Getting value from redis by key.")
                value = await redis.get(key)                            
            return value
        except Exception as excep:
            logger.exception(excep)
            raise

    async def increment_value_by_key(self, key: str)-> NoReturn:
        async with self.connector as redis:
            logger.info("Incrementing key's value in Redis.")            
            await redis.incr(key)
