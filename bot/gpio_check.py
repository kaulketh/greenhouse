#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
from subprocess import Popen, PIPE, STDOUT, call
import os
import sys
import commands
import time
import RPi.GPIO as GPIO
import logging
import conf.greenhouse_config as config

logging.basicConfig(filename=config.log_file, format=config.log_format,
                    datefmt=config.log_date_format, level=logging.INFO)

pin_to_check = int(sys.argv[1])
gpios = (21, 22, 23, 24, 25, 27, 28, 29)
# == config.GROUP_ALL 
pins = (29, 31, 33, 35, 37, 36, 38, 40)


def get_state(pin):
    proc = Popen('gpio read ' + str(pin), shell=True, stdout=PIPE,)
    output = proc.communicate()[0]
    return output


index = pins.index(pin_to_check)
gpio = gpios[int(index)]
state = int(get_state(gpio))

if state == 0:
    logging.info('GPIO.' + str(gpio) + ':' + str(state) + ' -> Valve open at pin ' + str(pins[index]) + '!')

if state == 1:
    logging.info('GPIO.' + str(gpio) + ':' + str(state) + ' -> Valve closed at pin ' + str(pins[index]) + '!')
