from typing import NoReturn
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock

from app.cache_server.server_client import CacheServerClient
from app.exception.authentication_exception import AuthenticationException
from app.authentication.dummy_api_authenticator import DummyAuthenticator


class TestDummyAuthenticator(IsolatedAsyncioTestCase):
    def setUp(self) -> NoReturn:
        self.cache_server_client = Mock(wraps=CacheServerClient)
        self.dummy_authenticator = DummyAuthenticator(cache_server=self.cache_server_client)

    
    async def test_authenticate_when_invalid_api_key_should_raise_AuthenticationException(self):
        api_key = "124656"
        with self.assertRaises(AuthenticationException) as excep:
            _ = await self.dummy_authenticator.authenticate(api_key=api_key)

        self.assertEqual("Not a valid API KEY.", excep.exception.message)
        self.assertEqual(401, excep.exception.status_code)
        