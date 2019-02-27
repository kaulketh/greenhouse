#!/usr/bin/python
# -*- coding: utf-8 -*-
# monitor.py
# author: Thomas Kaulke, kaulketh@gmail.com
# Temperature monitoring

from __future__ import absolute_import
import os
import time
import sys
from conf import temperature_warn, temperature_min, temperature_max, fan_pin, check_interval, mainId, token
import logger
import utils.utils as utils


logger = logger.get_logger()


def __measure_temp():
    global temp
    temp = os.popen("vcgencmd measure_temp").readline()
    temp = temp.replace("temp=", "")
    temp = temp[0:2]
    return temp


def __send_msg(msg):
    os.system('curl -s -k https://api.telegram.org/bot{0}/sendMessage -d text="{1}" -d chat_id={2}'
              .format(bot, str(msg), str(chat)))
    return


def __check_if_fan_required():
    temperature = int(__measure_temp())
    # TODO: remove if pin set!
    logger.warning('Current core temp: {}°C'.format(temperature))
    if temperature > temperature_max:
        logger.warning("Heat dissipation: Fan on")
        utils.switch_out_high(fan_pin)
    if temperature < temperature_min:
        logger.info("Heat dissipation: Fan off")
        utils.switch_out_low(fan_pin)
    return


def main():
    logger.info('Temperature monitoring started.')
    utils.set_pins()
    global bot, chat
    bot = token
    chat = mainId
    temp_limit = temperature_warn
    message = 'Warning, you Greenhouse Raspi reaches a temperature over {}°C! Current temperature is about {}°C!'
    while True:
        __check_if_fan_required()
        if int(__measure_temp()) > temp_limit:
            __send_msg(message.format(str(temp_limit), str(temp)))
        time.sleep(check_interval)


if __name__ == '__main__':
    pass
