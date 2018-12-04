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


def getValues():
    global temperature
    global humidity
    
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        logging.info ((lib.temp + ': '+ conf.temp_format + lib.empty + lib.hum + ': ' + conf.hum_format).format(temperature,humidity))
    else:
        logging.info ('Failed to get values. Try again!')
        
    return


