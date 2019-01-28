#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

import os
import time
import sys

bot = sys.argv[1]
chat = sys.argv[2]
temp_limit = 75
temp = 0
message = 'Warning, you RaspberryPi reaches a temperature over {}°C! ' \
          'Current temperature is about {}°C!'.format(str(temp_limit), temp)


def measure_temp():
    global temp
    temp = os.popen("vcgencmd measure_temp").readline()
    temp = temp.replace("temp=", "")
    temp = temp[0:2]
    return temp


def send_msg(msg):
    os.system('curl -s -k https://api.telegram.org/bot{0}/sendMessage -d text="{1}" -d chat_id={2}'
              .format(bot, str(msg), str(chat)))
    return


while True:
    if int(measure_temp()) > temp_limit:
        send_msg(message)
    time.sleep(10)
