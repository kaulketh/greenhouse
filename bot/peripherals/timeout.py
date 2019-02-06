#!/usr/bin/python
# -*- coding: utf-8 -*-
# script for "panic" mode - extended bot
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import os, sys, logging, time
import conf.greenhouse_config as conf
import conf.ext_greenhouse_lib as lib
import peripherals.four_digit.display as display


logging.basicConfig(filename=conf.log_file, format=conf.log_format,
                    datefmt=conf.log_date_format, level=logging.INFO)

# API token and chat Id
token = conf.token
chat_id = conf.mainId


def read_cmd(cmd):
    os.system(cmd + ' > ' + lib.tmp_file + ' 2>&1')
    file = open(lib.tmp_file, 'r')
    data = file.read()
    file.close()
    return data


def send_msg(message):
    os.system(
        'curl -s -k https://api.telegram.org/bot{0}/sendMessage -d text="{1}" -d chat_id={2} '
        'parse_mode=\'Markdown\' reply_markup=\'remove_keyboard\''.format(token, message, str(chat_id)))
    logging.info('Message send: {0}'.format(message))
    return


def timeout_reached():
    logging.info('Timeout reached, bot in standby.')
    read_cmd(conf.disable_camera)
    display.show_stop()
    time.sleep(2)
    send_msg(lib.msg_stop.format)
    display.show_standby()
    # kill the still running greenhouse bot script
    pid1 = read_cmd(lib.get_pid1)
    # logging.info('{0} is PID of running default bot, used to kill.'.format(str(pid1)))
    read_cmd('kill -9 {0}'.format(str(pid1)))
    return


if __name__ == '__main__':
    timeout_reached()
