import logging
import aioredis

from app.cache_server.connector import Connector
from app.utils.config_parser import ConfigFileParser
from app.exception.service_exception import ServiceException

logger = logging.getLogger(__name__)


class RedisConnector(Connector):
    def __init__(self) -> None:
        super().__init__()
        self.host = ConfigFileParser.get_config_section("redis")["host"]        
        self.port = ConfigFileParser.get_config_section("redis")["port"]

    async def __aenter__(self):
        try:
            logger.info(f"Connecting to Redis server, host: {self.host}")
            self.redis = await aioredis.create_redis_pool(f"{self.host}:{self.port}", encoding="utf-8")
            return self.redis
        except Exception as exp:
            logger.exception(exp)
            raise ServiceException()

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        try:
            logger.info(f"Closing Redis server connection.")
            self.redis.close()
            await self.redis.wait_closed()
        except Exception as exp:
            logger.exception(exp)
            raise ServiceException()