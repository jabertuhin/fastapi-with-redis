from abc import ABC
from typing import NoReturn


class CacheServerClient(ABC):
    """An interface for cache server."""
    async def set_key_value(key: str, value: int)-> NoReturn:
        raise NotImplementedError()

    async def get_value(key: str)-> int:
        raise NotImplementedError()

    async def increment_value(key: str, value: int)-> NoReturn:
        raise NotImplementedError()
