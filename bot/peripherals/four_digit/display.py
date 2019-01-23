#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
from time import sleep
from conf.greenhouse_config import clk_pin, dio_pin, brightness
import peripherals.four_digits as tm1637
import peripherals.temperature as core_temp

display = tm1637.TM1637(clk=clk_pin, dio=dio_pin, brightness=brightness)

group1 = [12, 1, 34, 3]
group2 = [12, 6, 34, 8]
group3 = [12, 4, 34, 5]
all_channels = [38, 10, 22, 22]
off = [38, 0, 15, 15]
boot = [11, 26, 26, 39]
error = [38, 14, 28, 28]
stop = [29, 39, 0, 27]
run = [38, 28, 40, 24]
standby = [29, 39, 11, 32]
update = [30, 27, 13, 39]
extended = [41, 41, 41, 41]
ready = [38, 28, 13, 32]


def disable_colon(on):
    display.show_doublepoint(not on)
    return


def show_duration(duration):
    disable_colon(True)
    display.show_int(duration)
    return


def show_ready():
    disable_colon(True)
    display.show(ready)
    return


def show_extended():
    disable_colon(True)
    display.show(extended)
    return


def show_update():
    disable_colon(True)
    display.show(update)
    return


def show_standby():
    disable_colon(True)
    display.show(standby)
    return


def show_run():
    disable_colon(True)
    display.show(run)
    return


def show_stop():
    disable_colon(True)
    display.show(stop)
    return


def show_error():
    disable_colon(True)
    display.show(error)
    return


def show_core_temp():
    disable_colon(True)
    display.show(core_temp.get_temp_as_digits())
    return


def blink(values, pulse):
    for i in range(0, pulse):
        display.show(values)
        sleep(0.3)
        display.clear()
        sleep(0.1)
    return


def show_channel(channel):
    disable_colon(True)
    display.show([12, 17, 38, channel])
    return


def show_group(group):
    disable_colon(True)
    if group == 1:
        display.show(group1)
    elif group == 2:
        display.show(group2)
    elif group == 3:
        display.show(group3)
    elif group == 0:
        display.show(all_channels)
    else:
        display.clear()
    return


def show_off():
    disable_colon(True)
    display.show(off)
    return


def show_boot():
    disable_colon(True)
    display.show(boot)
    return
