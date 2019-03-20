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


# timeout if no user activity
standby_timeout = 120


# keyboard configs
kb1 = [[lib.channel_1, lib.channel_2, lib.channel_3, lib.channel_4],
       [lib.channel_5, lib.channel_6, lib.channel_7, lib.channel_8],
       [lib.grouping],
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

# board pins of relays, refer hardware/raspi_gpio.info
RELAY_01 = 29
RELAY_02 = 31
RELAY_03 = 33
RELAY_04 = 35
RELAY_05 = 37
RELAY_06 = 36
RELAY_07 = 38
RELAY_08 = 40

ALL = (RELAY_01, RELAY_02, RELAY_03, RELAY_04, RELAY_05, RELAY_06, RELAY_07, RELAY_08)

# live stream address
live = access.live

# command to run extended bot
run_extended_greenhouse = 'sudo python /home/pi/scripts/TelegramBot/ext_greenhouse.py '

# camera commands
enable_camera = 'sudo service motion start & '
disable_camera = 'sudo service motion stop && sudo rm -rf /home/pi/Monitor/* &'

# gpio check
run_gpio_check = 'sudo python /home/pi/scripts/TelegramBot/gpio_check.py '

# heat dissipation, temperature monitoring, fan control
temperature_warn = 75
temperature_min = 40
temperature_max = 60
fan_pin = 12
check_interval = 10

if __name__ == '__main__':
    pass
