#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

paths = (
    '/home/pi/scripts/TelegramBot',
    '/home/pi/scripts/TelegramBot/conf',
    '/home/pi/scripts/TelegramBot/peripherals',
    '/home/pi/scripts/TelegramBot/peripherals/dht',
    '/home/pi/scripts/TelegramBot/peripherals/four_digit',
    '/home/pi/scripts/TelegramBot/peripherals/oled',
    '/home/pi/scripts/TelegramBot/peripherals/oled/fonts'
         )


if __name__ == '__main__':
    for path in paths:
        sys.path.append(path)

#print(sys.path)
