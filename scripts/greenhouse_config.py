#!/usr/bin/python
# -*- coding: utf-8 -*-
# configs, constants and methods
# author: Thomas Kaulke

import time
import RPi.GPIO as GPIO
import logging

# logger
logging.basicConfig(filename='./home/pi/scripts/TelegramBot/greenhouse.log', format='%(asctime)s %(levelname)-8s %(name)-25s %(message)s',datefmt='[%Y-%m-%d %H:%M:%S]', level=logging.INFO)

# API Token and Chat id          
#LIST_OF_ADMINS = ['mock to test']
LIST_OF_ADMINS = [00000000, 00000000] #thk1220, Annett
Api_Token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx" # ThK1220RealGreenHouse
# Api_Token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx" # ThK1220GreenHouse


# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# to use GPIO instead board pin numbers, then please adapt pin definition
# GPIO.setmode(GPIO.BCM)

# comment if warnings required
GPIO.setwarnings(False)

# def board pins/channels, refer hardware/rspi_gpio.info
RELAIS_01=29
RELAIS_02=31
RELAIS_03=33
RELAIS_04=35
RELAIS_05=37
RELAIS_06=36
RELAIS_07=38
RELAIS_08=40

All_In_One = (TOMATO_01, TOMATO_02, TOMATO_03, CHILI_01, CHILI_02, CHILI_03)
Tomatoes = (TOMATO_01, TOMATO_02, TOMATO_03)
Chilis = (CHILI_01, CHILI_02, CHILI_03)


# switch functions
def switch_on(pin):
    logging.info('switch on: ' + str(pin))
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    return

def switch_off(pin):
    logging.info('switch off: ' + str(pin))
    GPIO.output(pin,GPIO.HIGH)
    GPIO.cleanup(pin)
    return

# time stamp
timestamp=time.strftime('[%d.%m.%Y %H:%M:%S] ')
timestamp_line=time.strftime('`[%d.%m.%Y %H:%M:%S]\n---------------------\n`')

# live stream address
live = 'http://<url>'