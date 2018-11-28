#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke

from subprocess import Popen, PIPE, STDOUT, call

import greenhouse_config as config

import os
import commands
import time
import RPi.GPIO as GPIO
import logging

logging.basicConfig(filename=config.log_file, format=config.log_format,
                    datefmt=config.log_date_format, level=logging.INFO)

pin_to_check = sys.argv[1]
gpios = (21, 22, 23, 24, 25, 27, 28, 29)
pins =  config.GROUP_ALL

def getState(pin):
    proc = Popen('gpio read ' + str(pin), shell=True, stdout=PIPE,)
    output = proc.communicate()[0]
    return output

index = pins.index(pin_to_check)
gpio = gpios[index]
state = int(getState(gpio))
            
if state == 0:
    logging.info('GPIO.' + str(gpio) + ':' + str(state) + ' -> Valve open at pin ' + str(pins[index]) + '!')



   
