from abc import ABC
from typing import NoReturn


class CacheServerClient(ABC):
    """An interface for cache server."""
    async def set_key_value_with_expiry_time(self, key: str, value: int)-> NoReturn:
        raise NotImplementedError()

    async def get_value_by_key(self, key: str)-> int:
        raise NotImplementedError()

    async def increment_value_by_key(self, key: str)-> NoReturn:
        raise NotImplementedError()

    async def key_exists(self, key: str) -> int:
        raise NotImplementedError()