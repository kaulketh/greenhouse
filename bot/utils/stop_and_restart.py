#!/usr/bin/python
# -*- coding: utf-8 -*-
# stop_and_restart.py
"""
Kill running process after given time and reply message
author: Thomas Kaulke, kaulketh@gmail.com
"""

from __future__ import absolute_import
from telegram import (ReplyKeyboardRemove, ParseMode)
import time
import conf.lib_ext_greenhouse as lib
import conf.greenhouse_config as conf
import peripherals.four_digit.display as display
import logger.logger as log
import utils.utils as utils

logging = log.get_logger()

# API token and chat Id
token = conf.token
chat_id = conf.mainId


def stop_and_restart(update):
    logging.info('Stop and restart - set to standby.')
    utils.read_cmd(conf.disable_camera, lib.tmp_file)
    display.show_stop()
    time.sleep(2)
    """ start new new instance of greenhouse """
    utils.read_cmd(lib.restart_bot, lib.tmp_file)
    update.message.reply_text(conf.lib.msg_stop, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    display.show_standby()
    """ kill the current instance of greenhouse bot """
    pid1 = utils.read_cmd(lib.get_pid1, lib.tmp_file)
    utils.read_cmd('kill -9 {0}'.format(str(pid1)), lib.tmp_file)
    return


if __name__ == '__main__':
    pass
