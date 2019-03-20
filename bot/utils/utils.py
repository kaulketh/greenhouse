#!/usr/bin/python
# -*- coding: utf-8 -*-
# utils.py

"""
useful methods
author: Thomas Kaulke, kaulketh@gmail.com
"""

from __future__ import absolute_import
import conf
import time
import os
import RPi.GPIO as GPIO
import logger

logger = logger.get_logger()


# switch functions
def switch_on(pin):
    logger.info('switch relay on: ' + str(pin))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    # os.system(run_gpio_check + str(pin))
    return


def switch_off(pin):
    logger.info('switch relay off: ' + str(pin))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    # os.system(run_gpio_check + str(pin))
    GPIO.cleanup(pin)
    return


def switch_out_high(pin):
    logger.info('switch {} OUT HIGH'.format(str(pin)))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    return


def switch_out_low(pin):
    logger.info('switch {} OUT LOW'.format(str(pin)))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    return


# date time strings
def get_timestamp():
    return time.strftime('[%d.%m.%Y %H:%M:%S] ')


def get_timestamp_line():
    return time.strftime('`[%d.%m.%Y %H:%M:%S]\n---------------------\n`')


# gets the state of pin, if 0 is switched to LOW
def get_pin_state(pin):
    GPIO.setup(pin, GPIO.OUT)
    return GPIO.input(pin)


# to use Raspberry Pi board pin numbers
def set_pins():
    GPIO.setmode(GPIO.BOARD)
    logger.info('Set GPIO mode: GPIO.BOARD')
    # to use GPIO instead board pin numbers, then please adapt pin definition
    # GPIO.setmode(GPIO.BCM)
    # comment if warnings required
    GPIO.setwarnings(False)
    return GPIO


# Execute bash command, assign default output (stdout 1 and stderr 2) to file, read in variable and get back
def read_cmd(cmd, tmp_file):
    os.system(cmd + ' > ' + tmp_file + ' 2>&1')
    file = open(tmp_file, 'r')
    data = file.read()
    file.close()
    return data


# Provide release version information
def get_release():
    try:
        release = open(str(conf.latest_release)).read()
        if release is None:
            release = '-----'
        else:
            release = release.replace("\n", "")
    except Exception:
        release = '-----'
        return release
    return release


def get_last_commit():
    try:
        commit = open(str(conf.commit_id)).read()
        if commit is None:
            commit = '-------'
        else:
            commit = commit[0:7]
        branch = open(str(conf.cloned_branch)).read()
        if branch is None:
            branch = '-------'
        else:
            branch = branch.replace("\n", "")
    except Exception:
        build = '---ERROR---'
        return build

    build = commit + " " + branch
    return build


def get_release_info():
    return conf.application_name + conf.space + get_release() + ' Build:' + get_last_commit()


if __name__ == '__main__':
    pass
