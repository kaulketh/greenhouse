#!/usr/bin/python
# -*- coding: utf-8 -*-
# monitor.py
# author: Thomas Kaulke, kaulketh@gmail.com
# Temperature monitoring
# Will be started by cron job after reboot.
# e.g. @reboot sleep 60 && sudo python /home/pi/scripts/TelegramBot/peripherals/monitor.py <bot_token> <chat_id>


from __future__ import absolute_import
import os
import time
import sys
import utils.utils as utils
import conf
import logger

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


# TODO: if fan pin is set in greenhouse_config.py, activate/uncomment fan switching
def __check_if_fan_required():
    temperature = int(__measure_temp())
    if temperature > conf.temperature_max:
        logger.info("Heat dissipation: Fan on")
        # utils.switch_on(conf.fan_pin)
    if temperature < conf.temperature_min:
        logger.info("Heat dissipation: Fan off")
        # utils.switch_off(conf.fan_pin)
    return


def main():
    utils.set_pins()
    global bot, chat
    bot = sys.argv[1]
    chat = sys.argv[2]
    temp_limit = conf.temperature_warn
    message = 'Warning, you Greenhouse Raspi reaches a temperature over {}°C! Current temperature is about {}°C!'
    while True:
        __check_if_fan_required()
        if int(__measure_temp()) > temp_limit:
            __send_msg(message.format(str(temp_limit), str(temp)))
        time.sleep(conf.check_interval)


if __name__ == '__main__':
    main()
