#!/usr/bin/python
# -*- coding: utf-8 -*-
# original: author: Stefan Weigert  http://www.stefan-weigert.de/php_loader/raspi.php
# adapted: author: Thomas Kaulke, kaulketh@gmail.com

import greenhouse_config as conf
import greenhouse_strings_german as text

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, MessageEntity)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
import telepot
import time
import sys
import os
import commands
import logging

logging.basicConfig(filename=conf.log_file, format=conf.log_format,datefmt=conf.log_date_format, level=logging.INFO)

# define pins
Vegetables = conf.GROUP_ALL
Tomatoes = conf.GROUP_01
Chilis = conf.GROUP_02
Reserve = conf.GROUP_03


# time stamp
def timestamp():
    return conf.timestamp_line

# api and bot settings
SELECT, DURATION = range(2)
#LIST_OF_ADMINS = ['mock to test']
LIST_OF_ADMINS = conf.admins
API_TOKEN = conf.token

Target = text.empty
Water_Time = text.empty


# keyboard config
keyboard1 =     [[str(text.group1[0])],
                 [str(text.group1[1]), str(text.group1[2]), str(text.group1[3])],
                 [str(text.group2[0])],
                 [str(text.group2[1]), str(text.group2[2]), str(text.group2[3])],
                 [str(text.group3[1]), str(text.group3[2])],
                 [str(text.group3[0])],
                 [text.all,text.stop],
                 [str(text.panic)]
                ]
markup1 = ReplyKeyboardMarkup(keyboard1, resize_keyboard = True, one_time_keyboard = False)

keyboard2 =     [[text.cancel],
                 [text.stop]
                ]
markup2 = ReplyKeyboardMarkup(keyboard2, resize_keyboard = True, one_time_keyboard = False)


# start bot
def start(bot, update):
    logging.info('Bot started.')
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
        logging.info('Not allowed access by: ' + str(user_id) + ' - ' + update.message.from_user.last_name + ',' + update.message.from_user.first_name)
        update.message.reply_text(text.private_warning.format(update.message.from_user.first_name, update.message.chat_id), parse_mode=ParseMode.MARKDOWN)
        return ConversationHandler.END
    else:
        update.message.reply_text(text.msg_welcome.format(update.message.from_user.first_name) + '\n' + text.msg_choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        logging.info('Bot is using by: ' + str(user_id) + ' - ' + update.message.from_user.last_name + ',' + update.message.from_user.first_name)
        return SELECT


# set the target, member of group or group
def selection(bot, update):
    global Target
    Target = update.message.text

    if Target == str(text.panic):
        update.message.reply_text(text.msg_panic, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        logging.info(text.msg_panic)
        os.system(conf.run_extended_greenhouse)

    else:
        update.message.reply_text(text.msg_duration.format(Target), parse_mode=ParseMode.MARKDOWN, reply_markup=markup2)
        logging.info('Selection: ' + str(Target))
        return DURATION


# set water duration
def duration(bot, update):
    global Water_Time
    Water_Time = update.message.text

    if Water_Time == str(text.cancel):
        update.message.reply_text(text.msg_new_choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        logging.info(text.msg_new_choice)

    elif Water_Time == str(Panic):
        update.message.reply_text(text.msg_panic, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove()) 
        logging.info(text.msg_panic)
        os.system(conf.run_extended_greenhouse)

    elif Target == str(text.group1[1]):
        water(update, TOMATO_01)

    elif Target == str(text.group1[2]):
        water(update, TOMATO_02)

    elif Target == str(text.group1[3]):
        water(update, TOMATO_03)

    elif Target == str(text.group2[1]):
        water(update, CHILI_01)

    elif Target == str(text.group2[2]):
        water(update, CHILI_02)

    elif Target == str(text.group2[3]):
        water(update, CHILI_03)

    elif Target == str(text.group1[0]):
        water_group(update, Tomatoes)

    elif Target == str(text.group2[0]):
        water_group(update, Chilis)
        
    elif Target == str(text.group3[0]):
        water_group(update, Reserve)
        
    elif Target == str(text.all):
        logging.info('Duration: ' + Water_Time)
        update.message.reply_text(text.water_on_all.format(Target, Water_Time), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        for vegetable in Vegetables:
            conf.switch_on(vegetable)
            time.sleep(int(Water_Time))
        for vegetable in Vegetables:
            conf.switch_off(vegetable)
            update.message.reply_text(timestamp() + text.water_off_all.format(Water_Time) + text.msg_new_choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)

    else:
        update.message.reply_text(text.msg_choice, reply_markup=markup1)

    return SELECT


# water the target
def water(update, vegetable):
    logging.info('Duration: ' + Water_Time)
    logging.info('Toggle ' + str(vegetable))
    update.message.reply_text(text.water_on.format(Target, Water_Time), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    conf.switch_on(vegetable)
    time.sleep((int(Water_Time)))
    conf.switch_off(vegetable)
    update.message.reply_text(timestamp() + text.water_off.format(Target, Water_Time) + text.msg_new_choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    return

# water a group of targets
def water_group(update, group):
    logging.info('Duration: ' + Water_Time)
    logging.info('Toggle ' + str(group))
    update.message.reply_text(text.water_on_group.format(Target, Water_Time), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    for member in group:
        conf.switch_on(member)
    time.sleep(int(Water_Time))
    for member in group:
        conf.switch_off(member)
    update.message.reply_text(timestamp() + text.water_off_group.format(Target, Water_Time) + text.msg_new_choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    return


# stop bot
def stop(bot, update):
    logging.info('Bot stopped.')
    update.message.reply_text(text.msg_stop.format(update.message.from_user.first_name), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END





# error
def error(bot, update, error):
    logging.error('An error occurs! '+ str(error))
    conf.GPIO.cleanup()
    return ConversationHandler.END


# main
def main():
    updater = Updater(API_TOKEN)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
                SELECT:         [RegexHandler('^('+str(text.group1[0])+'|'+str(text.group1[1])+'|'+str(text.group1[2])+'|'+str(text.group1[3])+'|'+str(text.group2[0])+'|'+str(text.group2[1])+'|'+str(text.group2[2])+'|'+str(text.group2[3])+'|'+str(text.group3[0])+'|'+str(text.group3[1])+'|'+str(text.group3[2])+'|' + str(text.all) + '|'+str(text.panic)+')$', selection),
                                 RegexHandler('^' + str(text.stop) + '$', stop)],

                DURATION:       [RegexHandler('^([0-9]+|' + str(text.cancel) + '|'+str(text.panic)+')$', duration),
                                RegexHandler('^' + str(text.stop) + '$', stop )],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
