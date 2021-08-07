import asyncio
import aioredis
from typing import NoReturn

from fastapi import Depends
from app.cache_server import connector

from app.cache_server.server_client import CacheServerClient
from app.cache_server.connector import Connector
from app.cache_server.redis.redis_connector import RedisConnector



class RedisServerClient(CacheServerClient):
    def __init__(self, connector: Connector = Depends(RedisConnector)) -> NoReturn:
        super().__init__()
        self.connector = connector   

    async def set_key_value(key: str, value: int)-> NoReturn:
        raise NotImplementedError()

    async def get_value(self, key: str)-> int:
        async with connector as redis:
            value = redis.get(key)

        return value

    async def increment_value(key: str, value: int)-> NoReturn:
        raise NotImplementedError()