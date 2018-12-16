#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

import greenhouse_config as conf

def get_digit(integer, digit):
        return int(str(integer).__getitem__(digit))


temp = int(open('/sys/class/thermal/thermal_zone0/temp').read())

one = get_digit(temp, 0)
two = get_digit(temp, 1)
three = get_digit(temp, 2)
four = get_digit(temp, 3)
# five = get_digit(temp, 4)

temp_str = '{0}{1}{4}{2}{3}°C'.format(one, two, three, four, conf.lib.decimal)
print temp_str
