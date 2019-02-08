#!/usr/bin/python
# -*- coding: utf-8 -*-
# [#11] Add and implement the measurement of temperature and humidity
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import Adafruit_DHT
import conf.greenhouse_config as conf
import logger.logger as log

logging = log.get_logger('dht')

lib = conf.lib
sensor = Adafruit_DHT.DHT22
pin = conf.DHT_PIN



def get_values():
    global temperature
    global humidity
    logging.info('Try to get temperature and humidity values.')
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        logging.info(('{0}{1}{2}{3}{4}{1}{5}'.format(
            lib.temp, lib.colon_space, conf.temp_format, lib.space, lib.hum, conf.hum_format))
                     .format(temperature, humidity))
    else:
        logging.warning('Failed to get temperature and humidity values. Set to \'0\'!')
        humidity = 0
        temperature = 0 
    return


if __name__ == '__main__':
    pass
