from datetime import datetime
import logging
from typing import NoReturn

from fastapi import Depends, status

from app.utils.config_parser import ConfigFileParser
from app.cache_server.server_client import CacheServerClient
from app.authentication.api_key_authenticator import APIKeyAuthenticator
from app.cache_server.redis.redis_server_client import RedisServerClient
from app.exception.authentication_exception import AuthenticationException
from app.exception.messages import ExceptionMessage


logger = logging.getLogger(__name__)


class DummyAuthenticator(APIKeyAuthenticator):
    __allowed_api_keys = ["x189-0sf0", "0nmsd82sdf", "0ijnsd89"]

    def __init__(self, 
                cache_server: CacheServerClient = Depends(RedisServerClient)) -> NoReturn:
        super().__init__()
        self.cache_server = cache_server
        self.api_rate_limit = int(ConfigFileParser.get_config_section("api_rate")["limit"])
        self.api_rate_limit_time = int(ConfigFileParser.get_config_section("api_rate")["second"])

    async def authenticate(self, api_key: str) -> NoReturn:
        # TODO: Refactor this method to reduce if-else conditions.
        self._verify_api_key(api_key)

        user_api_key_with_minute = f"{api_key}:{str(datetime.now().minute)}"
        hit_count = await self.cache_server.get_value_by_key(user_api_key_with_minute)        
        if hit_count is None:
            logger.info(f"Initializing key with value.")
            await self.cache_server.set_key_value(key=user_api_key_with_minute,                                                
                                                value=1,
                                                expires_in_second=self.api_rate_limit_time) 
        elif int(hit_count) < self.api_rate_limit:
            logger.info(f"Incrementing key value.")
            await self.cache_server.increment_value_by_key(user_api_key_with_minute)
        else:
            logger.info(f"API rate limit crossed.")
            raise AuthenticationException(status_code=status.HTTP_403_FORBIDDEN,
                                        message=ExceptionMessage.FORBIDDEN_API_KEY_ERROR.format(self.api_rate_limit,
                                                                                                self.api_rate_limit_time))


    def _verify_api_key(self, api_key) -> NoReturn:
        if api_key not in DummyAuthenticator.__allowed_api_keys:
            raise AuthenticationException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        message=ExceptionMessage.UNAUTHORIZED_EXCEPTION)