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


# the decorator to apply on the logger methods info, warn, ...
def __add_color(logger_method, color):
    def wrapper(message, *args, **kwargs):
        return logger_method(
            # the coloring is applied here.
            color+message+NO_COLOR, *args, **kwargs)
    return wrapper


# the decorator to set colors at runtime
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


def get_logger(name=None):
    if name is None:
        name = __name__
    logger = logging.getLogger(name[0:15])

    for level, color in zip((
            "info", "warn", "error", "debug"), (
            GREEN, ORANGE, RED, BLUE
    )):
        setattr(logger, level, __add_color(getattr(logger, level), color))

    return logger


if __name__ == '__main__':
    pass
