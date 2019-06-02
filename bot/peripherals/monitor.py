#!/usr/bin/python
# -*- coding: utf-8 -*-
# monitor.py
# author: Thomas Kaulke, kaulketh@gmail.com
# Temperature monitoring and fan control

from __future__ import absolute_import
import os
import time
import sys
from conf import temperature_warn, temperature_min, temperature_max, fan_pin, check_interval, mainId, token
import logger
import utils.utils as utils


logger = logger.get_logger()
message = 'Warning, your RaspberryPi reaches a temperature over {}°C! Current temperature is about {}°C!'


def __calc_core_temp():
    temp1 = os.popen("vcgencmd measure_temp").readline()
    temp1 = temp1.replace("temp=", "")
    temp1 = round(float(temp1[0:4]), 4)
    temp2 = open('/sys/class/thermal/thermal_zone0/temp').read()
    temp2 = round((int(temp2))/1000, 4)
    temp = (temp1 + temp2) / 2
    return int(temp)


def __send_msg(msg, bot, chat):
    os.system('curl -s -k https://api.telegram.org/bot{0}/sendMessage -d text="{1}" -d chat_id={2}'
              .format(str(bot), str(msg), str(chat)))
    return


def __fan_control(temp):
    if temp >= temperature_max:
        if int(utils.get_pin_state(fan_pin)) == 0:
            logger.warning('Current core temperature: {0}°C {1}'.format(str(temp), "Heat dissipation: Fan on"))
            utils.switch_out_high(fan_pin)
    if temp <= temperature_min:
        if int(utils.get_pin_state(fan_pin)) == 1:
            logger.info('Core temperature: {0}°C {1}'.format(str(temp), "Heat dissipation: Fan off"))
    return


def main():
    logger.info('Temperature monitoring started.')
    utils.set_pins()
    while True:
        current_temp = __calc_core_temp()
        __fan_control(current_temp)
        if current_temp > temperature_warn:
            __send_msg(message.format(str(temperature_warn), str(current_temp)), token, mainId)
        time.sleep(check_interval)


if __name__ == '__main__':
    pass
