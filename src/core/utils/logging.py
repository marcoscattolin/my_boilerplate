#  Copyright (c) 2023, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary

import logging
import os
import uuid
from logging import handlers

from core.config import base_path

LOGS = "logs"


class PathConfig:
    """
    Class to load path configuration for log files
    """

    def __init__(self):
        # id
        self.run_id = uuid.uuid4()

        # logs
        self.log_path = os.path.join(base_path, LOGS)

        os.makedirs(self.log_path, exist_ok=True)


def get_logger(conf: PathConfig, log_level=logging.WARNING) -> logging.Logger:
    """
    Method initializing logger

    :param conf: PathConfig object containing logging path configuration
    :param log_level: level at which logs are produced, defaults to warning
    :return: logger to be used when logging messages

    """
    # define log filename
    logfile = f"{conf.log_path}/logfile.log"

    # define log format
    log_format = "%(asctime)s, [%(name)s] [%(levelname)s] : %(message)s"

    # init logger
    logger = logging.getLogger(str(conf.run_id))
    logger.setLevel(log_level)

    # Add rotating logfile handler (max 5 backups, 1 megabyte each)
    rotating_handler = handlers.RotatingFileHandler(
        logfile, maxBytes=10**6, backupCount=5
    )
    rotating_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(rotating_handler)

    # add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)

    logger.propagate = False
    return logger


# init path configuration
path_conf = PathConfig()
logger = get_logger(conf=path_conf, log_level=logging.DEBUG)

# print debug messages
logger.debug(f"Logging into {path_conf.log_path}")
