#!/usr/bin/python
# -*- coding: utf-8 -*-
# greenhouse.py

"""
 main script for greenhouse bot
 using telegram.ext as Python framework for Telegram Bot API
 https://core.telegram.org/api#bot-api
 original: author: Stefan Weigert  http://www.stefan-weigert.de/php_loader/raspi.php
 adapted: Thomas Kaulke, kaulketh@gmail.com
"""
from __future__ import absolute_import
import os
import time
import utils.utils as utils
import conf
import logger
import peripherals.dht.dht as dht
import peripherals.temperature as core
import utils.stop_and_restart as stop_and_restart
import peripherals.four_digit.display as display

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

logging = logger.get_logger()

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
markup1 = ReplyKeyboardMarkup(conf.kb1, resize_keyboard=True, one_time_keyboard=True)
markup2 = ReplyKeyboardMarkup(conf.kb2, resize_keyboard=True, one_time_keyboard=True)
markup3 = ReplyKeyboardMarkup(conf.kb3, resize_keyboard=True, one_time_keyboard=True)

# grouping
btn = ("Alle", "Kanal 1", "Kanal 2", "Kanal 3", "Kanal 4", "Kanal 5", "Kanal 6", "Kanal 7", "Kanal 8")
selection = ()


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
        logging.info('Bot started...')
        __message_values(update)
        __cam_on()
        display.show_ready()
        update.message.reply_text('{0}{1}{2}'.format(
            lib.msg_welcome.format(update.message.from_user.first_name), lib.space, lib.msg_choice),
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
        """ starts separate thread """
        display.show_switch_channel_duration(1, int(water_time))

        __water(bot, update, group_one[0])

    elif target == str(lib.group1[2]):
        """ starts separate thread """
        display.show_switch_channel_duration(2, int(water_time))

        __water(bot, update, group_one[1])

    elif target == str(lib.group1[3]):
        """ starts separate thread """
        display.show_switch_channel_duration(3, int(water_time))

        __water(bot, update, group_one[2])

    elif target == str(lib.group2[1]):
        """ starts separate thread """
        display.show_switch_channel_duration(6, int(water_time))

        __water(bot, update, group_two[0])

    elif target == str(lib.group2[2]):
        """ starts separate thread """
        display.show_switch_channel_duration(7, int(water_time))

        __water(bot, update, group_two[1])

    elif target == str(lib.group2[3]):
        """ starts separate thread """
        display.show_switch_channel_duration(8, int(water_time))

        __water(bot, update, group_two[2])

    elif target == str(lib.group1[0]):
        """ starts separate thread """
        display.show_switch_group_duration(1, int(water_time))

        __water_group(bot, update, group_one)

    elif target == str(lib.group2[0]):
        """ starts separate thread """
        display.show_switch_group_duration(2, int(water_time))

        __water_group(bot, update, group_two)

    elif target == str(lib.group3[1]):
        """ starts separate thread """
        display.show_switch_channel_duration(4, int(water_time))

        __water(bot, update, group_three[0])

    elif target == str(lib.group3[2]):
        """ starts separate thread """
        display.show_switch_channel_duration(5, int(water_time))

        __water(bot, update, group_three[1])

    elif target == str(lib.group3[0]):
        """ starts separate thread """
        display.show_switch_group_duration(3, int(water_time))

        __water_group(bot, update, group_three)

    elif target == str(lib.all_channels):
        #__water_all(bot, update)
        __group(bot, update)

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
    __stop_standby_timer(bot, update)
    update.message.reply_text(lib.water_on_all.format(target, water_time),
                              parse_mode=ParseMode.MARKDOWN, reply_markup=markup3)

    """ starts separate thread """
    display.show_switch_group_duration(0, int(water_time))

    for channel in all_groups:
        utils.switch_on(channel)
    time.sleep(int(water_time) * int(lib.time_conversion))
    __all_off()

    update.message.reply_text('{0}{1}{2}'.format(
        __timestamp(), lib.water_off_all.format(water_time), lib.msg_new_choice),
        parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    display.show_off()
    __start_standby_timer(bot, update)
    return


@run_async
def __water(bot, update, channel):
    logging.info('Duration: {0}'.format(water_time))
    logging.info('Toggle {0}'.format(str(channel)))
    __stop_standby_timer(bot, update)
    update.message.reply_text(lib.water_on.format(target, water_time),
                              parse_mode=ParseMode.MARKDOWN, reply_markup=markup3)

    utils.switch_on(channel)
    time.sleep(int(water_time) * int(lib.time_conversion))
    utils.switch_off(channel)

    update.message.reply_text('{0}{1}{2}'.format(
        __timestamp(), lib.water_off.format(target, water_time), lib.msg_new_choice),
        parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    display.show_off()
    __start_standby_timer(bot, update)
    return


@run_async
def __water_group(bot, update, group):
    logging.info('Duration: {0}'.format(water_time))
    logging.info('Toggle {0}'.format(str(group)))
    __stop_standby_timer(bot, update)
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
    __start_standby_timer(bot, update)
    return


# get humidity and temperature values
def __message_values(update):
    """  to avoid refresh intervals shorter than 3 seconds """
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
    __all_off()
    __stop_standby_timer(bot, update)
    logging.info('Bot stopped.')
    __cam_off()
    display.show_stop()
    update.message.reply_text(lib.msg_stop, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    time.sleep(2)
    display.show_standby()
    return ConversationHandler.END

 
# [#39] Implement emergency stop
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
    logging.warning("Initialize emergency stop immediately.")
    return


# [#30] implement standby  init after given time without user activity
def __start_standby_timer(bot, update):
    global timer_job
    timer_job = jq.run_once(__job_stop_and_restart, conf.standby_timeout, context=update)
    logging.warning("Init standby timer of {0} seconds, added to queue.".format(conf.standby_timeout))
    return


def __stop_standby_timer(bot, upadate):
    timer_job.schedule_removal()
    logging.warning("Timer job removed from the queue.")
    return


# job to stop and restart application
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


# grouping
def __button(bot, update):
    global selection
    query = update.callback_query
    added_selection = query.data
    if not added_selection == "Fertig" or not added_selection == "Abbruch":
        logger.info(added_selection)
        if not selection.__contains__(added_selection):
            selection += (added_selection,)

        bot.edit_message_text(text="Selected: {} - Summary: {}".format(query.data, selection),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup)

        logger.info(selection)

    elif added_selection == "Fertig":
        logger.info("current slection: " + str(selection))
        # return selection
    elif added_selection == "Abbruch":
        return SELECTION


def __get_inline_btn(text, callback):
    return InlineKeyboardButton(text, callback_data=callback)


def __group(bot, update):
    inline_keyboard = [
        [__get_inline_btn(btn[1], "1"), __get_inline_btn(btn[2], "2"), __get_inline_btn(btn[3], "3"), __get_inline_btn(btn[4], "4")],
        [__get_inline_btn(btn[5], "5"), __get_inline_btn(btn[6], "6"), __get_inline_btn(btn[7], "7"), __get_inline_btn(btn[8], "8")],
        [__get_inline_btn("Fertig", "Fertig"), __get_inline_btn("Abbruch", "Abbruch")]
    ]

    global reply_markup
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    update.message.reply_text(' Grouping, please select: ', reply_markup=reply_markup)


def main():
    __init_bot_set_pins()

    global updater
    updater = Updater(token)

    global jq
    jq = updater.job_queue
    logging.info('Init job queue.')

    dp = updater.dispatcher

    group_handler = CallbackQueryHandler(__button)

    emergency_stop_handler = RegexHandler('^{0}$'.format(str(lib.emergency_stop)),
                                          __emergency_stop_handler,
                                          pass_chat_data=True)
    ch = ConversationHandler(
        entry_points=[CommandHandler('start', __start)],
        states={
            SELECTION: [RegexHandler(
                '^({0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10}|{11}|{12}|{13})$'.format(
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
                    str(lib.panic),
                    str(lib.live_stream),
                    str(lib.reload)), __selection),
                RegexHandler('^{0}$'.format(lib.stop_bot), __stop),
                RegexHandler('^{0}$'.format(lib.all_channels),grouping.group)
            ],

            DURATION: [RegexHandler('^([0-9]+|{0}|{1})$'.format(str(lib.cancel), str(lib.panic)), __duration),
                       RegexHandler('^{0}$'.format(lib.stop_bot), __stop)]
                },
        fallbacks=[CommandHandler('stop', __stop)]
    )
    dp.add_handler(group_handler)

    dp.add_handler(emergency_stop_handler)

    dp.add_handler(ch)

    dp.add_error_handler(__error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
