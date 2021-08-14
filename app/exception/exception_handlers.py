from typing import NoReturn

from fastapi.applications import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from app.exception.authentication_exception import AuthenticationException
from app.exception.service_exception import ServiceException
from app.exception.base_exception import BaseException


# create custom exception in list
custom_exceptions = [AuthenticationException]


def custom_exception_handler(request: Request, exc: BaseException):
    return JSONResponse(status_code=exc.status_code,
                        content={"message": exc.message})


def service_exception_handler(request: Request, exc: ServiceException):
    return JSONResponse(status_code=exc.status_code,
                        content={"message": exc.message})



def add_exception_in_handler(app: FastAPI) -> NoReturn:
    # add custom exceptions
    for custom_exception in custom_exceptions:
        app.add_exception_handler(custom_exception, custom_exception_handler)

    # add service exception
    app.add_exception_handler(ServiceException, service_exception_handler)