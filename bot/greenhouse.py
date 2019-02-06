#!/usr/bin/python
# -*- coding: utf-8 -*-
# original: author: Stefan Weigert  http://www.stefan-weigert.de/php_loader/raspi.php
# adapted: author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
import logging
import os
import time
import conf.greenhouse_config as conf
import peripherals.dht.dht as dht
import peripherals.temperature as core
import peripherals.four_digit.display as display

from telegram import (ReplyKeyboardMarkup,
                      ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, RegexHandler, ConversationHandler)

logging.basicConfig(filename=conf.log_file, format=conf.log_format,
                    datefmt=conf.log_date_format, level=logging.INFO)

# language library
lib = conf.lib

# define pins
all_groups = conf.GROUP_ALL
group_one = conf.GROUP_01
group_two = conf.GROUP_02
group_three = conf.GROUP_03


# time stamp
def timestamp():
    return conf.get_timestamp_line()


def start_time():
    return conf.get_timestamp()


# switch all off at start, set all used GPIO=high
logging.info('\nInitialize bot, setup GPIO pins.')
conf.set_pins()
logging.info('Switch all off at start.')
for member in all_groups:
    conf.switch_off(member)

display.show_standby()


# enable camera module
def cam_on():
    logging.info('Enable camera module.')
    os.system(conf.enable_camera)
    return


# enable camera module
def cam_off():
    logging.info('Disable camera module.')
    os.system(conf.disable_camera)
    return


# api and bot settings
SELECT, DURATION = range(2)
# LIST_OF_ADMINS = ['mock to test']
list_of_admins = conf.admins
token = conf.token
target = lib.empty
water_time = lib.empty
user_id = lib.empty
jq = None

# keyboard config
markup1 = ReplyKeyboardMarkup(conf.kb1, resize_keyboard=True, one_time_keyboard=False)
markup2 = ReplyKeyboardMarkup(conf.kb2, resize_keyboard=True, one_time_keyboard=False)


# start bot
def start(bot, update):
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
        message_values(update)
        cam_on()
        display.show_ready()
        update.message.reply_text('{0}{1}{2}'.format(
            lib.msg_welcome.format(update.message.from_user.first_name), lib.line_break, lib.msg_choice),
            parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        logging.info('Bot is using by: {0} - {1},{2}'.format(
            str(user_id), update.message.from_user.last_name, update.message.from_user.first_name))
        logging.info('Time unit is \'{0}\''.format(str(lib.time_units_name[lib.time_units_index])))
        display.show_off()
        start_standby_timer(bot, update)
        return SELECT


# set the target, member of group or group
def selection(bot, update):
    global target
    target = update.message.text

    start_standby_timer(bot, update)

    if target == str(lib.panic):
        update.message.reply_text(lib.msg_panic,
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        logging.info(lib.msg_panic)
        os.system(conf.run_extended_greenhouse + str(user_id))

    elif target == str(lib.live_stream):
        update.message.reply_text(lib.msg_live.format(str(conf.live)), parse_mode=ParseMode.MARKDOWN)
        logging.info('Live URL requested.')
        return SELECT

    elif target == str(lib.reload):
        logging.info('Refresh values requested.')
        message_values(update)
        return SELECT

    else:
        update.message.reply_text(lib.msg_duration.format(target),
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=markup2)
        logging.info('Selection: {0}'.format(str(target)))
        return DURATION


# set water duration
def duration(bot, update):
    global water_time
    water_time = update.message.text

    start_standby_timer(bot, update)

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
        water(update, group_one[0])

    elif target == str(lib.group1[2]):
        """ starts separate thread"""
        display.show_switch_channel_duration(2, int(water_time))
        water(update, group_one[1])

    elif target == str(lib.group1[3]):
        """ starts separate thread"""
        display.show_switch_channel_duration(3, int(water_time))
        water(update, group_one[2])

    elif target == str(lib.group2[1]):
        """ starts separate thread"""
        display.show_switch_channel_duration(6, int(water_time))
        water(update, group_two[0])

    elif target == str(lib.group2[2]):
        """ starts separate thread"""
        display.show_switch_channel_duration(7, int(water_time))
        water(update, group_two[1])

    elif target == str(lib.group2[3]):
        """ starts separate thread"""
        display.show_switch_channel_duration(8, int(water_time))
        water(update, group_two[2])

    elif target == str(lib.group1[0]):
        """ starts separate thread"""
        display.show_switch_group_duration(1, int(water_time))
        water_group(update, group_one)

    elif target == str(lib.group2[0]):
        """ starts separate thread"""
        display.show_switch_group_duration(2, int(water_time))
        water_group(update, group_two)

    elif target == str(lib.group3[1]):
        """ starts separate thread"""
        display.show_switch_channel_duration(4, int(water_time))
        water(update, group_three[0])

    elif target == str(lib.group3[2]):
        """ starts separate thread"""
        display.show_switch_channel_duration(5, int(water_time))
        water(update, group_three[1])

    elif target == str(lib.group3[0]):
        """ starts separate thread"""
        display.show_switch_group_duration(3, int(water_time))
        water_group(update, group_three)

    elif target == str(lib.all_channels):
        logging.info('Duration: {0}'.format(water_time))
        update.message.reply_text(lib.water_on_all.format(target, water_time),
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        """ starts separate thread"""
        display.show_switch_group_duration(0, int(water_time))
        for channel in all_groups:
            conf.switch_on(channel)

        time.sleep((int(water_time) * int(lib.time_conversion)))
        for channel in all_groups:
            conf.switch_off(channel)
        update.message.reply_text('{0}{1}{2}'.format(
            timestamp(), lib.water_off_all.format(water_time), lib.msg_new_choice),
            parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        display.show_off()

    else:
        update.message.reply_text(lib.msg_choice, reply_markup=markup1)

    return SELECT


# water the target
def water(update, channel):
    logging.info('Duration: ' + water_time)
    logging.info('Toggle ' + str(channel))
    update.message.reply_text(lib.water_on.format(target, water_time),
                              parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    conf.switch_on(channel)
    time.sleep((int(water_time) * int(lib.time_conversion)))
    conf.switch_off(channel)
    update.message.reply_text('{0}{1}{2}'.format(
        timestamp(), lib.water_off.format(target, water_time), lib.msg_new_choice),
        parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    display.show_off()
    return


# water a group of targets
def water_group(update, group):
    logging.info('Duration: ' + water_time)
    logging.info('Toggle ' + str(group))
    update.message.reply_text(lib.water_on_group.format(target, water_time),
                              parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    for channel in group:
        conf.switch_on(channel)
    time.sleep((int(water_time) * int(lib.time_conversion)))
    for channel in group:
        conf.switch_off(channel)
    update.message.reply_text('{0}{1}{2}'.format(
        timestamp(), lib.water_off_group.format(target, water_time), lib.msg_new_choice),
        parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    display.show_off()
    return


# humidity and temperature
def message_values(update):
    """to avoid refresh intervals shorter than 3 seconds"""
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
        start_time(), temp, hum, core_temp), parse_mode=ParseMode.MARKDOWN)
    return


# stop bot
def stop(bot, update):
    timer_job = jq.run_once(job_stop, 0, context=update.message.chat_id)
    jq.start()
    jq.tick()
    stop_job_queue(bot, update, timer_job)
    return ConversationHandler.END


# error
def error(bot, update, e):
    logging.error('An error occurs! ' + str(e))
    display.show_error()
    cam_off()
    conf.GPIO.cleanup()
    return ConversationHandler.END


def job_stop(bot, job):
    logging.info('Bot stopped.')
    cam_off()
    display.show_stop()
    bot.send_message(
        chat_id=job.context, text=lib.msg_stop, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    time.sleep(2)
    display.show_standby()


def start_standby_timer(bot, update):
    jq.run_once(job_stop, conf.standby_timeout, context=str(user_id))
    jq.start()
    jq.tick()
    logging.info("Standby timer started.")
    return


def stop_job_queue(bot, update, job):
    job.schedule_removal()
    jq.stop()
    logging.info("Job queue stopped.")
    return


def main():
    updater = Updater(token)

    global jq
    jq = updater.job_queue
    logging.info('Init job queue.')

    dp = updater.dispatcher

    ch = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SELECT: [RegexHandler(
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
                    str(lib.reload)), selection),
                RegexHandler('^{0}$'.format(lib.stop_bot), stop)],

            DURATION: [RegexHandler('^([0-9]+|{0}|{1})$'.format(str(lib.cancel), str(lib.panic)), duration),
                       RegexHandler('^{0}$'.format(lib.stop_bot), stop)]

        },
        fallbacks=[CommandHandler('stop', stop)],

    )

    dp.add_handler(ch)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
