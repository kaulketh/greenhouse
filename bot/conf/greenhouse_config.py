#!/usr/bin/python
# -*- coding: utf-8 -*-
# greenhouse_config.py

"""
configs, command strings and constants
author: Thomas Kaulke, kaulketh@gmail.com
"""
import access as access
from lib_global import language_index
"""
 language settings
 import required lib
 set index in global library 
"""
if language_index == 0:
    import conf.lib_english as lib
elif language_index == 1:
    import conf.lib_german as lib
else:
    import conf.lib_english as lib

# API Token and Chat Id's from external file
admins = [access.thk, access.annett]
mainId = access.thk
token = access.token
standby_timeout = 60


# keyboard configs
kb1 = [[lib.group1[1], lib.group1[2], lib.group1[3], lib.group3[1]],
       [lib.group3[2], lib.group2[1], lib.group2[2], lib.group2[3]],
       [lib.group1[0], lib.group3[0], lib.group2[0]],
       [lib.all_channels],
       [lib.stop_bot, lib.live_stream, lib.reload]
       ]
kb2 = [[lib.cancel, lib.stop_bot]]
kb3 = [[lib.emergency_stop]]

# 7-segment display settings
clk_pin = 32
dio_pin = 22
""" 1 to 7 """
brightness = 1

# DHT sensor settings
DHT_PIN = 4
temp_format = '{:04.1f}°C'
hum_format = '{:05.2f}%'

# Raspi core temperature
core_temp_format = '{0}{1}{4}{2}{3}°C'

# def board pins/channels, refer hardware/raspi_gpio.info
RELAIS_01 = 29
RELAIS_02 = 31
RELAIS_03 = 33
RELAIS_04 = 35
RELAIS_05 = 37
RELAIS_06 = 36
RELAIS_07 = 38
RELAIS_08 = 40

GROUP_ALL = (RELAIS_01, RELAIS_02, RELAIS_03, RELAIS_04, RELAIS_05, RELAIS_06, RELAIS_07, RELAIS_08)
GROUP_01 = (RELAIS_01, RELAIS_02, RELAIS_03)
GROUP_02 = (RELAIS_06, RELAIS_07, RELAIS_08)
GROUP_03 = (RELAIS_04, RELAIS_05)

# live stream address
live = access.live

# command to run extended bot
run_extended_greenhouse = 'sudo python /home/pi/scripts/TelegramBot/ext_greenhouse.py '

# camera commands
enable_camera = 'sudo service motion start & '
disable_camera = 'sudo service motion stop && sudo rm -rf /home/pi/Monitor/* &'

# gpio check
run_gpio_check = 'sudo python /home/pi/scripts/TelegramBot/gpio_check.py '


if __name__ == '__main__':
    pass
