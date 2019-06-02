#!/usr/bin/python
# -*- coding: utf-8 -*-
# four.digit.display.py
""""
author: Thomas Kaulke, kaulketh@gmail.com
"""

from __future__ import absolute_import
import threading
from time import sleep
from conf import clk_pin, dio_pin, brightness, lib
import four_digits as tm1637
import peripherals.temperature as core_temp

display = tm1637.TM1637(clk=clk_pin, dio=dio_pin, brightness=brightness)

on = [38, 0, 24, 38]
off = [38, 0, 15, 15]
boot = [11, 26, 26, 39]
err = [38, 14, 28, 28]
stop = [29, 39, 0, 27]
run = [38, 28, 40, 24]
stby = [29, 39, 11, 32]
updt = [30, 27, 13, 39]
pnic = [27, 24, 1, 49]
rdy = [38, 28, 13, 32]
grp = [38, 16, 28, 27]


def show_duration(duration):
    duration = duration * lib.time_conversion
    __disable_colon(True)
    display.show_int(duration)
    return


def show_ready():
    __disable_colon(True)
    display.show(rdy)
    return


def show_extended():
    __disable_colon(True)
    display.show(pnic)
    return


def show_update():
    __disable_colon(True)
    display.show(updt)
    return


def show_standby():
    __disable_colon(True)
    display.show(stby)
    return


def show_run():
    __disable_colon(True)
    display.show(run)
    return


def show_stop():
    __disable_colon(True)
    display.show(stop)
    return


def show_error():
    __disable_colon(True)
    display.show(err)
    return


def show_core_temp():
    __disable_colon(True)
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
    __disable_colon(True)
    display.show([12, 17, 38, channel])
    return


def show_switch_channel_duration(channel, duration):
    duration = duration * lib.time_conversion
    global thread
    global g_channel
    global g_duration
    g_duration = duration
    g_channel = channel
    thread = threading.Thread(target=__switch_channel_duration, args=(g_channel, g_duration), name='switch display')
    thread.start()


def show_group():
    __disable_colon(True)
    display.show(grp)
    return


def show_switch_group_duration(duration):
    duration = duration * lib.time_conversion
    global thread
    global g_duration
    g_duration = duration
    thread = threading.Thread(target=__switch_group_duration, args=(g_duration,), name='switch display')
    thread.start()


def show_off():
    __disable_colon(True)
    display.show(off)
    return


def show_on():
    __disable_colon(True)
    display.show(on)
    return


def show_boot():
    __disable_colon(True)
    display.show(boot)
    return


def __disable_colon(yes):
    display.show_doublepoint(not yes)
    return


def __switch_channel_duration(channel, duration):
    global g_display
    g_display = tm1637.TM1637(clk=clk_pin, dio=dio_pin, brightness=brightness)
    g_display.show_doublepoint(False)
    while duration > 0:
        g_display.show([12, 17, 38, channel])
        sleep(1)
        duration -= 1
        g_display.show_remain_int(duration)
        sleep(1)
        duration -= 1
    return


def __switch_group_duration(duration):
    global g_display
    g_display = tm1637.TM1637(clk=clk_pin, dio=dio_pin, brightness=brightness)
    g_display.show_doublepoint(False)
    while duration > 0:
        g_display.show(grp)
        sleep(1)
        duration -= 1
        g_display.show_remain_int(duration)
        sleep(1)
        duration -= 1
    return


if __name__ == '__main__':
    pass
