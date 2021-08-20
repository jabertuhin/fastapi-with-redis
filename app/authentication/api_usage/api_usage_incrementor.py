from abc import ABC
from typing import NoReturn


class ApiUsageIncrementor(ABC):
    async def increment(self, api_key: str) -> NoReturn:
        return NotImplementedError()