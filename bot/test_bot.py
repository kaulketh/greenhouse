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
selection = ()

def __get_inline_kbd_btn(text, callback):
    return InlineKeyboardButton(text, callback_data=callback)


# def __build_kbd(callback=None):
#     keyboard = []
#     row = []
#     count = 0
#     for b in btn:
#         if btn.count(b) == int(callback):
#             next(btn.count(b))
#         while count < 3:
#             row.append(__get_inline_kbd_btn(b,btn.count(b)))
#             count +=1
#         if count == 3:
#             keyboard.append(row)
#             count = 0
#
#     return InlineKeyboardMarkup(keyboard)


def start(bot, update):
    keyboard =  [
        [InlineKeyboardButton(btn[1],"1"), InlineKeyboardButton(btn[2],"2"), InlineKeyboardButton(btn[3],"3")],
        [InlineKeyboardButton(btn[4],"4"), InlineKeyboardButton(btn[5],"5"), InlineKeyboardButton(btn[6],"6")],
        [InlineKeyboardButton(btn[7],"7"), InlineKeyboardButton(btn[8],"8"), InlineKeyboardButton(btn[0],"0")],
         ]

    global reply_markup
    global markup
    reply_markup = InlineKeyboardMarkup(keyboard)
    markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text(' Grouping, please select: ', reply_markup=reply_markup)


def button(bot, update):
    global selection
    query = update.callback_query
    added_selection = int(query.data)
    selection += (added_selection,)

    bot.edit_message_text(text="Selected: {} - Summary: {}".format(query.data, selection),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)

    logger.warning(selection)


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