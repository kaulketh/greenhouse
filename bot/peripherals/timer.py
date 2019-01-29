#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
# import conf.greenhouse_config as config
import threading
import time
# import sys
# import logging

# logging.basicConfig(filename=config.log_file, format=config.log_format,
#                    datefmt=config.log_date_format, level=logging.INFO)

count = 5
i = count
seconds_steps = 1
# count = sys.argv[1]
# seconds_steps = sys.argv[2]


def downwards():
    global t
    global count
    global seconds_steps
    # logging.info("counter :" + str(count))
    print(time.strftime('[%d.%m.%Y %H:%M:%S]') + " counter : " + str(count))
    count -= 1
    if count > 0:
        t = threading.Timer(seconds_steps, downwards)
        t.start()
    else:
        t.cancel()
        print("finished")





def upwards():
    global t
    global count
    global seconds_steps
    # logging.info("counter :" + str(count))
    count -= 1
    if count >= 0:
        print(time.strftime('[%d.%m.%Y %H:%M:%S]') + " counter : " + str(i-count))
        t = threading.Timer(seconds_steps, upwards)
        t.start()
    else:
        t.cancel()
        print("finished")


#downwards()
upwards()

