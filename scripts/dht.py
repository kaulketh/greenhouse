#!/usr/bin/python
# -*- coding: utf-8 -*-
# [#11] Add and implement the measurement of temperature and humidity
# author: Thomas Kaulke, kaulketh@gmail.com

import Adafruit_DHT
import time
import sys
import logging
import greenhouse_config as conf

# language library selection
lib = conf.lib

logging.basicConfig(filename=conf.log_file, format=conf.log_format, datefmt=conf.log_date_format, level=logging.INFO)

sensor = Adafruit_DHT.DHT22
pin = conf.DHT_PIN


def get_values():
    global temperature
    global humidity
    
    #sensor broken, deactivated
    humidity = 0
    temperature = 0 
    # humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        #logging.info(('{0}{1}{2}{3}{4}{1}{5}'.format(lib.temp, lib.colon_space, conf.temp_format, lib.space, lib.hum, conf.hum_format)).format(temperature, humidity))
        logging.info('Measuring disabled!')
    else:
        logging.info('Failed to get temperature and humidity values. Set to \'0\'!')
        humidity = 0
        temperature = 0 
    return


