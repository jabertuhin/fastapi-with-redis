from abc import ABC, abstractmethod


class Connector(ABC):
    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError()

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        raise NotImplementedError()
