#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import thread
import subprocess
from time import sleep
from PIL import Image, ImageFont, ImageDraw
from lib_oled96 import Ssd1306
import conf.greenhouse_config as conf
# import peripherals.temperature as core
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
font = ImageFont.truetype('/home/pi/scripts/TelegramBot/peripherals/oled/fonts/arial.ttf', 12)
font2 = ImageFont.truetype('/home/pi/scripts/TelegramBot/peripherals/oled/fonts/FreeSans.ttf', 12)


def animate():
    # Display clear
    oled.cls()
    oled.display()
    # header
    draw.text((18, 0), "GREENHOUSE", font=font, fill=1)
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


def show_state():
    width = oled.width
    height = oled.height
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw_image = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw_image.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Draw a black filled box to clear the image.
    draw_image.rectangle((0, 0, width, height), outline=0, fill=0)

    """
    Shell scripts for system monitoring from here : 
    https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    """
    cmd = "hostname -I | cut -d\' \' -f1"
    ip = subprocess.check_output(cmd, shell=True)
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    cpu = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    mem_usage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    disk = subprocess.check_output(cmd, shell=True)

    # Write two lines of text.

    draw_image.text((x, top), "ip: " + str(ip), font=font, fill=255)
    draw_image.text((x, top + 8), str(cpu), font=font, fill=255)
    draw_image.text((x, top + 16), str(mem_usage), font=font, fill=255)
    draw_image.text((x, top + 25), str(disk), font=font, fill=255)

    # Display image.
    oled.image(image)
    oled.display()
    sleep(10)


def run_in_separate_thread():
    thread.start_new_thread(animate, ())


if __name__ == '__main__':
    while 1:

        try:
            animate()
            show_state()

        except KeyboardInterrupt:
            logging.error('Oled thread interrupted.')
            oled.cls()
            exit()

        except:
            logging.error('Oled thread: Any error or exception occurred!')
