#!/usr/bin/python
# -*- coding: utf-8 -*-
# original: author: Stefan Weigert  http://www.stefan-weigert.de/php_loader/raspi.php
# adapted: author: Thomas Kaulke, kaulketh@gmail.com

import greenhouse_config as conf
import greenhouse_lib_german as lib
import keyboard_lib as keyboards

from telegram import (ReplyKeyboardMarkup,
                      ReplyKeyboardRemove, ParseMode, MessageEntity)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, RegexHandler, ConversationHandler)
import telepot
import time
import sys
import os
import commands
import logging

logging.basicConfig(filename=conf.log_file, format=conf.log_format,
                    datefmt=conf.log_date_format, level=logging.INFO)

# define pins
all_groups = conf.GROUP_ALL
group_one = conf.GROUP_01
group_two = conf.GROUP_02
group_three = conf.GROUP_03


# time stamp
def timestamp():
    return conf.getTimestampLine()


# switch all off at start, set all used GPIO=high
logging.info('Switch all off at start, set all used GPIO to HIGH.')
conf.resetPins()
for member in all_groups:
       conf.switch_off(member)
       
# enable camera module
def camOn():
    logging.info('Enable camera module.')
    os.system(conf.enable_camera)
    return

# enable camera module
def camOff():
    logging.info('Disable camera module.')
    os.system(conf.disable_camera)
    return

# api and bot settings
SELECT, DURATION = range(2)
#LIST_OF_ADMINS = ['mock to test']
LIST_OF_ADMINS = conf.admins
API_TOKEN = conf.token

Target = lib.empty
Water_Time = lib.empty
user_id = lib.empty


# keyboard config
keyboard1 = lib.kb1
markup1 = ReplyKeyboardMarkup(
    keyboard1, resize_keyboard=True, one_time_keyboard=False)

keyboard2 = lib.kb2
markup2 = ReplyKeyboardMarkup(keyboard2, resize_keyboard=True, one_time_keyboard=False)


# start bot
def start(bot, update):
    logging.info('Bot started.')
    camOn()
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
        logging.info('Not allowed access by: ' + str(user_id) + ' - ' +
                     update.message.from_user.last_name + ',' + update.message.from_user.first_name)
        update.message.reply_text(lib.private_warning.format(
            update.message.from_user.first_name, update.message.chat_id), parse_mode=ParseMode.MARKDOWN)
        return ConversationHandler.END
    else:
        update.message.reply_text(lib.msg_welcome.format(update.message.from_user.first_name) +
                                  '\n' + lib.msg_choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        logging.info('Bot is using by: ' + str(user_id) + ' - ' +
                     update.message.from_user.last_name + ',' + update.message.from_user.first_name)
        return SELECT


# set the target, member of group or group
def selection(bot, update):
    global Target
    Target = update.message.text

    if Target == str(lib.panic):
        update.message.reply_text(
            lib.msg_panic, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        logging.info(lib.msg_panic)
        os.system(conf.run_extended_greenhouse + str(user_id))

    else:
        update.message.reply_text(lib.msg_duration.format(
            Target), parse_mode=ParseMode.MARKDOWN, reply_markup=markup2)
        logging.info('Selection: ' + str(Target))
        return DURATION


# set water duration
def duration(bot, update):
    global Water_Time
    Water_Time = update.message.text

    if Water_Time == str(lib.cancel):
        update.message.reply_text(
            lib.msg_new_choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        logging.info(lib.msg_new_choice)

    elif Water_Time == str(lib.panic):
        update.message.reply_text(
            lib.msg_panic, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        logging.info(lib.msg_panic)
        os.system(conf.run_extended_greenhouse + str(user_id))

    elif Target == str(lib.group1[1]):
        water(update, group_one[0])

    elif Target == str(lib.group1[2]):
        water(update, group_one[1])

    elif Target == str(lib.group1[3]):
        water(update, group_one[2])

    elif Target == str(lib.group2[1]):
        water(update, group_two[0])

    elif Target == str(lib.group2[2]):
        water(update, group_two[1])

    elif Target == str(lib.group2[3]):
        water(update, group_two[2])

    elif Target == str(lib.group1[0]):
        water_group(update, group_one)

    elif Target == str(lib.group2[0]):
        water_group(update, group_two)

    elif Target == str(lib.group3[1]):
        water(update, group_three[0])

    elif Target == str(lib.group3[2]):
        water(update, group_three[1])

    elif Target == str(lib.group3[0]):
        water_group(update, group_three)

    elif Target == str(lib.all):
        logging.info('Duration: ' + Water_Time)
        update.message.reply_text(lib.water_on_all.format(
            Target, Water_Time), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        for member in all_groups:
            conf.switch_on(member)

        time.sleep(int(Water_Time))
        for member in all_groups:
            conf.switch_off(member)
        update.message.reply_text(timestamp() + lib.water_off_all.format(
            Water_Time) + lib.msg_new_choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)

    else:
        update.message.reply_text(lib.msg_choice, reply_markup=markup1)

    return SELECT


# water the target
def water(update, member):
    logging.info('Duration: ' + Water_Time)
    logging.info('Toggle ' + str(member))
    update.message.reply_text(lib.water_on.format(
        Target, Water_Time), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    conf.switch_on(member)
    time.sleep((int(Water_Time)))
    conf.switch_off(member)
    update.message.reply_text(timestamp() + lib.water_off.format(Target, Water_Time) +
                              lib.msg_new_choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    return

# water a group of targets
def water_group(update, group):
    logging.info('Duration: ' + Water_Time)
    logging.info('Toggle ' + str(group))
    update.message.reply_text(lib.water_on_group.format(
        Target, Water_Time), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    for member in group:
        conf.switch_on(member)
    time.sleep(int(Water_Time))
    for member in group:
        conf.switch_off(member)
    update.message.reply_text(timestamp() + lib.water_off_group.format(Target, Water_Time) +
                              lib.msg_new_choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    return


# stop bot
def stop(bot, update):
    logging.info('Bot stopped.')
    camOff()
    update.message.reply_text(lib.msg_stop.format(update.message.from_user.first_name),
                              parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


# error
def error(bot, update, error):
    logging.error('An error occurs! ' + str(error))
    camOff()
    conf.GPIO.cleanup()
    return ConversationHandler.END


# main
def main():
    updater = Updater(API_TOKEN)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SELECT:         [RegexHandler('^(' + str(lib.group1[0]) + '|' + str(lib.group1[1]) + '|' + str(lib.group1[2]) + '|' + str(lib.group1[3]) + '|' + str(lib.group2[0]) + '|' + str(lib.group2[1]) + '|' + str(lib.group2[2]) + '|' + str(lib.group2[3]) + '|' + str(lib.group3[0]) + '|' + str(lib.group3[1]) + '|' + str(lib.group3[2]) + '|' + str(lib.all) + '|' + str(lib.panic) + ')$', selection),
                             RegexHandler('^' + lib.stopBot + '$', stop)],

            DURATION:       [RegexHandler('^([0-9]+|' + str(lib.cancel) + '|' + str(lib.panic) + ')$', duration),
                             RegexHandler('^' + lib.stopBot + '$', stop)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
