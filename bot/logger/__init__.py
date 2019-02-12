# logger.__init__py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""
from .logger import get_logger
from .logger import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
