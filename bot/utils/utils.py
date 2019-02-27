#!/usr/bin/python
# -*- coding: utf-8 -*-
# utils.py

"""
useful methods
author: Thomas Kaulke, kaulketh@gmail.com
"""

from __future__ import absolute_import
import time
import os
import RPi.GPIO as GPIO
import logger

"""logging is configured in logger package in logger.ini"""
logging = logger.get_logger()


# switch functions
def switch_on(pin):
    logging.info('switch to LOW: ' + str(pin))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    # os.system(run_gpio_check + str(pin))
    return


def switch_off(pin):
    logging.info('switch to HIGH: ' + str(pin))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    # os.system(run_gpio_check + str(pin))
    GPIO.cleanup(pin)
    return


# date time strings
def get_timestamp():
    return time.strftime('[%d.%m.%Y %H:%M:%S] ')


def get_timestamp_line():
    return time.strftime('`[%d.%m.%Y %H:%M:%S]\n---------------------\n`')


# gets the state of pin, if 0 is switched on
def get_pin_state(pin):
    GPIO.setup(pin, GPIO.OUT)
    return GPIO.input(pin)


# to use Raspberry Pi board pin numbers
def set_pins():
    GPIO.setmode(GPIO.BOARD)
    logging.info('Set GPIO mode: GPIO.BOARD')
    # to use GPIO instead board pin numbers, then please adapt pin definition
    # GPIO.setmode(GPIO.BCM)
    # comment if warnings required
    GPIO.setwarnings(False)
    return GPIO


# Execute bash command, assign default output (stdout 1 and stderr 2) to file, read in variable and get back
def read_cmd(cmd, tmp_file):
    os.system(cmd + ' > ' + tmp_file + ' 2>&1')
    file = open(tmp_file, 'r')
    data = file.read()
    file.close()
    return data


if __name__ == '__main__':
    pass
