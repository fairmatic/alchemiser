import logging
import sys
from typing import Optional
from warnings import warn

logger: Optional[logging.Logger] = None


warn(message=f'The module {__name__} is deprecated. Please switch to fmlib.fmlogger', category=DeprecationWarning, stacklevel=2)

def setup_logging():
    global logger

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(process)d %(thread)d %(asctime)s [%(name)s][%(levelname)s]::%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def error(*args, **kwargs):
    logger.exception(*args)


# Setup logger
setup_logging()
