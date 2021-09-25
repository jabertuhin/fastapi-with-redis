import logging

import configparser
from typing import Dict

from app import ROOT_DIR

logger = logging.getLogger(__name__)


class ConfigFileParser:
    @staticmethod
    def setup_config(file_name: str) -> None:
        config_file_path = ROOT_DIR / file_name
        logger.debug(f"Setting config file path. FilePath: {config_file_path}")
        ConfigFileParser._config_parser = configparser.ConfigParser()
        ConfigFileParser._config_parser.read(config_file_path)

    @staticmethod
    def get_config_section(section: str) -> Dict[str, str]:
        try:
            return ConfigFileParser._config_parser[section]
        except Exception as error:
            logger.exception(error)
            raise
