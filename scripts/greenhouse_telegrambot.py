#!/usr/bin/python
# -*- coding: utf-8 -*-
# original: author: Stefan Weigert  http://www.stefan-weigert.de/php_loader/raspi.php
# adapted: author: Thomas Kaulke, kaulketh@gmail.com


from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, MessageEntity)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
import telepot
import time
import sys
import RPi.GPIO as GPIO
import os
import commands


# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# to use GPIO instead board pin numbers, then please adapt pin definition
# GPIO.setmode(GPIO.BCM)

# uncomment if warnings not required
#GPIO.setwarnings(False)

# def board pins/channels
TOMATO_01=29
TOMATO_02=31
TOMATO_03=33
CHILI_01=36
CHILI_02=38
CHILI_03=40

Vegetables = (TOMATO_01, TOMATO_02, TOMATO_03, CHILI_01, CHILI_02, CHILI_03)
Tomatoes = (TOMATO_01, TOMATO_02, TOMATO_03)
Chilis = (CHILI_01, CHILI_02, CHILI_03)

# time stamp
def timestamp():
        return time.strftime('`[%d.%m.%Y %H:%M:%S]\n---------------------\n`')



# switch functions
def switch_on(pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,GPIO.LOW)
        return

def switch_off(pin):
        GPIO.output(pin,GPIO.HIGH)
        GPIO.cleanup(pin)
        return

# default commands and texts
Cancel = 'Abbrechen'
All = 'Alles'
Stop = 'Beenden'
Group1 = ('Tomaten', 'Tomaten 1', 'Tomaten 2', 'Tomaten 3')
Group2 = ('Chilis', 'Chili 1', 'Chili 2', 'Chili 3')

# message texts
Msg_Welcome = '`Willkommen {}, lass uns Pflanzen bewässern!\n`'
Msg_Stop = '`Na dann, tschüss {}!\nZum nächsten Wässern geht\'s mit /start`'
Msg_Duration = '`Bewässerungsdauer für \'{}\' in Sekunden angeben:`'
Water_On = '`\'{}\' wird jetzt für {}s gewässert.`'
Water_On_All = '`Alle {} werden jetzt für {}s gewässert.`'
Water_Off = '`Bewässerung von \'{}\' nach {}s beendet.\n\n`'
Water_Off_All = '`Bewässerung von allen {} wurde nach {}s beendet.\n\n`'
Msg_Choice = '`Bitte auswählen:`'
Msg_New_Choice = '`Neue Auswahl oder Beenden?`'
Msg_Panic='*Panic called! \nTry some special!*'


# api and bot settings
SELECT, DURATION = range(2)
#LIST_OF_ADMINS = ['mock to test']
LIST_OF_ADMINS = [<first_allowed_id>, <second_allowed_id>, <next_allowed_id>]
Api_Token = "<token>"

Target = ' '
Water_Time = ' '


# keyboard config
keyboard1 =     [[str(Group1[0])],
                 [str(Group1[1]), str(Group1[2]), str(Group1[3])],
                 [str(Group2[0])],
                 [str(Group2[1]), str(Group2[2]), str(Group2[3])],
                 [All,Stop]
                ]
markup1 = ReplyKeyboardMarkup(keyboard1, resize_keyboard = True, one_time_keyboard = False)

keyboard2 =     [[Cancel],
                 [Stop]
                ]
markup2 = ReplyKeyboardMarkup(keyboard2, resize_keyboard = True, one_time_keyboard = False)


# start bot
def start(bot, update):

        try:
                user_id = update.message.from_user.id

        except (NameError, AttributeError):
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
                update.message.reply_text('`Hello {}, this is a private Bot!\nYour ChatID: {} has been blocked.`'.format(update.message.from_user.first_name, update.message.chat_id)$
                return ConversationHandler.END
        else:
                update.message.reply_text(Msg_Welcome.format(update.message.from_user.first_name) + '\n' + Msg_Choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
                return SELECT


# set the target, plant or plants
def selection(bot, update):
        global Target
        Target = update.message.text

        if Target == 'Panic':
                update.message.reply_text(Msg_Panic, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
                os.system('sudo python /home/pi/scripts/TelegramBot/ext_greenhouse.py')

        else:
                update.message.reply_text(Msg_Duration.format(Target), parse_mode=ParseMode.MARKDOWN, reply_markup=markup2)
                return DURATION


# set water duration
def duration(bot, update):
        global Water_Time
        Water_Time = update.message.text

        if Water_Time == str(Cancel):
                update.message.reply_text(Msg_New_Choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)

        elif Water_Time == 'Panic':
                update.message.reply_text(Msg_Panic, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
                os.system('sudo python /home/pi/scripts/TelegramBot/ext_greenhouse.py')

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

        elif Target == str(All):
                update.message.reply_text('`{} wird jetzt für {}s gewässert.`'.format(Target, Water_Time), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
                for vegetable in Vegetables:
                        switch_on(vegetable)
                time.sleep(int(Water_Time))
                for vegetable in Vegetables:
                        switch_off(vegetable)
                update.message.reply_text(timestamp() + '`Komplettbewässerung wurde nach {}s beendet.`\n\n'.format(Water_Time) + Msg_New_Choice, parse_mode=ParseMode.MARKDOWN, reply$

        else:
                update.message.reply_text(Msg_Choice, reply_markup=markup1)

        return SELECT

# water the target
def water(update, vegetable):
        update.message.reply_text(Water_On.format(Target, Water_Time), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        switch_on(vegetable)
        time.sleep((int(Water_Time)))
        switch_off(vegetable)
        update.message.reply_text(timestamp() + Water_Off.format(Target, Water_Time) + Msg_New_Choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        return


# water a group of targets
def water_group(update, group):
        update.message.reply_text(Water_On_All.format(Target, Water_Time), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        for member in group:
                switch_on(member)
        time.sleep(int(Water_Time))
        for member in group:
                switch_off(member)
        update.message.reply_text(timestamp() + Water_Off_All.format(Target, Water_Time) + Msg_New_Choice, parse_mode=ParseMode.MARKDOWN, reply_markup=markup1)
        return


# stop bot
def stop(bot, update):
        update.message.reply_text(Msg_Stop.format(update.message.from_user.first_name), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


# error
def error(bot, update, error):
        GPIO.cleanup()
        return ConversationHandler.END


# main
def main():
    updater = Updater(Api_Token)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
                SELECT:         [RegexHandler('^('+str(Group1[0])+'|'+str(Group1[1])+'|'+str(Group1[2])+'|'+str(Group1[3])+'|'+str(Group2[0])+'|'+str(Group2[1])+'|'+str(Group2[2])+'$
                                 RegexHandler('^' + str(Stop) + '$', stop)],

                DURATION:       [RegexHandler('^([0-9]+|' + str(Cancel) + '|Panic)$', duration),
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
