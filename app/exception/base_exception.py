from typing import NoReturn


class BaseException(Exception):
    def __init__(self, status_code: int, message: str) -> NoReturn:
        self.status_code = status_code
        self.message = message
