#!/usr/bin/python
# -*- coding: utf-8 -*-
# script for boot animation
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import logging
import thread
import conf.greenhouse_config as conf
import peripherals.display as display
from time import sleep

logging.basicConfig(filename=conf.log_file, format=conf.log_format,
                    datefmt=conf.log_date_format, level=logging.INFO)

animation = (42, 43, 44, 45, 46, 47, 48)
digits = (0, 1, 2, 3)
sleep_time = 0.2


def show(sign, digit):
    display.display.show1(digit, sign)
    sleep(sleep_time)
    display.display.clear()
    return


def animate(digit):
    for a in animation:
        show(a, digit)
    return


def thread_func(digit):
    thread.start_new_thread(animate, digit)


def run():
    pass
    """
        try:
            for d in digits:
                thread_func(d)

        except Exception:
            logging.warning('Any error occurs')
            display.show_error()
    """


if __name__ == '__main__':
    run()
