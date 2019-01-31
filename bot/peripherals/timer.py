#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import conf.greenhouse_config as config
import threading
import logging


logging.basicConfig(filename=config.log_file, format=config.log_format,
                    datefmt=config.log_date_format, level=logging.INFO)

seconds_steps = config.lib.time_units_conversion
t = None
wait = 15


def switch_to_standby(bot):
    global t
    global wait
    t = threading.Timer(wait, bot.stop())
    t.start()
    logging.info("switched to standby automatically")


if __name__ == '__main__':
    pass
