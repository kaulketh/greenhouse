#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""

from __future__ import absolute_import
import conf
import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logger = logger.get_logger('test bot')

btn = ( "Alle", "Kanal 1", "Kanal 2", "Kanal 3","Kanal 4", "Kanal 5", "Kanal 6", "Kanal 7", "Kanal 8")


def __get_inline_kbd_btn(text, callback):
    return InlineKeyboardButton(text, callback_data=callback)


def start(bot, update):
    keyboard =  [
        [__get_inline_kbd_btn(btn[1],"1"), __get_inline_kbd_btn(btn[2],"2"), __get_inline_kbd_btn(btn[3],"3")],
        [__get_inline_kbd_btn(btn[4],"4"), __get_inline_kbd_btn(btn[5],"5"), __get_inline_kbd_btn(btn[6],"6")],
        [__get_inline_kbd_btn(btn[7],"7"), __get_inline_kbd_btn(btn[8],"8"), __get_inline_kbd_btn(btn[0],"0")],
         ]

    # inline_keyboard = [
    #     [InlineKeyboardButton("Option 1", callback_data='1'), InlineKeyboardButton("Option 2", callback_data='2')],
    #                     [InlineKeyboardButton(text='R+',  url='www.rammstein.de')]
    # ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query


    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(conf.token)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()