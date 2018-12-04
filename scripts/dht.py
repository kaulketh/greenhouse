#!/usr/bin/python
# -*- coding: utf-8 -*-
# [#11] Add and implement the measurement of temperature and humidity
# author: Thomas Kaulke, kaulketh@gmail.com

import Adafruit_DHT
import time
import sys
import logging
import greenhouse_config as conf
import greenhouse_lib_german as lib

logging.basicConfig(filename=conf.log_file, format=conf.log_format, datefmt=conf.log_date_format, level=logging.INFO)

sensor = Adafruit_DHT.DHT22
pin = conf.DHT_PIN
interval = sys.argv[1]


def getValues():
    global humidity
    global temperature
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        logging.info ((lib.temperature + ': {0:04.1f}°C ' + lib.humidity + ': {1:05.2f}%').format(temperature,humidity))
    else:
        logging.info ('Failed to get values. Try again!')


while 1:
    try:
        getValues()
        time.sleep(int(interval))

    except KeyboardInterrupt:
        logging.warning('Humidity and temperature measurement interrupted')
        exit()

    except :
        logging.error('Humidity and temperature measurement, error or exception occured!')
