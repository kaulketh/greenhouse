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
def __add_color(logger_method, msg_color):
    def wrapper(message, *args, **kwargs):
        return logger_method(
            # the coloring is applied here.
            msg_color+message+TerminalColor.NO_COLOR, *args, **kwargs)
    return wrapper


def __add_coloring_to_emit_ansi(logging_method):
    # add methods we need to the class
    def wrapper(*args):
        levelno = args[1].levelno
        if levelno >= 50:
            color = TerminalColor.LIGHT_RED  # CRITICAL
        elif levelno >= 40:
            color = TerminalColor.RED  # ERROR
        elif levelno >= 30:
            color = TerminalColor.YELLOW  # WARNING
        elif levelno >= 20:
            color = TerminalColor.GREEN  # INFO
        elif levelno >= 10:
            color = TerminalColor.BLUE  # DEBUG
        else:
            color = TerminalColor.GREY  # normal
        args[1].msg = color+str(args[1].msg)+TerminalColor.GREY   # normal
        # print "after"
        return logging_method(*args)
    return wrapper


def get_logger(name=None):
    # all non-Windows platforms are supporting ANSI escapes
    logging.StreamHandler.emit = __add_coloring_to_emit_ansi(logging.StreamHandler.emit)
    if name is None:
        name = __name__
    logger = logging.getLogger(name[0:15])

    for level, color in zip((
            "info", "warning", "error", "debug", "critical"), (
            TerminalColor.GREEN, TerminalColor.YELLOW, TerminalColor.RED, TerminalColor.BLUE, TerminalColor.LIGHT_RED)):
        setattr(logger, level, __add_color(getattr(logger, level), color))

    return logger


if __name__ == '__main__':
    pass
