#!/usr/bin/python
# -*- coding: utf-8 -*-
# main script for greenhouse bot
# using telegram.ext as Python framework for Telegram Bot API
# https://core.telegram.org/api#bot-api
# original: author: Stefan Weigert  http://www.stefan-weigert.de/php_loader/raspi.php
# adapted: author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import os
import time
import utils.utils as utils
import conf.greenhouse_config as conf
import peripherals.dht.dht as dht
import peripherals.temperature as core
import utils.stop_and_restart as stop_and_restart
import peripherals.four_digit.display as display
import logger.logger as log

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler
from telegram.ext.dispatcher import run_async

logging = log.get_logger()

# used library
lib = conf.lib

# define pins
all_groups = conf.GROUP_ALL
group_one = conf.GROUP_01
group_two = conf.GROUP_02
group_three = conf.GROUP_03

# api and bot settings
SELECTION, DURATION = range(2)
# LIST_OF_ADMINS = ['mock to test']
list_of_admins = conf.admins
token = conf.token
target = lib.empty
water_time = lib.empty
user_id = lib.empty
jq = None
timer_job = None


# keyboard config
markup1 = ReplyKeyboardMarkup(conf.kb1, resize_keyboard=True, one_time_keyboard=False)
markup2 = ReplyKeyboardMarkup(conf.kb2, resize_keyboard=True, one_time_keyboard=False)
markup3 = ReplyKeyboardMarkup(conf.kb3, resize_keyboard=True, one_time_keyboard=True)


# Start info
def __init_bot_set_pins():
    logging.info('Initialize bot, setup GPIO pins.')
    utils.set_pins()
    logging.info('Switch all off at start.')
    __all_off()
    display.show_standby()
    return


# start bot
def __start(bot, update):
    global user_id

    try:
        user_id = update.message.from_user.id
    except (NameError, AttributeError):
        try:
            user_id = update.inline_query.from_user.id
        except (NameError, AttributeError):
            try:
                user_id = update.chosen_inline_result.from_user.id
            except (NameError, AttributeError):
                try:
                    user_id = update.callback_query.from_user.id
                except (NameError, AttributeError):
                    return ConversationHandler.END

    if user_id not in list_of_admins:
        display.show_stop()
        logging.info('Not allowed access by: {0} - {1},{2}'.format(
            str(user_id), update.message.from_user.last_name, update.message.from_user.first_name))
        update.message.reply_text(lib.private_warning.format(
            update.message.from_user.first_name, update.message.chat_id), parse_mode=ParseMode.MARKDOWN)
        return ConversationHandler.END
    else:
        display.show_run()
        logging.info('Bot started.')
        __message_values(update)
        __cam_on()
        display.show_ready()
        update.message.reply_text('{0}{1}{2}'.format(
            lib.msg_welcome.format(update.message.from_user.first_name), lib.line_break, lib.msg_choice),
            parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        logging.info('Bot is using by: {0} - {1},{2}'.format(
            str(user_id), update.message.from_user.last_name, update.message.from_user.first_name))
        logging.info('Time unit is \'{0}\''.format(str(lib.time_units_name[lib.time_units_index])))
        display.show_off()

        __start_standby_timer(bot, update)
        return SELECTION


# set the target, member of group or group
def __selection(bot, update):
    global target
    target = update.message.text

    __stop_standby_timer(bot, update)

    if target == str(lib.panic):
        update.message.reply_text(lib.msg_panic,
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        logging.info(lib.msg_panic)
        os.system(conf.run_extended_greenhouse + str(user_id))

    elif target == str(lib.live_stream):
        logging.info('Live URL requested.')
        update.message.reply_text(lib.msg_live.format(str(conf.live)), parse_mode=ParseMode.MARKDOWN)
        __start_standby_timer(bot, update)
        return SELECTION

    elif target == str(lib.reload):
        logging.info('Refresh values requested.')
        __message_values(update)
        __start_standby_timer(bot, update)
        return SELECTION

    else:
        update.message.reply_text(lib.msg_duration.format(target),
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=markup2)
        logging.info('Selection: {0}'.format(str(target)))

        __start_standby_timer(bot, update)
        return DURATION


# set water duration
def __duration(bot, update):
    global water_time
    global g_duration_update
    g_duration_update = update
    water_time = update.message.text

    __stop_standby_timer(bot, update)

    if water_time == str(lib.cancel):
        update.message.reply_text(lib.msg_new_choice,
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        logging.info(lib.msg_new_choice)

    elif water_time == str(lib.panic):
        update.message.reply_text(lib.msg_panic,
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        logging.info(lib.msg_panic)
        os.system(conf.run_extended_greenhouse + str(user_id))

    elif target == str(lib.group1[1]):
        """ starts separate thread"""
        display.show_switch_channel_duration(1, int(water_time))

        __water(bot, update, group_one[0])

    elif target == str(lib.group1[2]):
        """ starts separate thread"""
        display.show_switch_channel_duration(2, int(water_time))

        __water(bot, update, group_one[1])

    elif target == str(lib.group1[3]):
        """ starts separate thread"""
        display.show_switch_channel_duration(3, int(water_time))

        __water(bot, update, group_one[2])

    elif target == str(lib.group2[1]):
        """ starts separate thread"""
        display.show_switch_channel_duration(6, int(water_time))

        __water(bot, update, group_two[0])

    elif target == str(lib.group2[2]):
        """ starts separate thread"""
        display.show_switch_channel_duration(7, int(water_time))

        __water(bot, update, group_two[1])

    elif target == str(lib.group2[3]):
        """ starts separate thread"""
        display.show_switch_channel_duration(8, int(water_time))

        __water(bot, update, group_two[2])

    elif target == str(lib.group1[0]):
        """ starts separate thread"""
        display.show_switch_group_duration(1, int(water_time))

        __water_group(bot, update, group_one)

    elif target == str(lib.group2[0]):
        """ starts separate thread"""
        display.show_switch_group_duration(2, int(water_time))

        __water_group(bot, update, group_two)

    elif target == str(lib.group3[1]):
        """ starts separate thread"""
        display.show_switch_channel_duration(4, int(water_time))

        __water(bot, update, group_three[0])

    elif target == str(lib.group3[2]):
        """ starts separate thread"""
        display.show_switch_channel_duration(5, int(water_time))

        __water(bot, update, group_three[1])

    elif target == str(lib.group3[0]):
        """ starts separate thread"""
        display.show_switch_group_duration(3, int(water_time))

        __water_group(bot, update, group_three)

    elif target == str(lib.all_channels):
        __water_all(bot, update)

    else:
        update.message.reply_text(lib.msg_choice, reply_markup=markup1)

    __start_standby_timer(bot, update)
    return SELECTION


# watering targets
def __all_off():
    logging.info('Switch all off.')
    for channel in all_groups:
        utils.switch_off(channel)
    return


@run_async
def __water_all(bot, update):
    logging.info('Duration: {0}'.format(water_time))
    update.message.reply_text(lib.water_on_all.format(target, water_time),
                              parse_mode=ParseMode.MARKDOWN, reply_markup=markup3)

    """ starts separate thread"""
    display.show_switch_group_duration(0, int(water_time))

    for channel in all_groups:
        utils.switch_on(channel)
    time.sleep(int(water_time) * int(lib.time_conversion))
    __all_off()

    update.message.reply_text('{0}{1}{2}'.format(
        __timestamp(), lib.water_off_all.format(water_time), lib.msg_new_choice),
        parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    display.show_off()
    return


@run_async
def __water(bot, update, channel):
    logging.info('Duration: ' + water_time)
    logging.info('Toggle ' + str(channel))
    update.message.reply_text(lib.water_on.format(target, water_time),
                              parse_mode=ParseMode.MARKDOWN, reply_markup=markup3)

    utils.switch_on(channel)
    time.sleep(int(water_time) * int(lib.time_conversion))
    utils.switch_off(channel)

    update.message.reply_text('{0}{1}{2}'.format(
        __timestamp(), lib.water_off.format(target, water_time), lib.msg_new_choice),
        parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    display.show_off()
    return


@run_async
def __water_group(bot, update, group):
    logging.info('Duration: ' + water_time)
    logging.info('Toggle ' + str(group))
    update.message.reply_text(lib.water_on_group.format(target, water_time),
                              parse_mode=ParseMode.MARKDOWN, reply_markup=markup3)

    for channel in group:
        utils.switch_on(channel)
    time.sleep((int(water_time) * int(lib.time_conversion)))
    for channel in group:
        utils.switch_off(channel)
    update.message.reply_text('{0}{1}{2}'.format(
        __timestamp(), lib.water_off_group.format(target, water_time), lib.msg_new_choice),
        parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    display.show_off()
    return


# humidity and temperature
def __message_values(update):
    # to avoid refresh intervals shorter than 3 seconds
    time.sleep(3)
    dht.get_values()
    if dht.temperature == 0:
        temp = (lib.temp + lib.colon_space + '------')
    else:
        temp = (lib.temp + lib.colon_space + conf.temp_format).format(dht.temperature)

    if dht.humidity == 0:
        hum = (lib.hum + lib.colon_space + '------')
    else:
        hum = (lib.hum + lib.colon_space + conf.hum_format).format(dht.humidity)

    core_temp = (lib.core + lib.colon_space + core.get_temperature())
    update.message.reply_text(lib.msg_temperature.format(
        __start_time(), temp, hum, core_temp), parse_mode=ParseMode.MARKDOWN)
    return


# stop bot
def __stop(bot, update):
    global enable_emergency_stop
    enable_emergency_stop = False
    __all_off()
    __stop_standby_timer(bot, update)
    logging.info('Bot stopped.')
    __cam_off()
    display.show_stop()
    update.message.reply_text(lib.msg_stop, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    time.sleep(2)
    display.show_standby()
    return ConversationHandler.END


# emergency stop
@run_async
def __emergency_stop_handler(bot, update, chat_data):
    emergency = update.message.text
    if not emergency:
        return
    if emergency == lib.emergency_stop:
        __all_off()
        __start_emergency_stop(bot, g_duration_update)


def __start_emergency_stop(bot, update):
    global emergency_job
    emergency_job = jq.run_once(__job_stop_and_restart, 0, context=update)
    logging.info("Initialize emergency stop immediately.")
    return


# timer
def __start_standby_timer(bot, update):
    global timer_job
    timer_job = jq.run_once(__job_stop_and_restart, conf.standby_timeout, context=update)
    logging.info("Init standby timer of {0} seconds, added to queue.".format(conf.standby_timeout))
    return


def __stop_standby_timer(bot, upadate):
    timer_job.schedule_removal()
    logging.info("Timer job removed from the queue.")
    return


def __job_stop_and_restart(bot, job):
    logging.warning("Job: Stop and restart called!")
    stop_and_restart.stop_and_restart(job.context)
    return


# error
def __error(bot, update, e):
    logging.error('Update "{0}" caused error "{1}"'.format(update, e))
    display.show_error()
    __cam_off()
    conf.GPIO.cleanup()
    return ConversationHandler.END


# time stamps
def __timestamp():
    return utils.get_timestamp_line()


def __start_time():
    return utils.get_timestamp()


# camera
def __cam_on():
    logging.info('Enable camera module.')
    os.system(conf.enable_camera)
    return


def __cam_off():
    logging.info('Disable camera module.')
    os.system(conf.disable_camera)
    return


def main():
    __init_bot_set_pins()

    global updater
    updater = Updater(token)

    global jq
    jq = updater.job_queue
    logging.info('Init job queue.')

    dp = updater.dispatcher

    emergency_stop_handler = RegexHandler('^{0}$'.format(str(lib.emergency_stop)),
                                          __emergency_stop_handler,
                                          pass_chat_data=True)
    ch = ConversationHandler(
        entry_points=[CommandHandler('start', __start)],
        states={
            SELECTION: [RegexHandler(
                '^({0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10}|{11}|{12}|{13}|{14})$'.format(
                    str(lib.group1[0]),
                    str(lib.group1[1]),
                    str(lib.group1[2]),
                    str(lib.group1[3]),
                    str(lib.group2[0]),
                    str(lib.group2[1]),
                    str(lib.group2[2]),
                    str(lib.group2[3]),
                    str(lib.group3[0]),
                    str(lib.group3[1]),
                    str(lib.group3[2]),
                    str(lib.all_channels),
                    str(lib.panic),
                    str(lib.live_stream),
                    str(lib.reload)), __selection),
                RegexHandler('^{0}$'.format(lib.stop_bot), __stop)],

            DURATION: [RegexHandler('^([0-9]+|{0}|{1})$'.format(str(lib.cancel), str(lib.panic)), __duration),
                       RegexHandler('^{0}$'.format(lib.stop_bot), __stop)]
                },
        fallbacks=[CommandHandler('stop', __stop)]
    )
    dp.add_handler(emergency_stop_handler)

    dp.add_handler(ch)

    dp.add_error_handler(__error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
