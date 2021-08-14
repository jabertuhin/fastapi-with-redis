# Github Issue: https://github.com/tiangolo/fastapi/issues/142
import logging
from typing import List, NoReturn

from fastapi.param_functions import Depends
from fastapi.params import Security
from fastapi.security.api_key import APIKeyHeader

from app.exception.service_exception import ServiceException
from app.authentication.api_key_authenticator import APIKeyAuthenticator
from app.exception.authentication_exception import AuthenticationException
from app.authentication.dummy_api_authenticator import DummyAuthenticator


logger = logging.getLogger(__name__)

API_KEY_NAME = "x-api-key"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def authenticate_api_key(api_key: str = Security(API_KEY_HEADER),
                            authenticator: APIKeyAuthenticator = Depends(DummyAuthenticator)) -> NoReturn:
    try:                            
        await authenticator.authenticate(api_key)        
    except AuthenticationException as excep:
        logger.exception(excep)
        raise
    except Exception as excep:
        logger.exception(excep)
        raise ServiceException()