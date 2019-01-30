#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import greenhouse as mainbot
import conf.greenhouse_config as config
import peripherals.four_digit.display as display
import threading
import logging
import time

logging.basicConfig(filename=config.log_file, format=config.log_format,
                    datefmt=config.log_date_format, level=logging.INFO)

seconds_steps = config.lib.time_units_conversion
t = None
count = None


def _display_count(number):
    display.show_duration(number)


def _show_channel_or_group(channel):
    if channel is int:
        display.show_group(channel)
    else:
        display.show_channel(channel)


def countdown(channel, counter):
    _show_channel_or_group(channel)
    return


def switch_to_standby(wait):
    global t
    global count
    count = wait
    t = threading.Timer(wait, mainbot.stop())
    t.start()
    count -= wait
    if count == 0:
        t.cancel()
        logging.info("switched to standby automatically")


count = 5
seconds_steps = 1


# TODO: only for test, remove if not needed!
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
    pass
