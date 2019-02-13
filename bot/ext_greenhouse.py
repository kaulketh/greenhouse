#!/usr/bin/python
# -*- coding: utf-8 -*-
# ext_greenhouse.py
"""
script for "panic" mode - extended bot
using telepot as Python framework for Telegram Bot API
https://telepot.readthedocs.io/en/latest/reference.html
author: Thomas Kaulke, kaulketh@gmail.com
"""

from __future__ import absolute_import
import conf.greenhouse_config as conf
import conf.lib_ext_greenhouse as lib
import utils.utils as utils
import peripherals.four_digit.display as display
import sys
import time
import telepot
import os
import logger.logger as log

logging = log.get_logger()

pins_state = False

markdown = "-d parse_mode='Markdown'"
no_parse_mode = conf.lib.empty

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


# water a group of targets
def __water_on_group(group):
    for member in group:
        utils.switch_on(member)
    return


# water off for a  group of targets
def __water_off_group(group):
    for member in group:
        utils.switch_off(member)
    return


def __send_msg(message, parse_mode):
    os.system(
        'curl -s -k https://api.telegram.org/bot{0}/sendMessage -d text="{1}" -d chat_id={2} {3}'.format(
            apiToken, message.replace("`", "\\`"), str(chat_id), parse_mode))
    logging.info('Message send: {0}'.format(message))
    return


def __check_pins_state():
    global pins_state
    for pin in group_all:
        if not utils.get_pin_state(pin):
            display.show_on()
            pins_state = False
            break
        else:
            display.show_off()
            pins_state = True

    if not pins_state:
        __send_msg('Attention, something is still opened!', no_parse_mode)
    return


def __handle(msg):
    if pins_state:
        display.show_extended()

    command = msg['text']
    logging.info('Got command: %s' % command)

    # commands
    if command == lib.cmd_restart:
        __send_msg(utils.read_cmd('sudo reboot', lib.tmp_file), no_parse_mode)
        display.show_boot()
    elif command == lib.cmd_update:
        utils.read_cmd(lib.update_bot, lib.tmp_file)
        __send_msg(lib.msg_update, no_parse_mode)
        display.show_update()
        time.sleep(3)
    elif command == lib.cmd_logrotate:
        __send_msg(utils.read_cmd(lib.logrotate_bot, lib.tmp_file), no_parse_mode)
    elif command == lib.cmd_all_on:
        __send_msg(utils.get_timestamp() + ' all on', no_parse_mode)
        __water_on_group(group_all)
    elif command == lib.cmd_all_off:
        __send_msg('all off.', no_parse_mode)
        __water_off_group(group_all)
    elif command == lib.cmd_group1_on:
        __send_msg(utils.get_timestamp() + 'group 1 on', no_parse_mode)
        __water_on_group(group_one)
    elif command == lib.cmd_group1_off:
        __send_msg('group 1 off', no_parse_mode)
        __water_off_group(group_one)
    elif command == lib.cmd_group2_on:
        __send_msg(utils.get_timestamp() + 'group 2  on', no_parse_mode)
        __water_on_group(group_two)
    elif command == lib.cmd_group2_off:
        __send_msg('group 2 off', no_parse_mode)
        __water_off_group(group_two)
    elif command == lib.cmd_group3_on:
        __send_msg(utils.get_timestamp() + 'group 3 on', no_parse_mode)
        __water_on_group(group_three)
    elif command == lib.cmd_group3_off:
        __send_msg('group 3 off', no_parse_mode)
        __water_off_group(group_three)
    elif command == lib.cmd_kill:
        # disable camera
        logging.info('Disable camera module.')
        utils.read_cmd(conf.disable_camera, lib.tmp_file)
        pid2 = utils.read_cmd(lib.get_pid2, lib.tmp_file)
        utils.read_cmd(lib.restart_bot, lib.tmp_file)
        __send_msg(conf.lib.msg_stop, markdown)
        utils.read_cmd('kill -9 ' + pid2, lib.tmp_file)
    elif command == '/live':
        __send_msg(conf.lib.msg_live.format(conf.live), markdown)
    elif command == '/help':
        __send_msg(lib.msg_help, no_parse_mode)
    else:
        __send_msg(lib.msg_unknown, no_parse_mode)
    __check_pins_state()


def __init_and_start():
    # API token and chat Id
    global apiToken, chat_id
    apiToken = conf.token
    chat_id = sys.argv[1]

   # kill the still running greenhouse bot script.
    pid1 = utils.read_cmd(lib.get_pid1, lib.tmp_file)
    utils.read_cmd('kill -9 {0}'.format(str(pid1)), lib.tmp_file)

    utils.set_pins()
    bot = telepot.Bot(apiToken)
    bot.message_loop(__handle)
    logging.info('I am listening...')
    display.show_extended()
    while 1:
        try:
            time.sleep(5)

        except KeyboardInterrupt:
            logging.warning('Program interrupted')
            display.show_error()
            exit()

        except Exception:
            logging.warning('Any error occurs')
            display.show_error()


if __name__ == '__main__':
    __init_and_start()
