#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

# from __future__ import absolute_import
import sys
import thread
from time import sleep
from PIL import Image, ImageFont
from lib_oled96 import Ssd1306
# import conf.greenhouse_config as conf
# import peripherals.temperature as core
from smbus import SMBus
import logging

# logging.basicConfig(filename=conf.log_file, format=conf.log_format, datefmt=conf.log_date_format, level=logging.INFO)

# Display setup, methods and members
""" 0 = Raspberry Pi 1, 1 = Raspberry Pi > 1 """
i2cbus = SMBus(1)
oled = Ssd1306(i2cbus)
draw = oled.canvas
c0 = '\''
c1 = u'°'
c2 = u'\xb0'


def get_last_commit():
    commit = open("/lastGreenhouseCommit.id").read()
    return commit[0:6]


def get_core_temp():
    temp_str = int(open('/sys/class/thermal/thermal_zone0/temp').read())
    one = temp_str.__getitem__(0)
    two = temp_str.__getitem__(1)
    temp_str = '{0}{1}{2}{3}'.format(one, two, c0, 'C')
    return temp_str


# Fonts
# font = ImageFont.load_default()
# font = ImageFont.truetype('arial.ttf', 12)
font2 = ImageFont.truetype('FreeSans.ttf', 12)


def animate():
    # Display clear
    oled.cls()
    oled.display()
    # header
    draw.text((18, 0), "GREENHOUSE", font=font2, fill=1)
    oled.display()
    sleep(1)
    # line
    draw.line((oled.width+1, 1, oled.width-1, 1), fill=1)
    oled.display()
    sleep(1)
    # core temp
    draw.text((0, 18), "Core temperature: " + get_core_temp(), font=font2, fill=1)
    oled.display()
    sleep(1)
    # build
    draw.text((0, 36), "Build : " + get_last_commit(), font=font2, fill=1)
    oled.display()
    sleep(10)
    oled.cls()
    # image inverted
    draw.rectangle((32, 0, 95, 63), outline=1, fill=1)
    draw.bitmap((32, 0), Image.open('pi_logo.png'), fill=0)
    oled.display()
    sleep(3)


def run_in_separate_thread():
    thread.start_new_thread(animate, ())


if __name__ == '__main__':
    while 1:

        try:
            animate()

        except KeyboardInterrupt:
            # logging.error
            print ('Oled thread interrupted.')
            oled.cls()
            exit()

        except:
            # logging.error
            print('Oled thread: Any error or exception occurred!')
