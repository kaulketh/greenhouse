#!/usr/bin/python
# -*- coding: utf-8 -*-
# gpio_check.py

"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

from __future__ import absolute_import
from subprocess import Popen, PIPE
import sys
import logger.logger as log

logging = log.get_logger()

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
