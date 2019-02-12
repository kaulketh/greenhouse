#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

import os
import time
import sys


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


def main():
    global bot, chat
    bot = sys.argv[1]
    chat = sys.argv[2]
    temp_limit = 75
    message = 'Warning, you Greenhouse Raspi reaches a temperature over {}°C! Current temperature is about {}°C!'
    while True:
        if int(__measure_temp()) > temp_limit:
            __send_msg(message.format(str(temp_limit), str(temp)))
        time.sleep(10)


if __name__ == '__main__':
    main()

