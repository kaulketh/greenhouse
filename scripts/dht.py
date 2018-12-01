#!/usr/bin/python
# -*- coding: utf-8 -*-
# [#11] Add and implement the measurement of temperature and humidity
# author: Thomas Kaulke, kaulketh@gmail.com

import Adafruit_DHT
import greenhouse_config as conf

sensor = Adafruit_DHT.DHT22
pin = conf.DHT_PIN

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print 'Temperatur: {0:0.1f}°C Luftfeuchtigkeit: {1:0.1f}%'.format(temperature,humidity)
    #print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get values. Try again!')

