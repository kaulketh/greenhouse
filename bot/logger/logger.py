#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
# logger.py
"""
logging tool
author: Thomas Kaulke, kaulketh@gmail.com
"""

import logging
import os
import ConfigParser
from logging.config import fileConfig
from conf import get_path

logger_ini = 'logger.ini'

this_folder = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(this_folder, logger_ini)

CONFIG = ConfigParser.ConfigParser()
CONFIG.read(config_file)
CONFIG.set('handler_stream_handler', 'args', value=get_path('file_log_debug'))
CONFIG.set('handler_file_handler', 'args', value=get_path('file_log_greenhouse'))

fileConfig(config_file)


def get_logger(name=None):
    if name is None:
        name = __name__
    logger = logging.getLogger(name[0:15])
    return logger


if __name__ == '__main__':
    pass
