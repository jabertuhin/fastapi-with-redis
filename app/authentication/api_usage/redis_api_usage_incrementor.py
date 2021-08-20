import logging

from fastapi import Depends

from app.utils.config_parser import ConfigFileParser
from app.authentication.api_key_manipulation import get_api_key_with_time
from app.authentication.api_usage.api_usage_incrementor import ApiUsageIncrementor
from app.cache_server.server_client import CacheServerClient
from app.cache_server.redis.redis_server_client import RedisServerClient


logger = logging.getLogger(__name__)


class RedisApiUsageIncrementor(ApiUsageIncrementor):
    def __init__(self, 
                cache_server: CacheServerClient = Depends(RedisServerClient)) -> None:
        super().__init__()
        self._cache_server = cache_server
        self._api_rate_limit_time = int(ConfigFileParser.get_config_section("api_rate")["second"])

    async def increment(self, api_key: str) -> None:
        user_api_key_with_time = get_api_key_with_time(api_key=api_key, time=self._api_rate_limit_time)

        key_existence = await self._cache_server.key_exists(user_api_key_with_time)

        if key_existence == 0:
            logger.debug(f"Setting key with default value 1 in Redis.")
            await self._cache_server.set_key_value(key=user_api_key_with_time,                                                
                                                value=1,
                                                expires_in_second=self._api_rate_limit_time)
            return                                            

        logger.debug(f"Incrementing key value.")
        await self._cache_server.increment_value_by_key(user_api_key_with_time)
        