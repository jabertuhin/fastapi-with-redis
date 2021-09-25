from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock

from app.utils.config_parser import ConfigFileParser
from app.cache_server.server_client import CacheServerClient
from app.exception.authentication_exception import AuthenticationException
from app.authentication.authenticator.dummy_api_authenticator import DummyAuthenticator


class TestDummyAuthenticator(IsolatedAsyncioTestCase):

    @patch.object(ConfigFileParser, 'get_config_section')
    async def test_authenticate_when_api_key_is_none_should_raise_AuthenticationException(self,
                                                                                        mock_config_section):
        mock_config_section.side_effect = [{"limit": 20}, {"second": 60}]
        api_key = None

        cache_server_client = AsyncMock(wraps=CacheServerClient)

        dummy_authenticator = DummyAuthenticator(cache_server=cache_server_client)

        with self.assertRaises(AuthenticationException) as excep:
            _ = await dummy_authenticator.authenticate(api_key=api_key)

        self.assertEqual("Not authorized.", excep.exception.message)
        self.assertEqual(401, excep.exception.status_code)

    @patch("app.authentication.authenticator.dummy_api_authenticator.get_api_key_with_time")
    @patch.object(ConfigFileParser, 'get_config_section')
    async def test_authenticate_when_invalid_api_key_should_raise_AuthenticationException(self,
                                                                                        mock_config_section,
                                                                                        mock_get_api_key_with_time):
        mock_config_section.side_effect = [{"limit": 20}, {"second": 60}]
        api_key = "124656"

        mock_get_api_key_with_time.return_value = f"{api_key}:2"
        cache_server_client = AsyncMock(wraps=CacheServerClient)
        cache_server_client.get_value_by_key.return_value = None

        dummy_authenticator = DummyAuthenticator(cache_server=cache_server_client)

        with self.assertRaises(AuthenticationException) as excep:
            _ = await dummy_authenticator.authenticate(api_key=api_key)

        self.assertEqual("Not authorized.", excep.exception.message)
        self.assertEqual(401, excep.exception.status_code)

    @patch("app.authentication.authenticator.dummy_api_authenticator.get_api_key_with_time")
    @patch.object(ConfigFileParser, 'get_config_section')
    async def test_authenticate_when_valid_api_key_first_time_should_return_none(self,
                                                                                mock_config_section,
                                                                                mock_get_api_key_with_time):
        mock_config_section.side_effect = [{"limit": 20}, {"second": 60}]
        api_key = "x189-0sf0"

        mock_get_api_key_with_time.return_value = f"{api_key}:2"
        cache_server_client = AsyncMock(wraps=CacheServerClient)
        cache_server_client.get_value_by_key.return_value = None

        dummy_authenticator = DummyAuthenticator(cache_server=cache_server_client)

        actual = await dummy_authenticator.authenticate(api_key=api_key)

        self.assertIsNone(actual)
        cache_server_client.get_value_by_key.assert_awaited_once()


    @patch("app.authentication.authenticator.dummy_api_authenticator.get_api_key_with_time")
    @patch.object(ConfigFileParser, 'get_config_section')
    async def test_authenticate_when_valid_api_key_ninth_time_should_return_none(self,
                                                                                mock_config_section,
                                                                                mock_get_api_key_with_time):
        mock_config_section.side_effect = [{"limit": 20}, {"second": 60}]
        api_key = "x189-0sf0"

        mock_get_api_key_with_time.return_value = f"{api_key}:2"
        cache_server_client = AsyncMock(wraps=CacheServerClient)
        cache_server_client.get_value_by_key.return_value = b'9'

        dummy_authenticator = DummyAuthenticator(cache_server=cache_server_client)

        actual = await dummy_authenticator.authenticate(api_key=api_key)

        self.assertIsNone(actual)
        cache_server_client.get_value_by_key.assert_awaited_once()

    @patch("app.authentication.authenticator.dummy_api_authenticator.get_api_key_with_time")
    @patch.object(ConfigFileParser, 'get_config_section')
    async def test_authenticate_when_valid_api_key_crosses_limit_should_raise_AuthenticationException(self,
                                                                                                    mock_config_section,
                                                                                                    mock_get_api_key_with_time):
        mock_config_section.side_effect = [{"limit": 20}, {"second": 60}]

        api_key = "x189-0sf0"
        mock_get_api_key_with_time.return_value = f"{api_key}:2"
        cache_server_client = AsyncMock(wraps=CacheServerClient)
        cache_server_client.get_value_by_key.return_value = b'20'

        dummy_authenticator = DummyAuthenticator(cache_server=cache_server_client)

        with self.assertRaises(AuthenticationException) as excep:
            _ = await dummy_authenticator.authenticate(api_key=api_key)

        self.assertEqual(f"API rate limit crossed as per terms and conditions. You have used this api 20 times in 60 seconds.", excep.exception.message)
        self.assertEqual(403, excep.exception.status_code)

        cache_server_client.get_value_by_key.assert_awaited_once()
