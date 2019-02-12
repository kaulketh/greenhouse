#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import conf.greenhouse_config as conf
import logger.logger as log

logging = log.get_logger()

temp = 0
one = 0
two = 0
three = 0
four = 0


def __get_digit(integer, digit):
        return int(str(integer).__getitem__(digit))


def __read_temperature():
    return int(open('/sys/class/thermal/thermal_zone0/temp').read())


def get_temperature():
    global temp, one, two, three, four
    temp = __read_temperature()
    one = __get_digit(temp, 0)
    two = __get_digit(temp, 1)
    three = __get_digit(temp, 2)
    four = __get_digit(temp, 3)
    temp_str = conf.core_temp_format.format(one, two, three, four, conf.lib.decimal)
    logging.info('Formatted core temperature value to message: ' + temp_str)
    return temp_str


def get_temp_as_digits():
    get_temperature()
    round_temp = float('{1}{2}{0}{3}{4}'.format('.', one, two, three, four))
    result = str(int(round(round_temp)))
    """ 1.digit,  2.digit and '°' and 'C' """
    logging.info('Rounded core temperature value for 4-digit display: ' + result)
    return [int(__get_digit(int(result), 0)), int(__get_digit(int(result), 1)), 36, 12]


if __name__ == '__main__':
    pass
