
#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke

from subprocess import Popen,PIPE,STDOUT,call

import greenhouse_config as config

import os
import commands
import time
import RPi.GPIO as GPIO
import logging

logging.basicConfig(filename=config.log_file, format=config.log_format,
                    datefmt=config.log_date_format, level=logging.INFO)

gpios = (21, 22, 23, 24, 25, 27, 28, 29)


def getState(pin):
        proc=Popen('gpio read '+str(pin), shell=True,stdout=PIPE,)
        output=proc.communicate()[0]
        return output


while 1:
    for pin in gpios:
        index = gpios.index(pin)
        state = int(getState(pin))
        if state == 0:
                logging.info('GPIO.'+str(pin)+':'+str(state)+' -> Valve open at pin '+str(config.GROUP_ALL[index])+'!')
    try:
        time.sleep(1)

    except KeyboardInterrupt:
        logging.warning('Check interrupted')
        exit()
    except:
        logging.error('Other error or exception occured!')

