#!/usr/bin/python
# -*- coding: utf-8 -*-
# configs, constants and methods
# author: Thomas Kaulke

import access as access

import os
import sys
import time
import RPi.GPIO as GPIO
import logging


# API Token and Chat Id's from external file
admins = [access.thk, access.annett]
mainId = access.thk
token = access.token

# to use Raspberry Pi board pin numbers
def resetPins():
    logging.info('Setup GPIO mode.')
    GPIO.setmode(GPIO.BOARD)
    # to use GPIO instead board pin numbers, then please adapt pin definition
    # GPIO.setmode(GPIO.BCM)
    # comment if warnings required
    GPIO.setwarnings(False)
    return
    

# def board pins/channels, refer hardware/rspi_gpio.info
RELAIS_01 = 29
RELAIS_02 = 31
RELAIS_03 = 33
RELAIS_04 = 35
RELAIS_05 = 37
RELAIS_06 = 36
RELAIS_07 = 38
RELAIS_08 = 40

GROUP_ALL = (RELAIS_01, RELAIS_02, RELAIS_03, RELAIS_04,
             RELAIS_05, RELAIS_06, RELAIS_07, RELAIS_08)
GROUP_01 = (RELAIS_01, RELAIS_02, RELAIS_03)
GROUP_02 = (RELAIS_06, RELAIS_07, RELAIS_08)
GROUP_03 = (RELAIS_04, RELAIS_05)

# live stream address
live = access.live

# logging
log_file = 'greenhouse.log'
log_format = '%(asctime)s %(levelname)-8s %(name)-10s %(message)s'
log_date_format = '[%Y-%m-%d %H:%M:%S]'
logging.basicConfig(filename=log_file, format=log_format,
                    datefmt=log_date_format, level=logging.INFO)
# command to run extended bot
run_extended_greenhouse = 'sudo python /home/pi/scripts/TelegramBot/ext_greenhouse.py '

# camera commands
enable_camera = 'sudo modprobe bcm2835-v4l2 && sudo service motion start & '
disable_camera = 'sudo service motion stop && sudo modprobe -r bcm2835-v4l2 & '

# gpio check
run_gpio_check = 'sudo python /home/pi/scripts/TelegramBot/gpio_check.py & '
stop_gpio_check = 'sudo pkill -f /home/pi/scripts/TelegramBot/gpio_check.py & '

# switch functions
def switch_on(pin):
    logging.info('switch on: ' + str(pin))
    os.system(run_gpio_check)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    return

def switch_off(pin):
    logging.info('switch off: ' + str(pin))
    os.system(stop_gpio_check)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    GPIO.cleanup(pin)
    return

# date time strings
def getTimestamp():
    return time.strftime('[%d.%m.%Y %H:%M:%S] ')
    
def getTimestampLine():
    return time.strftime('`[%d.%m.%Y %H:%M:%S]\n---------------------\n`')