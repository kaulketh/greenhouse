#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

import os
import time
import sys

bot = sys.argv[1]
chat = sys.argv[2]
temp_value = 0
temp_limit = 75
message = 'Warning, you RaspberryPi reaches a temperature over {} °C! ' \
          'Current temperature is about {}°C!'.format(str(temp_limit), temp_value)


def measure_temp():
    global temp_value
    temp = os.popen("vcgencmd measure_temp").readline()
    temp_value = int(temp[0:2])
    return temp.replace("temp=", "")


def send_msg(message):
    os.system('curl -s -k https://api.telegram.org/bot{0}/sendMessage -d text="{1}" -d chat_id={2}'
              .format(bot, message, str(chat)))
    return


while True:
        if measure_temp() > temp_limit:
            send_msg(message)
        time.sleep(10)
