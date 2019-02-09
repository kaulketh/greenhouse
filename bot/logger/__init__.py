import logging
""" this import makes get_logger directly accessible from logger.get_logger """
from logger.logger import get_logger

logging.getLogger(__name__).addHandler(logging.NullHandler())
