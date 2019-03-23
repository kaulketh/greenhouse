#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
# logger.py
"""
logging tool
author: Thomas Kaulke, kaulketh@gmail.com

color: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
"""

import logging
import os
from logging.config import fileConfig


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


# the decorator to apply on the logger methods info, warn, ...
def add_color(logger_method, color):
    def wrapper(message, *args, **kwargs):
        return logger_method(
            # the coloring is applied here.
            color+message+NO_COLOR, *args, **kwargs)
    return wrapper


def get_logger(name=None):
    if name is None:
        name = __name__
    logger = logging.getLogger(name[0:15])

    for level, color in zip(("info", "warn", "error", "debug"),
                            (TerminalColor.GREEN, TerminalColor.YELLOW, TerminalColor.RED, TerminalColor.BLUE)):
        setattr(logger, level, add_color(getattr(logger, level), color))
    return logger


if __name__ == '__main__':
    pass
