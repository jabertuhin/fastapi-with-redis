from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock

from app.utils.config_parser import ConfigFileParser
from app.cache_server.server_client import CacheServerClient
from app.authentication.api_usage.redis_api_usage_incrementor import RedisApiUsageIncrementor


class TestRedisApiUsageIncrementor(IsolatedAsyncioTestCase):
    @patch("app.authentication.api_usage.redis_api_usage_incrementor.get_api_key_with_time")
    @patch.object(ConfigFileParser, 'get_config_section')
    async def test_increment_when_key_doesnt_exists_should_call_set_key_value_with_expiry_time_once(self,
                                                                                                    mock_config_section,
                                                                                                    mock_get_api_key_with_time):
        api_key = "123abc"
        mock_get_api_key_with_time.return_value = f"{api_key}:2"
        mock_config_section.return_value = {"second": 60}

        cache_server_client = AsyncMock(wraps=CacheServerClient)
        cache_server_client.key_exists.return_value = 0
        cache_server_client.set_key_value_with_expiry_time.return_value = None

        api_usage_incrementor = RedisApiUsageIncrementor(cache_server_client)

        actual = await api_usage_incrementor.increment(api_key=api_key)

        self.assertIsNone(actual)
        cache_server_client.key_exists.assert_awaited_once()
        cache_server_client.set_key_value_with_expiry_time.assert_awaited_once()

    @patch("app.authentication.api_usage.redis_api_usage_incrementor.get_api_key_with_time")
    @patch.object(ConfigFileParser, 'get_config_section')
    async def test_increment_when_key_exists_should_call_increment_value_by_key_once(self,
                                                                                    mock_config_section,
                                                                                    mock_get_api_key_with_time):
        api_key = "123abc"
        mock_get_api_key_with_time.return_value = f"{api_key}:2"
        mock_config_section.return_value = {"second": 60}

        cache_server_client = AsyncMock(wraps=CacheServerClient)
        cache_server_client.key_exists.return_value = 1
        cache_server_client.increment_value_by_key.return_value = None

        api_usage_incrementor = RedisApiUsageIncrementor(cache_server_client)

        actual = await api_usage_incrementor.increment(api_key=api_key)

        self.assertIsNone(actual)
        cache_server_client.key_exists.assert_awaited_once()
        cache_server_client.set_key_value_with_expiry_time.assert_not_awaited()
        cache_server_client.increment_value_by_key.assert_awaited_once()
