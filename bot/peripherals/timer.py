#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import conf.greenhouse_config as config
import peripherals.four_digit.display as display
from greenhouse import Water_Time
import threading
import logging

logging.basicConfig(filename=config.log_file, format=config.log_format,
                    datefmt=config.log_date_format, level=logging.INFO)

count = Water_Time
seconds_steps = config.lib.time_units_conversion
t = None


def display_count(number):
    display.show_duration(number)
    return


def countdown():
    global t
    global count
    logging.info("counter : " + str(count))
    count -= 1
    if count > 0:
        t = threading.Timer(seconds_steps, display_count(count))
        t.start()
    else:
        t.cancel()
        logging.info("counter finished: " + str(count))



