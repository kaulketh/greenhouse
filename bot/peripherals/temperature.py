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


def get_temperature():
        return conf.core_temp_format.format(one, two, three, four, conf.lib.decimal)


def get_temp_as_digits():
    round_temp = float('{1}{2}{0}{3}{4}'.format('.',
                                                get_digit(get_temperature(), 0), get_digit(get_temperature(), 1),
                                                get_digit(get_temperature(), 2), get_digit(get_temperature(), 3),
                                                get_digit(get_temperature(), 4)))
    result = str(int(round(round_temp)))
    # 1.digit,  2.digit and '°' and 'C'
    return [int(get_digit(int(result), 0)), int(get_digit(int(result), 1)), 36, 12]
