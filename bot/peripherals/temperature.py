#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import conf.greenhouse_config as conf


def get_digit(integer, digit):
        return int(str(integer).__getitem__(digit))


temp = int(open('/sys/class/thermal/thermal_zone0/temp').read())

one = get_digit(temp, 0)
two = get_digit(temp, 1)
three = get_digit(temp, 2)
four = get_digit(temp, 3)
# five = get_digit(temp, 4)


def get_temperature():
        return conf.lib.core_temp_format.format(one, two, three, four, conf.lib.decimal)


print get_temperature()
