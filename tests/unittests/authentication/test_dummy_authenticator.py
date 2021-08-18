from typing import NoReturn
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, patch, AsyncMock

from app.utils.config_parser import ConfigFileParser
from app.cache_server.server_client import CacheServerClient
from app.exception.authentication_exception import AuthenticationException
from app.authentication.dummy_api_authenticator import DummyAuthenticator


class TestDummyAuthenticator(IsolatedAsyncioTestCase):
    @patch.object(ConfigFileParser, 'get_config_section')
    async def test_authenticate_when_invalid_api_key_should_raise_AuthenticationException(self,
                                                                                        mock_config_section):
        mock_config_section.side_effect = [{"limit": 20}, {"second": 60}]

        cache_server_client = Mock(wraps=CacheServerClient)
        dummy_authenticator = DummyAuthenticator(cache_server=cache_server_client)        

        api_key = "124656"
        with self.assertRaises(AuthenticationException) as excep:
            _ = await dummy_authenticator.authenticate(api_key=api_key)

        self.assertEqual("Not a valid API KEY.", excep.exception.message)
        self.assertEqual(401, excep.exception.status_code)
        
    @patch.object(ConfigFileParser, 'get_config_section')
    async def test_authenticate_when_valid_api_key_for_first_time_should_call_set_key_by_value(self,
                                                                                        mock_config_section):
        mock_config_section.side_effect = [{"limit": 20}, {"second": 60}]

        cache_server_client = AsyncMock(wraps=CacheServerClient)
        cache_server_client.get_value_by_key.return_value = None
        cache_server_client.set_key_value.return_value = None

        dummy_authenticator = DummyAuthenticator(cache_server=cache_server_client)        

        api_key = "x189-0sf0"        
        _ = await dummy_authenticator.authenticate(api_key=api_key)


        cache_server_client.get_value_by_key.assert_awaited_once()
        cache_server_client.set_key_value.assert_awaited_once()

    @patch.object(ConfigFileParser, 'get_config_section')
    async def test_authenticate_when_valid_api_key_in_limit_should_call_increment_value_by_key(self,
                                                                                        mock_config_section):
        mock_config_section.side_effect = [{"limit": 20}, {"second": 60}]

        cache_server_client = AsyncMock(wraps=CacheServerClient)
        cache_server_client.get_value_by_key.return_value = b'5'        
        cache_server_client.increment_value_by_key.return_value = None

        dummy_authenticator = DummyAuthenticator(cache_server=cache_server_client)        

        api_key = "x189-0sf0"        
        _ = await dummy_authenticator.authenticate(api_key=api_key)


        cache_server_client.get_value_by_key.assert_awaited_once()  
        cache_server_client.increment_value_by_key.assert_awaited_once()


    @patch.object(ConfigFileParser, 'get_config_section')
    async def test_authenticate_when_valid_api_key_crosses_limit_should_raise_AuthenticationException(self,
                                                                                                    mock_config_section):
        mock_config_section.side_effect = [{"limit": 20}, {"second": 60}]

        cache_server_client = AsyncMock(wraps=CacheServerClient)
        cache_server_client.get_value_by_key.return_value = b'20'                

        dummy_authenticator = DummyAuthenticator(cache_server=cache_server_client)        

        api_key = "x189-0sf0"     

        with self.assertRaises(AuthenticationException) as excep:
            _ = await dummy_authenticator.authenticate(api_key=api_key)

        self.assertEqual(f"API rate limit crossed as per terms and conditions. You have used this api 20 times in 60 seconds.", excep.exception.message)
        self.assertEqual(403, excep.exception.status_code)

        cache_server_client.get_value_by_key.assert_awaited_once()  
        cache_server_client.set_key_value.assert_not_awaited()
        cache_server_client.increment_value_by_key.assert_not_awaited()