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



def __apply_level_colors(level, lvl_color, msg_color):
    logging.addLevelName(level, "{0}{1}{2}".format(lvl_color, logging.getLevelName(level), msg_color))
    return


def get_logger(name=None):
    if name is None:
        name = __name__
    logger = logging.getLogger(name[0:15])

    __apply_level_colors(logging.DEBUG, TerminalColor.PURPLE, TerminalColor.GREY)
    __apply_level_colors(logging.INFO, TerminalColor.CYAN, TerminalColor.BLUE)
    __apply_level_colors(logging.WARNING, TerminalColor.YELLOW, TerminalColor.WHITE)
    __apply_level_colors(logging.ERROR, TerminalColor.RED, TerminalColor.WHITE)
    __apply_level_colors(logging.CRITICAL, TerminalColor.LIGHT_RED, TerminalColor.RED)

    return logger


if __name__ == '__main__':
    pass
