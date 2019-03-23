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

"""https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output"""
NO_COLOR = "\33[m"
RED, GREEN, ORANGE, BLUE, PURPLE, LBLUE, GREY = map("\33[%dm".__mod__, range(31, 38))


# decorator to apply on the logger methods info, warn, ...
def __add_color(logger_method, color):
    def wrapper(message, *args, **kwargs):
        return logger_method(
            # the coloring is applied here.
            color+message+NO_COLOR, *args, **kwargs)
    return wrapper


# decorator to set colors at runtime, e.g. logger.debug("message", color=GREY)
def __add_color_at_runtime(logger_method, _color):
    def wrapper(message, *args, **kwargs):
        color = kwargs.pop("color", _color)
        if isinstance(color, int):
            color = "\33[%dm" % color
        return logger_method(
            # the coloring is applied here.
            color+message+NO_COLOR, *args, **kwargs)
    return wrapper


this_folder = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(this_folder, 'logger.ini')
fileConfig(config_file)


# enum that contains color codes
class TerminalColor:
    """
    Color formatting codes
    """
    # https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREY = '\033[0m'  # normal
    WHITE = '\033[1m'  # bright white
    UNDERLINE = '\033[4m'


# apply colors to log levels
def __apply_colors():
    logging.addLevelName(logging.INFO, "{0}{1}{2}".format(
        TerminalColor.WHITE, logging.getLevelName(logging.INFO), TerminalColor.GREY))
    logging.addLevelName(logging.WARNING, "{0}{1}{2}".format(
        TerminalColor.YELLOW, logging.getLevelName(logging.WARNING), TerminalColor.GREY))
    logging.addLevelName(logging.ERROR, "{0}{1}{2}".format(
        TerminalColor.RED, logging.getLevelName(logging.ERROR), TerminalColor.GREY))
    logging.addLevelName(logging.CRITICAL, "{0}{1}{2}".format(
        TerminalColor.MAGENTA, logging.getLevelName(logging.CRITICAL), TerminalColor.GREY))
    return


def get_logger(name=None):
    if name is None:
        name = __name__
    logger = logging.getLogger(name[0:15])

    for level, color in zip(("INFO", "WARNING", "ERROR", "DEBUG"), (GREEN, ORANGE, RED, BLUE)):
        setattr(logger, level, __add_color(getattr(logger, level), color))

    return logger


if __name__ == '__main__':
    pass
