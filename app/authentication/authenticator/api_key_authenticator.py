from abc import ABC
from typing import NoReturn


class APIKeyAuthenticator(ABC):
    async def authenticate(self, api_key: str) -> None:
        raise NotImplementedError()
