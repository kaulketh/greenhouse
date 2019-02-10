#!/usr/bin/python
# -*- coding: utf-8 -*-
# configs and constants and methods
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import time
import RPi.GPIO as GPIO
import logger.logger as log

"""logging is configured in logger package in logger.ini"""
logging = log.get_logger()

# switch functions
def switch_on(pin):
    logging.info('switch on: ' + str(pin))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    # os.system(run_gpio_check + str(pin))
    return


def switch_off(pin):
    logging.info('switch off: ' + str(pin))
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
