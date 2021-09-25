from fastapi import status

from app.exception.messages import ExceptionMessage


class ServiceException(Exception):
    def __init__(self,
                 status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
                 message: str = ExceptionMessage.INTERNAL_SERVER_ERROR) -> None:
        self.status_code = status_code
        self.message = message
