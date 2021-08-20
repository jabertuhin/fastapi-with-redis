# Github Issue: https://github.com/tiangolo/fastapi/issues/142
import logging
from typing import List, NoReturn

from fastapi.param_functions import Depends
from fastapi.params import Security
from fastapi.security.api_key import APIKeyHeader

from app.exception.service_exception import ServiceException
from app.authentication.api_usage.redis_api_usage_incrementor import RedisApiUsageIncrementor
from app.authentication.api_usage.api_usage_incrementor import ApiUsageIncrementor
from app.authentication.authenticator.api_key_authenticator import APIKeyAuthenticator
from app.exception.authentication_exception import AuthenticationException
from app.authentication.authenticator.dummy_api_authenticator import DummyAuthenticator


logger = logging.getLogger(__name__)

API_KEY_NAME = "x-api-key"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def authenticate_and_increment_api_key_usage(api_key: str = Security(API_KEY_HEADER),
                            authenticator: APIKeyAuthenticator = Depends(DummyAuthenticator),
                            api_usage_incrementor: ApiUsageIncrementor = Depends(RedisApiUsageIncrementor)) -> None:
    try:                            
        await authenticator.authenticate(api_key)        
        await api_usage_incrementor.increment(api_key)
    except AuthenticationException as excep:
        logger.exception(excep)
        raise
    except Exception as excep:
        logger.exception(excep)
        raise ServiceException()