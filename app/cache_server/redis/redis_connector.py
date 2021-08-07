import logging
import aioredis

from app.cache_server.connector import Connector
from app.utils.config_parser import ConfigFileParser

logger = logging.getLogger(__name__)


class RedisConnector(Connector):
    def __init__(self) -> None:
        super().__init__()
        self.host = ConfigFileParser.get_config_section("redis")["host"]        

    async def __aenter__(self):
        try:
            logger.info(f"Connecting to Redis server, host: {self.host}")
            self.redis = await aioredis.create_redis_pool(self.host)
            return self.redis
        except Exception as exception:
            logger.exception(exception)

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        logger.info(f"Closing Redis server connection.")
        self.redis.close()
        await self.redis.wait_closed()