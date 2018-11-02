#!/usr/bin/python
# -*- coding: utf-8 -*-
# original: author: Stefan Weigert  http://www.stefan-weigert.de/php_loader/raspi.php
# adapted: author: Thomas Kaulke, kaulketh@gmail.com

import greenhouse_config as conf
import greenhouse_strings_german as de
import greenhouse_strings_english as en


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
Reserve = conf.GROUP_02
Chilis = conf.GROUP_03


# time stamp
def timestamp():
    return conf.timestamp_line


# commands and descriptions
run_extended_greenhouse = conf.run_extended_greenhouse
Panic = 'Panic'
Cancel = 'Abbrechen'
All = 'Alles'
Stop = 'Beenden'
Group1 = ('Tomaten', 'Tomaten 1', 'Tomaten 2', 'Tomaten 3')
Group2 = ('Chilis', 'Chili 1', 'Chili 2', 'Chili 3')
Group3 = ('Reserve', 'Reserve 1', 'Reserve 2')

# messages
Msg_Welcome = '`Willkommen {}, lass uns Pflanzen bewässern!\n`'
Msg_Stop = '`Na dann, tschüss {}!\nZum nächsten Wässern geht\'s mit /start`'
Msg_Duration = '`Bewässerungsdauer für \'{}\' in Sekunden angeben:`'
Water_On = '`\'{}\' wird jetzt für {}s gewässert.`'
Water_On_Group = '`Alle {} werden jetzt für {}s gewässert.`'
Water_On_All='`{} wird jetzt für {}s gewässert.`'
Water_Off = '`Bewässerung von \'{}\' nach {}s beendet.\n\n`'
Water_Off_Group = '`Bewässerung von allen {} wurde nach {}s beendet.\n\n`'
Water_Off_All='`Komplettbewässerung wurde nach {}s beendet.`\n\n'
Msg_Choice = '`Bitte auswählen:`'
Msg_New_Choice = '`Neue Auswahl oder Beenden?`'
Msg_Panic='*Panic called! \nTry some special!*'
Private_Warning = '`Hello {}, this is a private Bot!\nYour ChatID: {} has been blocked.`'


# api and bot settings
SELECT, DURATION = range(2)
#LIST_OF_ADMINS = ['mock to test']
LIST_OF_ADMINS = conf.admins
Api_Token = conf.token

Target = ' '
Water_Time = ' '


# keyboard config
keyboard1 =     [[str(Group1[0])],
                 [str(Group1[1]), str(Group1[2]), str(Group1[3])],
                 [str(Group2[0])],
                 [str(Group2[1]), str(Group2[2]), str(Group2[3])],
                 [str(Group3[1]), str(Group3[2])],
                 [str(Group3[0])],
                 [All,Stop],
                 [str(Panic)]
                ]
markup1 = ReplyKeyboardMarkup(keyboard1, resize_keyboard = True, one_time_keyboard = False)

keyboard2 =     [[Cancel],
                 [Stop]
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
        update.message.reply_text(Private_Warning.format(update.message.from_user.first_name, update.message.chat_id), parse_mode=ParseMode.MARKDOWN)
        return ConversationHandler.END
    else:
        update.message.reply_text(Msg_Welcome.format(update.message.from_user.first_name) + '\n' + Msg_Choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        logging.info('Bot is using by: ' + str(user_id) + ' - ' + update.message.from_user.last_name + ',' + update.message.from_user.first_name)
        return SELECT


# set the target, member of group or group
def selection(bot, update):
    global Target
    Target = update.message.text

    if Target == str(Panic):
        update.message.reply_text(Msg_Panic, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        logging.info(Msg_Panic)
        os.system(run_extended_greenhouse)

    else:
        update.message.reply_text(Msg_Duration.format(Target), parse_mode=ParseMode.MARKDOWN, reply_markup=markup2)
        logging.info('Selection: ' + str(Target))
        return DURATION


# set water duration
def duration(bot, update):
    global Water_Time
    Water_Time = update.message.text

    if Water_Time == str(Cancel):
        update.message.reply_text(Msg_New_Choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        logging.info(Msg_New_Choice)

    elif Water_Time == str(Panic):
        update.message.reply_text(Msg_Panic, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove()) 
        logging.info(Msg_Panic)
        os.system(run_extended_greenhouse)

    elif Target == str(Group1[1]):
        water(update, TOMATO_01)

    elif Target == str(Group1[2]):
        water(update, TOMATO_02)

    elif Target == str(Group1[3]):
        water(update, TOMATO_03)

    elif Target == str(Group2[1]):
        water(update, CHILI_01)

    elif Target == str(Group2[2]):
        water(update, CHILI_02)

    elif Target == str(Group2[3]):
        water(update, CHILI_03)

    elif Target == str(Group1[0]):
        water_group(update, Tomatoes)

    elif Target == str(Group2[0]):
        water_group(update, Chilis)
        
    elif Target == str(Group3[0]):
        water_group(update, Reserve)
        
    elif Target == str(All):
        logging.info('Duration: ' + Water_Time)
        update.message.reply_text(Water_On_All.format(Target, Water_Time), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        for vegetable in Vegetables:
            conf.switch_on(vegetable)
            time.sleep(int(Water_Time))
        for vegetable in Vegetables:
            conf.switch_off(vegetable)
            update.message.reply_text(timestamp() + Water_Off_All.format(Water_Time) + Msg_New_Choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)

    else:
        update.message.reply_text(Msg_Choice, reply_markup=markup1)

    return SELECT


# water the target
def water(update, vegetable):
    logging.info('Duration: ' + Water_Time)
    logging.info('Toggle ' + str(vegetable))
    update.message.reply_text(Water_On.format(Target, Water_Time), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    conf.switch_on(vegetable)
    time.sleep((int(Water_Time)))
    conf.switch_off(vegetable)
    update.message.reply_text(timestamp() + Water_Off.format(Target, Water_Time) + Msg_New_Choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    return

# water a group of targets
def water_group(update, group):
    logging.info('Duration: ' + Water_Time)
    logging.info('Toggle ' + str(group))
    update.message.reply_text(Water_On_Group.format(Target, Water_Time), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    for member in group:
        conf.switch_on(member)
    time.sleep(int(Water_Time))
    for member in group:
        conf.switch_off(member)
    update.message.reply_text(timestamp() + Water_Off_Group.format(Target, Water_Time) + Msg_New_Choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
    return


# stop bot
def stop(bot, update):
    logging.info('Bot stopped.')
    update.message.reply_text(Msg_Stop.format(update.message.from_user.first_name), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END





# error
def error(bot, update, error):
    logging.error('An error occurs! '+ str(error))
    conf.GPIO.cleanup()
    return ConversationHandler.END


# main
def main():
    updater = Updater(Api_Token)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
                SELECT:         [RegexHandler('^('+str(Group1[0])+'|'+str(Group1[1])+'|'+str(Group1[2])+'|'+str(Group1[3])+'|'+str(Group2[0])+'|'+str(Group2[1])+'|'+str(Group2[2])+'|'+str(Group2[3])+'|'+str(Group3[0])+'|'+str(Group3[1])+'|'+str(Group3[2])+'|' + str(All) + '|'+str(Panic)+')$', selection),
                                 RegexHandler('^' + str(Stop) + '$', stop)],

                DURATION:       [RegexHandler('^([0-9]+|' + str(Cancel) + '|'+str(Panic)+')$', duration),
                                RegexHandler('^' + str(Stop) + '$', stop )],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
