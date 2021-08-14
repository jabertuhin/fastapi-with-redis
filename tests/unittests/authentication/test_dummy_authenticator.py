from typing import NoReturn
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, patch

from app.utils.config_parser import ConfigFileParser
from app.cache_server.redis.redis_server_client import RedisServerClient
from app.exception.authentication_exception import AuthenticationException
from app.authentication.dummy_api_authenticator import DummyAuthenticator


class TestDummyAuthenticator(IsolatedAsyncioTestCase):
    @patch.object(ConfigFileParser, 'get_config_section')
    async def test_authenticate_when_invalid_api_key_should_raise_AuthenticationException(self,
                                                                                        mock_config_section):
        mock_config_section.side_effect = [{"limit": 20}, {"second": 60}]

        cache_server_client = Mock(wraps=RedisServerClient)
        dummy_authenticator = DummyAuthenticator(cache_server=cache_server_client)        

        api_key = "124656"
        with self.assertRaises(AuthenticationException) as excep:
            _ = await dummy_authenticator.authenticate(api_key=api_key)

        self.assertEqual("Not a valid API KEY.", excep.exception.message)
        self.assertEqual(401, excep.exception.status_code)
        