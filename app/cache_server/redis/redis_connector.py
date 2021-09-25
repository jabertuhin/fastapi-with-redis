import logging
import aioredis

from app.cache_server.connector import Connector
from app.utils.config_parser import ConfigFileParser
from app.exception.service_exception import ServiceException

logger = logging.getLogger(__name__)


class RedisConnector(Connector):
    def __init__(self) -> None:
        super().__init__()
        self._host = ConfigFileParser.get_config_section("redis")["host"]
        self._port = ConfigFileParser.get_config_section("redis")["port"]
        self._db_index = int(ConfigFileParser.get_config_section("redis")["db_index"])
        self._address = f"{self._host}:{self._port}/{self._db_index}"

    async def __aenter__(self):
        try:
            logger.debug(f"Connecting to Redis server, host: {self._host}")
            self.redis = await aioredis.create_redis_pool(self._address, encoding="utf-8")
            return self.redis
        except Exception as exp:
            logger.exception(exp)
            raise ServiceException()

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        try:
            logger.debug("Closing Redis server connection.")
            self.redis.close()
            await self.redis.wait_closed()
        except Exception as exp:
            logger.exception(exp)
            raise ServiceException()
