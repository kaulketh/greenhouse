#!/usr/bin/python
# -*- coding: utf-8 -*-
# script for "panic" mode - extended bot
# author: Thomas Kaulke, kaulketh@gmail.com

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

# def board pins/channels, refer hardware/raspi_gpio.info
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

# API token and chat Id
apiToken = conf.token
Id = sys.argv[1]


# water a group of targets
def water_on_group(group):
    for member in group:
        conf.switch_on(member)
    return


# water off for a  group of targets
def water_off_group(group):
    for member in group:
        conf.switch_off(member)
    return


# Assign default output (stdout 1 and stderr 2) to file and read in
# variable and get back
def read_cmd(cmd):
    os.system(cmd + ' > ' + lib.tmp_file + ' 2>&1')
    file = open(lib.tmp_file, 'r')
    data = file.read()
    file.close()
    return data


# kill the still running greenhouse bot script
pid1 = read_cmd(lib.get_pid1)
logging.info('{0} is PID of running default bot, use to kill.'.format(str(pid1)))
read_cmd('kill -9 {0}'.format(str(pid1)))


def send_msg(message):
    os.system('curl -s -k https://api.telegram.org/bot{0}/sendMessage -d text="{1}" -d chat_id={2}'
              .format(apiToken, message, str(Id)))
    logging.info('Message send: {0}'.format(message))
    return


def handle(msg):
    command = msg['text']

    logging.info('Got command: %s' % command)

    # commands
    if command == lib.cmd_restart:
        send_msg(read_cmd('sudo reboot'))
    elif command == lib.cmd_update:
        read_cmd(lib.update_bot)
        send_msg(lib.msg_update)
    elif command == lib.cmd_logrotate:
        send_msg(read_cmd(lib.logrotate_bot))
    elif command == lib.cmd_all_on:
        send_msg(conf.get_timestamp() + ' all on')
        water_on_group(group_all)
    elif command == lib.cmd_all_off:
        send_msg('all off.')
        water_off_group(group_all)
    elif command == lib.cmd_group1_on:
        send_msg(conf.get_timestamp() + 'group 1 on')
        water_on_group(group_one)
    elif command == lib.cmd_group1_off:
        send_msg('group 1 off')
        water_off_group(group_one)
    elif command == lib.cmd_group2_on:
        send_msg(conf.get_timestamp() + 'group 2  on')
        water_on_group(group_two)
    elif command == lib.cmd_group2_off:
        send_msg('group 2 off')
        water_off_group(group_two)
    elif command == lib.cmd_group3_on:
        send_msg(conf.get_timestamp() + 'group 3 on')
        water_on_group(group_three)
    elif command == lib.cmd_group3_off:
        send_msg('group 3 off')
        water_off_group(group_three)
    elif command == lib.cmd_kill:
        # disable camera
        logging.info('Disable camera module.')
        read_cmd(conf.disable_camera)
        pid2 = read_cmd(lib.get_pid2)
        logging.info('got own PID to kill me by myself and also prepare the other bot for proper using:{0}'
                     .format(str(pid2)))
        read_cmd(lib.restart_bot)
        send_msg('Process killed! Enable default bot... Run with /start')
        read_cmd('kill -9 ' + pid2)
    elif command == '/start':
        send_msg('Extended input possible, bot is ready to use!')
    elif command == '/live':
        send_msg(conf.live)
    elif command == '/help':
        send_msg(lib.msg_help)
    else:
        send_msg(lib.msg_unknown)


conf.reset_pins()
bot = telepot.Bot(apiToken)
bot.message_loop(handle)
logging.info('I am listening...')


while 1:
    try:
        time.sleep(10)

    except KeyboardInterrupt:
        logging.warning('Program interrupted')
        exit()
