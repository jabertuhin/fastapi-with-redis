import logging

from fastapi import Depends, status

from app.authentication.api_key_manipulation import get_api_key_with_time
from app.utils.config_parser import ConfigFileParser
from app.cache_server.server_client import CacheServerClient
from app.authentication.authenticator.api_key_authenticator import APIKeyAuthenticator
from app.cache_server.redis.redis_server_client import RedisServerClient
from app.exception.authentication_exception import AuthenticationException
from app.exception.messages import ExceptionMessage

logger = logging.getLogger(__name__)


class DummyAuthenticator(APIKeyAuthenticator):
    __allowed_api_keys = ["x189-0sf0", "0nmsd82sdf", "0ijnsd89"]

    def __init__(self,
                 cache_server: CacheServerClient = Depends(RedisServerClient)) -> None:
        super().__init__()
        self._cache_server = cache_server
        self._api_rate_limit = int(ConfigFileParser.get_config_section("api_rate")["limit"])
        self._api_rate_limit_time = int(ConfigFileParser.get_config_section("api_rate")["second"])

    async def authenticate(self, api_key: str) -> None:
        if api_key is None:
            raise AuthenticationException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          message=ExceptionMessage.UNAUTHORIZED_ERROR)

        user_api_key_with_time = get_api_key_with_time(api_key, self._api_rate_limit_time)
        api_usage_count = await self._cache_server.get_value_by_key(user_api_key_with_time)

        if api_usage_count is None:
            self._verify_api_key(api_key)
            return

        if int(api_usage_count) >= self._api_rate_limit:
            logger.info("API rate limit crossed.")
            raise AuthenticationException(status_code=status.HTTP_403_FORBIDDEN,
                                          message=ExceptionMessage.FORBIDDEN_API_KEY_ERROR.
                                          format(self._api_rate_limit, self._api_rate_limit_time))

    def _verify_api_key(self, api_key: str) -> None:
        logger.debug("Verifying API-key.")
        if api_key not in DummyAuthenticator.__allowed_api_keys:
            raise AuthenticationException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          message=ExceptionMessage.UNAUTHORIZED_ERROR)
