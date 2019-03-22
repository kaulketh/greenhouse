#!/usr/bin/python
# -*- coding: utf-8 -*-
# greenhouse.py

"""
 main script for greenhouse bot
 using python-telegram-bot as Python framework for Telegram Bot API
 https://python-telegram-bot.readthedocs.io/en/stable/telegram.html
 https://github.com/python-telegram-bot
 https://core.telegram.org/api#bot-api
 original: author: Stefan Weigert  http://www.stefan-weigert.de/php_loader/raspi.php
 adapted: Thomas Kaulke, kaulketh@gmail.com
"""
from __future__ import absolute_import
import threading
import os
import time
import utils.utils as utils
import conf
import logger
import peripherals.dht.dht as dht
import peripherals.temperature as core
import utils.stop_and_restart as stop_and_restart
import peripherals.four_digit.display as display
import peripherals.monitor as monitor

from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

logger = logger.get_logger()
thread = threading.Thread(target=monitor.main, name='MainBot temperature monitoring')
thread.start()

lib = conf.lib
SELECTION, DURATION, GROUPING = range(3)
list_of_admins = conf.admins
token = conf.token
target = lib.empty
water_time = lib.empty
user_id = lib.empty
jq = None
timer_job = None
selection = ()
markup1 = ReplyKeyboardMarkup(conf.kb1, resize_keyboard=True, one_time_keyboard=True)
markup2 = ReplyKeyboardMarkup(conf.kb2, resize_keyboard=True, one_time_keyboard=True)
markup3 = ReplyKeyboardMarkup(conf.kb3, resize_keyboard=True, one_time_keyboard=True)


# Start info
def __init_bot_set_pins():
    logger.info('Initializing...')
    utils.set_pins()
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
        logger.warning('Not allowed access by: {0} - {1},{2}'.format(
            str(user_id), update.message.from_user.last_name, update.message.from_user.first_name))
        __reply(update, lib.private_warning.format(update.message.from_user.first_name, update.message.chat_id))
        return ConversationHandler.END
    else:
        display.show_run()
        logger.info('Started...')
        __message_values(update)
        __cam_on()
        display.show_ready()
        __reply(
            update,
            '{0}{1}{2}'.format(lib.msg_welcome.format(update.message.from_user.first_name), lib.space, lib.msg_choice),
            markup1)
        logger.info('Bot usage: {0} - {1},{2}'.format(
            str(user_id), update.message.from_user.last_name, update.message.from_user.first_name))
        display.show_off()

        __start_standby_timer(bot, update)
        return SELECTION


# select targets
def __selection(bot, update):
    global target
    target = update.message.text
    __stop_standby_timer(bot, update)

    if target == str(lib.panic):
        __panic(update)

    elif target == str(lib.live_stream):
        logger.info('Live URL requested.')
        __reply(update, lib.msg_live.format(str(conf.live)), markup1)
        __start_standby_timer(bot, update)
        return SELECTION

    elif target == str(lib.reload):
        logger.info('Refresh values requested.')
        __message_values(update)
        __start_standby_timer(bot, update)
        return SELECTION

    else:
        return __selected_target(bot, update, target)


def __selected_target(bot, update, selected_target):
    __reply(update, lib.msg_duration.format(selected_target), markup2)
    logger.info('Selection: {0}'.format(str(selected_target)))
    __start_standby_timer(bot, update)
    return DURATION
# end: select targets


# [#31] grouping
def __grouping(bot, update, chat_data):
    global selection
    query = update.callback_query
    btn_click = str(query.data)

    if not (btn_click == str(lib.btn_finished) or btn_click == str(lib.cancel)):
        if not selection.__contains__(int(btn_click)):
            __stop_standby_timer(bot, update)
            selection += (int(btn_click),)
            bot.edit_message_text(text=lib.msg_grouping_selection.format(selection),
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=reply_markup)
            __start_standby_timer(bot, update)

    elif btn_click == str(lib.btn_finished) and len(selection) > 0:
        __stop_standby_timer(bot, update)
        global target
        target = lib.grouping
        bot.edit_message_text(text=lib.msg_grouping_selection.format(selection),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=reply_markup)
        bot.send_message(text=lib.msg_duration.format(target + str(selection)),
                         chat_id=query.message.chat_id,
                         parse_mode=ParseMode.MARKDOWN,
                         reply_markup=markup2)
        logger.info('Selected: {0} {1}'.format(str(target), str(selection)))
        __start_standby_timer(bot, update)
        return DURATION

    elif btn_click == lib.cancel:
        __stop_standby_timer(bot, update)
        selection = ()
        bot.delete_message(chat_id=query.message.chat_id,
                           message_id=query.message.message_id)

        __send_message(lib.msg_new_choice, query, bot, markup1)
        __start_standby_timer(bot, update)
        return SELECTION


def __group_menu(bot, update):
    global selection
    selection = ()
    inline_keyboard = [
        [__get_btn(lib.channel_1, conf.RELAY_01), __get_btn(lib.channel_2, conf.RELAY_02),
         __get_btn(lib.channel_3, conf.RELAY_03), __get_btn(lib.channel_4, conf.RELAY_04)],
        [__get_btn(lib.channel_5, conf.RELAY_05), __get_btn(lib.channel_6, conf.RELAY_06),
         __get_btn(lib.channel_7, conf.RELAY_07), __get_btn(lib.channel_8, conf.RELAY_08)],
        [InlineKeyboardButton(lib.btn_finished, callback_data=lib.btn_finished),
         InlineKeyboardButton(lib.btn_cancel, callback_data=lib.btn_cancel)]
    ]

    global reply_markup
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    __reply(update, lib.msg_grouping, reply_markup)
    logger.info('Grouping called.')
    return GROUPING


def __get_btn(text, callback):
    return InlineKeyboardButton('{0} ({1})'.format(text, callback), callback_data=callback)
# end: grouping


# water duration
def __duration(bot, update):
    global water_time
    global g_duration_update
    g_duration_update = update
    water_time = update.message.text

    if water_time == str(lib.cancel):
        __reply(update, lib.msg_new_choice, markup1)
        logger.info(lib.msg_new_choice)

    elif water_time == str(lib.panic):
        __panic(update)

    elif target == str(lib.channel_1):
        display.show_switch_channel_duration(1, int(water_time))
        __water(bot, update, conf.RELAY_01)

    elif target == str(lib.channel_2):
        display.show_switch_channel_duration(2, int(water_time))
        __water(bot, update, conf.RELAY_02)

    elif target == str(lib.channel_3):
        display.show_switch_channel_duration(3, int(water_time))
        __water(bot, update, conf.RELAY_03)

    elif target == str(lib.channel_4):
        display.show_switch_channel_duration(4, int(water_time))
        __water(bot, update, conf.RELAY_04)

    elif target == str(lib.channel_5):
        display.show_switch_channel_duration(5, int(water_time))
        __water(bot, update, conf.RELAY_05)

    elif target == str(lib.channel_6):
        display.show_switch_channel_duration(6, int(water_time))
        __water(bot, update, conf.RELAY_06)

    elif target == str(lib.channel_7):
        display.show_switch_channel_duration(7, int(water_time))
        __water(bot, update, conf.RELAY_07)

    elif target == str(lib.channel_8):
        display.show_switch_channel_duration(8, int(water_time))
        __water(bot, update, conf.RELAY_08)

    elif target == str(lib.grouping):
        display.show_switch_group_duration(int(water_time))
        __water_group(bot, update, selection)

    else:
        __reply(update, lib.msg_choice, markup1)

    return SELECTION
# end: duration


# watering targets
def __all_off():
    logger.info('All off.')
    for relay in conf.ALL:
        utils.switch_out_high(relay)
    return


@run_async
def __water(bot, update, channel):
    __stop_standby_timer(bot, update)
    logger.info('Toggle {0} , Duration {1}'.format(str(channel), str(water_time)))
    __reply(update, lib.water_on.format(target, water_time), markup3)
    utils.switch_out_low(channel)
    time.sleep(int(water_time) * int(lib.time_conversion))
    utils.switch_out_high(channel)
    __reply(update,
            '{0}{1}{2}'.format(__timestamp(), lib.water_off.format(target, water_time), lib.msg_new_choice), markup1)
    display.show_off()
    __start_standby_timer(bot, update)
    return


@run_async
def __water_group(bot, update, group):
    __stop_standby_timer(bot, update)
    logger.info('Toggle {0} , Duration {1}'.format(str(group), str(water_time)))
    __reply(update, lib.water_on.format(target, water_time), markup3)
    for channel in group:
        utils.switch_out_low(channel)
    time.sleep((int(water_time) * int(lib.time_conversion)))
    for channel in group:
        utils.switch_out_high(channel)
    __reply(update,
            '{0}{1}{2}'.format(__timestamp(), lib.water_off.format(target, water_time), lib.msg_new_choice), markup1)
    display.show_off()
    __start_standby_timer(bot, update)
    return
# end watering targets


# get humidity and temperature values
def __message_values(update):
    time.sleep(3)
    """ avoid refresh intervals shorter than 3 seconds! """
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
    __reply(update, lib.msg_temperature.format(__start_time(), temp, hum, core_temp), markup1)
    return


# stop bot
def __stop(bot, update):
    __all_off()
    __stop_standby_timer(bot, update)
    logger.info('Stopped.')
    __cam_off()
    display.show_stop()
    __reply(update, lib.msg_stop, ReplyKeyboardRemove())
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
    logger.warning("Initialize emergency stop immediately.")
    global emergency_job
    emergency_job = jq.run_once(__job_stop_and_restart, 0, context=update)
    return
# end: emergency stop


# [#30] implement standby  init after given time without user activity
def __start_standby_timer(bot, update):
    logger.info("Init standby timer of {0} seconds, added to queue.".format(conf.standby_timeout))
    global timer_job
    timer_job = jq.run_once(__job_stop_and_restart, conf.standby_timeout, context=update)
    return


def __stop_standby_timer(bot, update):
    timer_job.schedule_removal()
    logger.info("Timer job removed from the queue.")
    return
# end: standby


# job to stop and restart application
def __job_stop_and_restart(bot, job):
    logger.info("Job: Stop and restart called!")
    stop_and_restart.stop_and_restart(job.context)
    return


# error handling
def __error(bot, update, any_error):
    try:
        logger.error('Update "{0}" caused error "{1}"'.format(update, any_error))
        display.show_error()
        __cam_off()
        __all_off()
        utils.GPIO.cleanup()

    except Unauthorized:
        # remove update.message.chat_id from conversation list
        logger.warning('TelegramError Unauthorized occurs!')

    except BadRequest:
        # handle malformed requests - read more below!
        logger.warning('TelegramError BadRequest occurs!')

    except TimedOut:
        # handle slow connection problems
        logger.warning('TelegramError TimedOut occurs!')

    except NetworkError:
        # handle other connection problems
        logger.warning('TelegramError NetworkError occurs!')

    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        logger.warning('TelegramError ChatMigrated \'{0}\' occurs!'.format(e))

    except TelegramError:
        # handle all other telegram related errors
        logger.warning('Any TelegramError occurs!')

    return ConversationHandler.END


# time stamps
def __timestamp():
    return utils.get_timestamp_line()


def __start_time():
    return utils.get_timestamp()
# end: time stamps


# camera
def __cam_on():
    logger.info('Enable camera module.')
    os.system(conf.enable_camera)
    return


def __cam_off():
    logger.info('Disable camera module.')
    os.system(conf.disable_camera)
    return
# end: camera


# release info
def __message_release_info(bot, update):
    __reply(update, '`' + utils.get_release_info() + '`')
    return


# reply message
def __reply(update, text, markup=None):
    if markup is None:
        update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    return


def __panic(update):
    logger.info('Panic mode called.')
    __reply(update, lib.msg_panic, ReplyKeyboardRemove())
    os.system(conf.run_extended_greenhouse + str(user_id))
    return


def main():
    __init_bot_set_pins()

    global updater
    updater = Updater(token)

    global jq
    jq = updater.job_queue
    logger.info('Init job queue.')

    dp = updater.dispatcher

    help_handler = CommandHandler('help', __message_release_info)

    emergency_stop_handler = RegexHandler('^{0}$'.format(str(lib.emergency_stop)),
                                          __emergency_stop_handler,
                                          pass_chat_data=True)
    ch = ConversationHandler(
        entry_points=[CommandHandler('start', __start)],
        states={
            SELECTION: [RegexHandler('^({0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10})$'.format(
                str(lib.channel_1), str(lib.channel_2), str(lib.channel_3), str(lib.channel_4),
                str(lib.channel_5), str(lib.channel_6), str(lib.channel_7), str(lib.channel_8),
                str(lib.panic), str(lib.live_stream), str(lib.reload)),
                __selection),

                RegexHandler('^{0}$'.format(lib.stop_bot), __stop),
                RegexHandler('^{0}$'.format(lib.grouping), __group_menu)],

            DURATION: [RegexHandler('^([0-9]+|{0}|{1})$'.format(str(lib.cancel), str(lib.panic)), __duration),
                       RegexHandler('^{0}$'.format(lib.stop_bot), __stop)],

            GROUPING: [CallbackQueryHandler(__grouping, pass_chat_data=True),
                       RegexHandler('^({0}|{1}|{2})$'.format(
                           str(lib.cancel), str(lib.btn_finished), str(selection)),
                           __selection)]
            },
        fallbacks=[CommandHandler('stop', __stop)],
        allow_reentry=True,
        per_chat=True,
        per_user=True
    )

    dp.add_error_handler(__error)
    dp.add_handler(emergency_stop_handler)
    dp.add_handler(help_handler)
    dp.add_handler(ch)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
