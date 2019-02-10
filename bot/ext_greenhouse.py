#!/usr/bin/python
# -*- coding: utf-8 -*-
# script for "panic" mode - extended bot
# using telepot as Python framework for Telegram Bot API
# https://telepot.readthedocs.io/en/latest/reference.html
# author: Thomas Kaulke, kaulketh@gmail.com


from __future__ import absolute_import
import conf.greenhouse_config as conf
import conf.ext_greenhouse_lib as lib
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

# API token and chat Id
apiToken = conf.token
Id = sys.argv[1]


# water a group of targets
def _water_on_group(group):
    for member in group:
        utils.switch_on(member)
    return


# water off for a  group of targets
def _water_off_group(group):
    for member in group:
        utils.switch_off(member)
    return


# Assign default output (stdout 1 and stderr 2) to file and read in
# variable and get back
def _read_cmd(cmd):
    os.system(cmd + ' > ' + lib.tmp_file + ' 2>&1')
    file = open(lib.tmp_file, 'r')
    data = file.read()
    file.close()
    return data


def _send_msg(message, parse_mode):
    os.system(
        'curl -s -k https://api.telegram.org/bot{0}/sendMessage -d text="{1}" -d chat_id={2} {3}'.format(
            apiToken, message.replace("`", "\\`"), str(Id), parse_mode))
    logging.info('Message send: {0}'.format(message))
    return


def _check_pins_state():
    global pins_state
    for pin in group_all:
        if not utils.get_pin_state(pin):
            display.show_on()
            pins_state = False
            break
        else:
            display.show_off()
            pins_state = True
    return


def _handle(msg):
    if pins_state:
        display.show_extended()

    command = msg['text']
    logging.info('Got command: %s' % command)

    # commands
    if command == lib.cmd_restart:
        _send_msg(_read_cmd('sudo reboot'), no_parse_mode)
        display.show_boot()
    elif command == lib.cmd_update:
        _read_cmd(lib.update_bot)
        _send_msg(lib.msg_update, no_parse_mode)
        display.show_update()
        time.sleep(3)
    elif command == lib.cmd_logrotate:
        _send_msg(_read_cmd(lib.logrotate_bot), no_parse_mode)
    elif command == lib.cmd_all_on:
        _send_msg(utils.get_timestamp() + ' all on', no_parse_mode)
        _water_on_group(group_all)
    elif command == lib.cmd_all_off:
        _send_msg('all off.', no_parse_mode)
        _water_off_group(group_all)
    elif command == lib.cmd_group1_on:
        _send_msg(utils.get_timestamp() + 'group 1 on', no_parse_mode)
        _water_on_group(group_one)
    elif command == lib.cmd_group1_off:
        _send_msg('group 1 off', no_parse_mode)
        _water_off_group(group_one)
    elif command == lib.cmd_group2_on:
        _send_msg(utils.get_timestamp() + 'group 2  on', no_parse_mode)
        _water_on_group(group_two)
    elif command == lib.cmd_group2_off:
        _send_msg('group 2 off', no_parse_mode)
        _water_off_group(group_two)
    elif command == lib.cmd_group3_on:
        _send_msg(conf.get_timestamp() + 'group 3 on', no_parse_mode)
        _water_on_group(group_three)
    elif command == lib.cmd_group3_off:
        _send_msg('group 3 off', no_parse_mode)
        _water_off_group(group_three)
    elif command == lib.cmd_kill:
        # disable camera
        logging.info('Disable camera module.')
        _read_cmd(utils.disable_camera)
        pid2 = _read_cmd(lib.get_pid2)
        # logging.info('Got own PID to kill me and prepare the other bot for proper using: {0}'.format(str(pid2)))
        _read_cmd(lib.restart_bot)
        _send_msg(conf.lib.msg_stop, markdown)
        _read_cmd('kill -9 ' + pid2)
    elif command == '/live':
        _send_msg(conf.lib.msg_live.format(conf.live), markdown)
    elif command == '/help':
        _send_msg(lib.msg_help, no_parse_mode)
    else:
        _send_msg(lib.msg_unknown, no_parse_mode)
    _check_pins_state()


def init_and_start():
    # kill the still running greenhouse bot script
    pid1 = _read_cmd(lib.get_pid1)
    # logging.info('{0} is PID of running default bot, used to kill.'.format(str(pid1)))
    _read_cmd('kill -9 {0}'.format(str(pid1)))

    utils.set_pins()
    bot = telepot.Bot(apiToken)
    bot.message_loop(_handle)
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


init_and_start()

if __name__ == '__main__':
    pass
