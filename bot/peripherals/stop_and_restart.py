#!/usr/bin/python
# -*- coding: utf-8 -*-
# Timeout: Kill running process after given time and sends a message
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
from telegram import (ReplyKeyboardRemove, ParseMode)
import os
import time
import conf.ext_greenhouse_lib as lib
import conf.greenhouse_config as conf
import peripherals.four_digit.display as display
import logger.logger as log

logging = log.get_logger()

# API token and chat Id
token = conf.token
chat_id = conf.mainId


def _read_cmd(cmd):
    os.system(cmd + ' > ' + lib.tmp_file + ' 2>&1')
    file = open(lib.tmp_file, 'r')
    data = file.read()
    file.close()
    return data


def stop_and_restart(update):
    logging.warning('Timeout reached, set bot in standby.')
    _read_cmd(conf.disable_camera)
    display.show_stop()
    time.sleep(2)
    # start new new instance of greenhouse
    _read_cmd(lib.restart_bot)
    update.message.reply_text(conf.lib.msg_stop, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    display.show_standby()
    # kill the current instance of greenhouse bot
    pid1 = _read_cmd(lib.get_pid1)
    _read_cmd('kill -9 {0}'.format(str(pid1)))
    return


if __name__ == '__main__':
    pass
