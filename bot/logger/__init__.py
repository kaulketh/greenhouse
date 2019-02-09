from .logger import get_logger
from .logger import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
