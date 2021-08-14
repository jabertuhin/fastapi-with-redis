from abc import ABC
from typing import NoReturn
from fastapi.security import APIKeyHeader


class APIKeyAuthenticator(ABC):
    async def authenticate(api_key: str) -> NoReturn:
        raise NotImplementedError()
