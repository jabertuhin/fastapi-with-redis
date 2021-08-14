from typing import NoReturn

from app.exception.base_exception import BaseException


class AuthenticationException(BaseException):
    def __init__(self, status_code: int, message: str) -> NoReturn:
        super().__init__(status_code, message)