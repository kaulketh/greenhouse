#!/usr/bin/python
# -*- coding: utf-8 -*-
# configs, constants and methods
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import time
import RPi.GPIO as GPIO
import logging
import conf.access as access

# language selection
""" for English import greenhouse_lib_english """
import conf.greenhouse_lib_german as lib


# API Token and Chat Id's from external file
admins = [access.thk, access.annett]
mainId = access.thk
token = access.token


# keyboard configs
kb1 = [[lib.group1[1], lib.group1[2], lib.group1[3], lib.group3[1]],
       [lib.group3[2], lib.group2[1], lib.group2[2], lib.group2[3]],
       [lib.group1[0], lib.group3[0], lib.group2[0]],
       [lib.all_channels],
       [lib.stop_bot, lib.live_stream, lib.reload]
       ]
kb2 = [[lib.cancel, lib.stop_bot]]


# to use Raspberry Pi board pin numbers
def reset_pins():
    logging.info('Setup GPIO mode.')
    GPIO.setmode(GPIO.BOARD)
    # to use GPIO instead board pin numbers, then please adapt pin definition
    # GPIO.setmode(GPIO.BCM)
    # comment if warnings required
    GPIO.setwarnings(False)
    return


# 7-segment display settings
# TODO: setup 7-segment display pins!
clk_pin = 99
dio_pin = 99
brightness = 0.5

# DHT settings
DHT_PIN = 4
temp_format = '{:04.1f}°C'
hum_format = '{:05.2f}%'

# core temperature
core_temp_format = '{0}{1}{4}{2}{3}°C'

# def board pins/channels, refer hardware/raspi_gpio.info
RELAIS_01 = 29
RELAIS_02 = 31
RELAIS_03 = 33
RELAIS_04 = 35
RELAIS_05 = 37
RELAIS_06 = 36
RELAIS_07 = 38
RELAIS_08 = 40

GROUP_ALL = (RELAIS_01, RELAIS_02, RELAIS_03, RELAIS_04, RELAIS_05, RELAIS_06, RELAIS_07, RELAIS_08)
GROUP_01 = (RELAIS_01, RELAIS_02, RELAIS_03)
GROUP_02 = (RELAIS_06, RELAIS_07, RELAIS_08)
GROUP_03 = (RELAIS_04, RELAIS_05)

# live stream address
live = access.live

# logging
log_file = 'greenhouse.log'
log_format = '%(asctime)s %(levelname)-8s %(name)-10s %(message)s'
log_date_format = '[%Y-%m-%d %H:%M:%S]'
logging.basicConfig(filename=log_file, format=log_format, datefmt=log_date_format, level=logging.INFO)
# command to run extended bot
run_extended_greenhouse = 'sudo python /home/pi/scripts/TelegramBot/ext_greenhouse.py '

# camera commands
enable_camera = 'sudo service motion start & '
disable_camera = 'sudo service motion stop && sudo rm -rf /home/pi/Monitor/* &'

# gpio check
run_gpio_check = 'sudo python /home/pi/scripts/TelegramBot/gpio_check.py '


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
