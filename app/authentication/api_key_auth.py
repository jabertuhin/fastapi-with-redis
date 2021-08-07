from abc import ABC
from typing import NoReturn
from fastapi.security import APIKeyHeader

API_KEY_NAME = "x-api-key"


api_key_header = APIKeyHeader(name=API_KEY_NAME, 
                            scheme_name="API Key",
                            auto_error=True)


class APIKeyAuthenticator(ABC):
    async def authenticate(api_key: str) -> NoReturn:
        raise NotImplementedError()
