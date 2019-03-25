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


# the decorator,
""" https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output """
def __add_coloring_to_emit_ansi(logging_method):
    # add methods we need to the class
    def wrapper(*args):
        level_number = args[1].levelno
        if level_number >= 50:
            """ CRITICAL """
            color = TerminalColor.LIGHT_RED

        elif level_number >= 40:
            """ ERROR """
            color = TerminalColor.RED

        elif level_number >= 30:
            """WARNING """
            color = TerminalColor.YELLOW

        elif level_number >= 20:
            """ INFO """
            color = TerminalColor.CYAN

        elif level_number >= 10:
            """ DEBUG """
            color = TerminalColor.BLUE

        else:
            """ default """
            color = TerminalColor.GREY
        # print "after"
        args[1].msg = color + str(args[1].msg) + color + TerminalColor.NO_COLOR
        return logging_method(*args)
    return wrapper


def get_logger(name=None):
    logging.StreamHandler.emit = __add_coloring_to_emit_ansi(logging.StreamHandler.emit)
    """ all non-Windows platforms are supporting ANSI escapes """

    if name is None:
        name = __name__
    logger = logging.getLogger(name[0:15])
    return logger


if __name__ == '__main__':
    pass
