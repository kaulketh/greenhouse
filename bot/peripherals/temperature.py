#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import conf.greenhouse_config as conf

temp, one, two, three, four = conf.lib.empty


def get_digit(integer, digit):
        return int(str(integer).__getitem__(digit))


def read_temperature():
    return int(open('/sys/class/thermal/thermal_zone0/temp').read())


def get_temperature():
    global temp, one, two, three, four
    temp = read_temperature()
    one = get_digit(temp, 0)
    two = get_digit(temp, 1)
    three = get_digit(temp, 2)
    four = get_digit(temp, 3)
    return conf.core_temp_format.format(one, two, three, four, conf.lib.decimal)


def get_temp_as_digits():
    get_temperature()
    round_temp = float('{1}{2}{0}{3}{4}'.format('.', one, two, three, four))
    result = str(int(round(round_temp)))
    """ 1.digit,  2.digit and '°' and 'C' """
    return [int(get_digit(int(result), 0)), int(get_digit(int(result), 1)), 36, 12]
