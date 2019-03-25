#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
# logger.py
"""
logging tool
author: Thomas Kaulke, kaulketh@gmail.com
"""

import logging
import os
from logging.config import fileConfig


this_folder = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(this_folder, 'logger.ini')
fileConfig(config_file)


# enum that contains color codes
class TerminalColor:

    NO_COLOR = "\33[m"
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[0;36m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREY = '\033[0m'  # normal
    PURPLE = '\033[0;35m'
    WHITE = '\033[1m'  # bright white
    UNDERLINE = '\033[4m'
    LIGHT_BLUE = '\033[1;34m'
    LIGHT_PURPLE = '\033[1;35m'
    LIGHT_CYAN = '\033[1;36m'
    LIGHT_RED = '\033[1;31m'
    LIGHT_GREEN = '\033[1;32m'


# the decorator to apply on the logger methods info, warn, ...
def add_color(logger_method, color):
    def wrapper(message, *args, **kwargs):
        return logger_method(
            # the coloring is applied here.
            color+message+TerminalColor.NO_COLOR, *args, **kwargs)
    return wrapper


def get_logger(name=None):
    if name is None:
        name = __name__
    logger = logging.getLogger(name[0:15])

    for level, color in zip((
            "info", "warning", "error", "debug", "critical"), (
            TerminalColor.CYAN, TerminalColor.YELLOW, TerminalColor.RED, TerminalColor.BLUE, TerminalColor.LIGHT_RED)):
        setattr(logger, level, add_color(getattr(logger, level), color))

    return logger


if __name__ == '__main__':
    pass
