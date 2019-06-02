#!/usr/bin/python
# -*- coding: utf-8 -*-
# oled.display.py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

from __future__ import absolute_import

import subprocess
from time import sleep

import conf
import logger
import utils
from PIL import Image, ImageFont
from lib_oled96 import Ssd1306
from smbus import SMBus

# Display setup, methods and members
logger = logger.get_logger()
""" 0 = Raspberry Pi 1, 1 = Raspberry Pi > 1 """
i2cbus = SMBus(1)
oled = Ssd1306(i2cbus)
draw = oled.canvas
c = '\''
left = 5
top = 7
switch_time = 15
bot_dir = conf.bot_dir

# Fonts
font = ImageFont.truetype(str(bot_dir) + 'peripherals/oled/fonts/arial.ttf', 12)
font2 = ImageFont.truetype(str(bot_dir) + 'peripherals/oled/fonts/FreeSans.ttf', 12)


def __get_core_temp():
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read())
    one = str(temp).__getitem__(0)
    two = str(temp).__getitem__(1)
    temp_str = '{0}{1}{2}{3}'.format(one, two, c, 'C')
    return temp_str


def __animate(time):
    # Display clear
    oled.cls()
    oled.display()
    # header
    draw.text((left, top), conf.application_name + conf.space + utils.get_release(), font=font, fill=1)
    # build
    draw.text((left, top + 18), "Build: " + utils.get_last_commit(), font=font2, fill=1)
    # line
    draw.line((left, top + 35, oled.width - left + 128, top + 35), fill=1)
    # core temp
    draw.text((left, top + 45), "Core Temperature: " + __get_core_temp(), font=font2, fill=1)
    oled.display()
    sleep(time)


def __show_pi(time):
    oled.cls()
    # image inverted
    draw.rectangle((32, top - 3, 95, 63), outline=1, fill=1)
    draw.bitmap((32, top - 3), Image.open(str(bot_dir) + 'peripherals/oled/pi_logo.png'), fill=0)
    oled.display()
    sleep(time)


def __show_state(time):
    oled.cls()
    oled.display()
    """
    Shell scripts for system monitoring from here :
    https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    """
    cmd = "hostname -I | cut -d\' \' -f1"
    ip = subprocess.check_output(cmd, shell=True)
    cmd = "top - bn1 | grep \"Cpu(s)\" | sed \"s/.*, *\\([0-9.]*\\)%* id.*/\\1/\" | " \
          "awk '{print \"CPU Load : \"100 - $1\"%\"}'"
    # cmd = "top -bn1 | grep load | awk '{printf \"CPU Load : %.2f\", $(NF-2)}'"
    cpu = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"Mem : %s / %s MB %.0f%%\", $3,$2,$3*100/$2 }'"
    mem_usage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk : %d / %d GB %s\", $3,$2,$5}'"
    disk = subprocess.check_output(cmd, shell=True)

    # Write the lines of text.
    draw.text((left, top), "IP : " + str(ip), font=font2, fill=255)
    draw.text((left, top + 15), str(cpu), font=font2, fill=255)
    draw.text((left, top + 30), str(mem_usage), font=font2, fill=255)
    draw.text((left, top + 45), str(disk), font=font2, fill=255)
    oled.display()
    sleep(time)


if __name__ == '__main__':
    while True:

        try:
            __animate(switch_time)
            __show_pi(switch_time/5)
            __show_state(switch_time)

        except KeyboardInterrupt:
            print('Oled interrupted.')
            oled.cls()
            exit()

        except:
            print('Oled: Any error or exception occurred!')
