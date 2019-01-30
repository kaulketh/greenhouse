#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
#import conf.greenhouse_config as config
#import peripherals.four_digit.display as display
import threading
import logging
import time

#logging.basicConfig(filename=config.log_file, format=config.log_format,
#                    datefmt=config.log_date_format, level=logging.INFO)

#seconds_steps = config.lib.time_units_conversion
t = None
count = None


# def display_count(number):
#     display.show_duration(number)
#     return
#
#
# def countdown(period):
#     global t
#     global count
#     count = period
#     logging.info("counter : " + str(count))
#     count -= 1
#     if count > 0:
#         t = threading.Timer(seconds_steps, display_count(count))
#         t.start()
#     else:
#         t.cancel()
#         logging.info("counter finished: " + str(count))

count = 5
seconds_steps = 1

def downwards():
    global t
    global count
    global seconds_steps
    # logging.info("counter :" + str(count))
    print(time.strftime('[%d.%m.%Y %H:%M:%S]') + " counter : " + str(count))
    count -= 1
    if count > 0:
        t = threading.Timer(seconds_steps, downwards)
        t.start()
    else:
        t.cancel()
        print("finished")


if __name__ == '__main__':
    downwards()
