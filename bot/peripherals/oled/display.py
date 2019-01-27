#!/usr/bin/python
# -*- coding: utf-8 -*-
# configs, constants and methods
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
from time import sleep
from PIL import Image, ImageFont
from peripherals.oled.lib_oled96 import Ssd1306
from smbus import SMBus
import logging

logging.basicConfig(filename=conf.log_file, format=conf.log_format, datefmt=conf.log_date_format, level=logging.INFO)

# Display setup, methods and members
""" 0 = Raspberry Pi 1, 1 = Raspberry Pi > 1 """
i2cbus = SMBus(1)
oled = Ssd1306(i2cbus)
draw = oled.canvas
c0 = '\''
c1 = u'°'
c2 = u'\xb0'


def get_digit(integer, digit):
    return int(str(integer).__getitem__(digit))


def get_temperature():
    return int(open('/sys/class/thermal/thermal_zone0/temp').read())


def get_temp():
    global round_temp
    round_temp = float('{1}{2}{0}{3}{4}'.format('.',
                                                get_digit(get_temperature(), 0),
                                                get_digit(get_temperature(), 1),
                                                get_digit(get_temperature(), 2),
                                                get_digit(get_temperature(), 3),
                                                get_digit(get_temperature(), 4)))
    global result
    result = str(int(round(round_temp)))
    one = get_digit(int(result), 0)
    two = get_digit(int(result), 1)
    temp_str = '{0}{1}{2}{3}'.format(str(one), str(two), c0, 'C')
    return temp_str


# Fonts
# font = ImageFont.load_default()
# font = ImageFont.truetype('FreeSerifItalic.ttf', 20)
font = ImageFont.truetype('arial.ttf', 12)
font2 = ImageFont.truetype('FreeSans.ttf', 12)


def animate():  # (temp, temp_value, hum, hum_value, time):
    # Display clear
    oled.cls()
    oled.display()
    # text
    draw.text((20, 0), "GREENHOUSE", font=font2, fill=255)
    draw.text((0, 18), "Temperature : " + str(get_temp()), font=font, fill=255)
    oled.display()
    sleep(1)
    draw.text((0, 36), "Humidity   : --,- %", font=font, fill=1)
    oled.display()
    sleep(5)
    oled.cls()
    # image inverted
    draw.rectangle((32, 0, 95, 63), outline=1, fill=1)
    draw.bitmap((32, 0), Image.open('pi_logo.png'), fill=0)
    oled.display()
    sleep(2)
    oled.cls()


if __name__ == '__main__':
    while 1:

        try:
            # animate()
            pass

        except KeyboardInterrupt:
            logging.error('Oled interrupted.')
            oled.cls()
            exit()

        except:
            logging.error('Oled: Any error or exception occurred!')
