#!/usr/bin/python
# -*- coding: utf-8 -*-
# script for boot animation
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import logging
import conf.greenhouse_config as conf
import peripherals.display as display
from time import sleep

logging.basicConfig(filename=conf.log_file, format=conf.log_format,
                    datefmt=conf.log_date_format, level=logging.INFO)

animation = (42, 43, 44, 45, 46, 47, 48)
digits = (0, 1, 2, 3)
sleep_time = 0.1


def show(sign, digit):
    display.display.show1(sign, digit)
    sleep(sleep_time)
    display.display.clear()
    return


while 1:
    try:
        for i in animation:
            show(i, 0)
            show(i, 1)
            show(i, 2)
            show(i, 3)

    except Exception:
        logging.warning('Any error occurs - ' + Exception.__qualname__)
        display.show_error()

