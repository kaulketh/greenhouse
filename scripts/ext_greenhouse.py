#!/usr/bin/python
# -*- coding: utf-8 -*-
# script for panic mode
# author: Thomas Kaulke

import greenhouse_config as conf
import ext_greenhouse_lib as lib

import sys
import time
import telepot
import os
import commands
import subprocess
import tempfile
import os
import logging

logging.basicConfig(filename=conf.log_file, format=conf.log_format,
                    datefmt=conf.log_date_format, level=logging.INFO)

# def board pins/channels, refer hardware/rspi_gpio.info
relais01 = conf.RELAIS_01
relais02 = conf.RELAIS_02
relais03 = conf.RELAIS_03
relais04 = conf.RELAIS_04
relais05 = conf.RELAIS_05
relais06 = conf.RELAIS_06
relais07 = conf.RELAIS_07
relais08 = conf.RELAIS_08

group_all = (relais01, relais02, relais03, relais04,
             relais05, relais06, relais07, relais08)
group_one = (relais01, relais02, relais03)
group_two = (relais06, relais07, relais08)
group_three = (relais04, relais05)

#API token and chat Id
apiToken = conf.token
Id = sys.argv[1]

# time stamp
def timestamp():
    return conf.getTimestamp()

# live stream address
live = conf.live

#check GPIO state and log       
def checkGpioState():
    os.system(conf.run_gpio_check)
    return

def stopGpioCheck():
    os.system(conf.stop_gpio_check)
    return


# water a group of targets
def water_on_group(group):
    checkGpioState()
    for member in group:
        conf.switch_on(member)
    stopGpioCheck()
    return

# water off for a  group of targets
def water_off_group(group):
    checkGpioState()
    for member in group:
        conf.switch_off(member)
    stopGpioCheck() 
    return

# Assign default output (stdout 1 and stderr 2) to file and read in
# variable and get back
def readcmd(cmd):
    os.system(cmd + ' > ' + lib.tmp_file + ' 2>&1')
    data = ""
    file = open(lib.tmp_file, 'r')
    data = file.read()
    file.close()
    return data

# kill the still running greenhouse bot script
PID1 = readcmd(lib.get_pid1)
logging.info(str(PID1)+' is PID of running default bot, use to kill.')
readcmd('kill -9 ' + PID1)

def sendmsg(message):
    os.system('curl -s -k https://api.telegram.org/bot' + apiToken +
              '/sendMessage -d text="' + message + '" -d chat_id=' + str(Id))
    logging.info('Message send: ' + message)
    return

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    logging.info('Got command: %s' % command)

    # commands
    if command == lib.cmd_restart:
        sendmsg(readcmd('sudo reboot'))
    elif command == lib.cmd_update:
        readcmd(lib.update_bot)
        sendmsg(lib.msg_update)
    elif command == lib.cmd_logrotate:
        sendmsg(readcmd(lib.logrotate_bot))
    elif command == lib.cmd_all_on:
        sendmsg(timestamp() + ' all on')
        water_on_group(group_all)
    elif command == lib.cmd_all_off:
        sendmsg('all off.')
        water_off_group(group_all)
    elif command == lib.cmd_group1_on:
        sendmsg(timestamp() + 'group 1 on')
        water_on_group(group_one)
    elif command == lib.cmd_group1_off:
        sendmsg('group 1 off')
        water_off_group(group_one)
    elif command == lib.cmd_group2_on:
        sendmsg(timestamp() + 'group 2  on')
        water_on_group(group_two)
    elif command == lib.cmd_group2_off:
        sendmsg('group 2 off')
        water_off_group(group_two)
    elif command == lib.cmd_group3_on:
        sendmsg(timestamp() + 'group 3 on')
        water_on_group(group_three)
    elif command == lib.cmd_group3_off:
        sendmsg('group 3 off')
        water_off_group(group_three)
    elif command == lib.cmd_kill:
        #disable camera
        logging.info('Disable camera module.')
        readcmd(conf.disable_camera)
        # clear monitor directory
        logging.info('Clear monitor folder.')
        readcmd(lib.clear_monitor)
        PID2 = readcmd(lib.get_pid2)
        logging.info('got own PID to kill me by myself and also prepare the other bot for proper using:'+str(PID2))
        readcmd(lib.restart_bot)
        sendmsg('Process killed! Enable default bot... Run with /start')
        readcmd('kill -9 ' + PID2)
    elif command == '/start':
        sendmsg('External input possible, bot is ready to use!')
    elif command == '/live':
        sendmsg(live)
    elif command == '/help':
        sendmsg(lib.msg_help)
    else:
        sendmsg(lib.msg_unknown)

conf.resetPins()
bot = telepot.Bot(apiToken)
bot.message_loop(handle)
logging.info('I am listening...')


while 1:
    try:
        time.sleep(10)

    except KeyboardInterrupt:
        logging.warning('Program interrupted')
        exit()

    except:
        logging.error('Other error or exception occured!')
