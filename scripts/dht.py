#!/usr/bin/python
# -*- coding: utf-8 -*-
# [#11] Add and implement the measurement of temperature and humidity
# author: Thomas Kaulke, kaulketh@gmail.com

import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
gpio = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

print 'Temperatur: {0:0.1f}°C Luftfeuchtigkeit: {1:0.1f}%'.format(temperature,humidity)
