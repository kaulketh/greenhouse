#!/usr/bin/python
# -*- coding: utf-8 -*-
# original: author: Stefan Weigert  http://www.stefan-weigert.de/php_loader/raspi.php
# adapted: author: Thomas Kaulke, kaulketh@gmail.com


from __future__ import absolute_import
import logging
import os
import time
import peripherals.timer as start_countdown
import peripherals.dht.dht as dht
import peripherals.temperature as core
import peripherals.four_digit.display as display
import conf.greenhouse_config as conf
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
logging.info('Enable bot, setup GPIO pins.')
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
LIST_OF_ADMINS = conf.admins
API_TOKEN = conf.token
Target = lib.empty
Water_Time = lib.empty
user_id = lib.empty


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

    if user_id not in LIST_OF_ADMINS:
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
        return SELECT


# set the target, member of group or group
def selection(bot, update):
    global Target
    Target = update.message.text

    if Target == str(lib.panic):
        update.message.reply_text(lib.msg_panic,
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        logging.info(lib.msg_panic)
        os.system(conf.run_extended_greenhouse + str(user_id))

    elif Target == str(lib.live_stream):
        update.message.reply_text(lib.msg_live.format(str(conf.live)), parse_mode=ParseMode.MARKDOWN)
        logging.info('Live URL requested.')
        return SELECT

    elif Target == str(lib.reload):
        logging.info('Refresh values requested.')
        message_values(update)
        return SELECT

    else:
        update.message.reply_text(lib.msg_duration.format(Target),
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=markup2)
        logging.info('Selection: {0}'.format(str(Target)))
        return DURATION


# set water duration
def duration(bot, update):
    global Water_Time
    Water_Time = update.message.text

    if Water_Time == str(lib.cancel):
        update.message.reply_text(lib.msg_new_choice,
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        logging.info(lib.msg_new_choice)

    elif Water_Time == str(lib.panic):
        update.message.reply_text(lib.msg_panic,
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        logging.info(lib.msg_panic)
        os.system(conf.run_extended_greenhouse + str(user_id))

    elif Target == str(lib.group1[1]):
        display.show_channel(1)
        water(update, group_one[0])

    elif Target == str(lib.group1[2]):
        display.show_channel(2)
        water(update, group_one[1])

    elif Target == str(lib.group1[3]):
        display.show_channel(3)
        water(update, group_one[2])

    elif Target == str(lib.group2[1]):
        display.show_channel(6)
        water(update, group_two[0])

    elif Target == str(lib.group2[2]):
        display.show_channel(7)
        water(update, group_two[1])

    elif Target == str(lib.group2[3]):
        display.show_channel(8)
        water(update, group_two[2])

    elif Target == str(lib.group1[0]):
        display.show_group(1)
        water_group(update, group_one)

    elif Target == str(lib.group2[0]):
        display.show_group(2)
        water_group(update, group_two)

    elif Target == str(lib.group3[1]):
        display.show_channel(4)
        water(update, group_three[0])

    elif Target == str(lib.group3[2]):
        display.show_channel(5)
        water(update, group_three[1])

    elif Target == str(lib.group3[0]):
        display.show_group(3)
        water_group(update, group_three)

    elif Target == str(lib.all_channels):
        logging.info('Duration: {0}'.format(Water_Time))
        update.message.reply_text(lib.water_on_all.format(Target, Water_Time),
                                  parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        display.show_group(0)
        for member in all_groups:
            conf.switch_on(member)

        time.sleep((int(Water_Time)*int(lib.time_conversion)))
        for member in all_groups:
            conf.switch_off(member)
        update.message.reply_text('{0}{1}{2}'.format(
            timestamp(), lib.water_off_all.format(Water_Time), lib.msg_new_choice),
            parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        display.show_off()

    else:
        update.message.reply_text(lib.msg_choice, reply_markup=markup1)
    return SELECT


# water the target
def water(update, member):
    logging.info('Duration: ' + Water_Time)
    logging.info('Toggle ' + str(member))
    update.message.reply_text(lib.water_on.format(Target, Water_Time),
                              parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    start_countdown
    conf.switch_on(member)
    time.sleep((int(Water_Time)*int(lib.time_conversion)))
    conf.switch_off(member)
    update.message.reply_text('{0}{1}{2}'.format(
        timestamp(), lib.water_off.format(Target, Water_Time), lib.msg_new_choice),
        parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    display.show_off()
    return


# water a group of targets
def water_group(update, group):
    logging.info('Duration: ' + Water_Time)
    logging.info('Toggle ' + str(group))
    update.message.reply_text(lib.water_on_group.format(Target, Water_Time),
                              parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    start_countdown
    for member in group:
        conf.switch_on(member)
    time.sleep((int(Water_Time)*int(lib.time_conversion)))
    for member in group:
        conf.switch_off(member)
    update.message.reply_text('{0}{1}{2}'.format(
        timestamp(), lib.water_off_group.format(Target, Water_Time), lib.msg_new_choice),
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
    logging.info('Bot stopped.')
    cam_off()
    display.show_stop()
    update.message.reply_text(lib.msg_stop.format(update.message.from_user.first_name),
                              parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    time.sleep(2)
    display.show_standby()
    return ConversationHandler.END


# error
def error(bot, update, error):
    logging.error('An error occurs! ' + str(error))
    display.show_error()
    cam_off()
    conf.GPIO.cleanup()
    return ConversationHandler.END


# main
def main():
    updater = Updater(API_TOKEN)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
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
                       RegexHandler('^{0}$'.format(lib.stop_bot), stop)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
