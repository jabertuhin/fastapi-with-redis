import logging
import logging.config

from fastapi import FastAPI
from fastapi.params import Depends

from app.exception.exception_handlers import add_exception_in_handler
from app.authentication.authenticate import authenticate_and_increment_api_key_usage
from app.utils.config_parser import ConfigFileParser
from app.routers import health, process_pdf


app = FastAPI()


# add exception handlers
add_exception_in_handler(app)

# including router in the app
app.include_router(health.router)
app.include_router(process_pdf.router,
                   dependencies=[Depends(authenticate_and_increment_api_key_usage)])


# Setting config file parser
ConfigFileParser.setup_config("config.ini")


# Logging configuration
logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
