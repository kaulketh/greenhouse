#!/usr/bin/python
# -*- coding: utf-8 -*-
# logging tool
# author: Thomas Kaulke, kaulketh@gmail.com

import logging
from logging.config import fileConfig

fileConfig('logger_config.ini')


def get_logger(name=None):
    if name is None:
        name = __name__
    logger = logging.getLogger(name)
    return logger

get_logger('Test').debug("debug test")
get_logger('Test').info("info test")
get_logger('Test').warning("warning test")
get_logger('Test').error("error test")
get_logger('Test').critical("critical test")

if __name__ == '__main__':
    pass
