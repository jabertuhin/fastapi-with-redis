from abc import ABC


class CacheServerClient(ABC):
    """An interface for cache server."""
    async def set_key_value_with_expiry_time(self,
                                             key: str,
                                             value: int,
                                             expires_in_second: int) -> None:
        raise NotImplementedError()

    async def get_value_by_key(self, key: str) -> bytes:
        raise NotImplementedError()

    async def increment_value_by_key(self, key: str) -> None:
        raise NotImplementedError()

    async def key_exists(self, key: str) -> int:
        raise NotImplementedError()
