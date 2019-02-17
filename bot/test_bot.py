#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""

from __future__ import absolute_import
import conf
import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logger = logger.get_logger('test bot')

btn = ( "Alle", "Kanal 1", "Kanal 2", "Kanal 3","Kanal 4", "Kanal 5", "Kanal 6", "Kanal 7", "Kanal 8")
selection = ()
message_ids = ()

def __get_inline_btn(text, callback):
    return InlineKeyboardButton(text, callback_data=callback)


def __get_kbd_btn(text, callback):
    return KeyboardButton(text, callback_data=callback)
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


def __store_message_id(bot, update):
    global message_ids
    try:
        if update.message.message_id is not None:
            message_ids += str(update.message.message_id)
        if update.callback_query.message.message_id is not None:
            message_ids += str(update.callback_query.message.message_id)
    finally:
        logger.critical(message_ids)
    return


def start(bot, update):
    inline_keyboard =  [
        [__get_inline_btn(btn[1], "1"), __get_inline_btn(btn[2], "2"), __get_inline_btn(btn[3], "3")],
        [__get_inline_btn(btn[4], "4"), __get_inline_btn(btn[5], "5"), __get_inline_btn(btn[6], "6")],
        [__get_inline_btn(btn[7], "7"), __get_inline_btn(btn[8], "8"), __get_inline_btn(btn[0], "0")],
         ]

    reply_keyboard = [
        [__get_kbd_btn(btn[1], "1"), __get_kbd_btn(btn[2], "2"), __get_kbd_btn(btn[3], "3")],
        [__get_kbd_btn(btn[4], "4"), __get_kbd_btn(btn[5], "5"), __get_kbd_btn(btn[6], "6")],
        [__get_kbd_btn(btn[7], "7"), __get_kbd_btn(btn[8], "8"), __get_kbd_btn(btn[0], "0")],
        [__get_kbd_btn('Water group: {}'.format(selection),'water')]
    ]

    global reply_markup
    global markup
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    #reply_markup = ReplyKeyboardMarkup(reply_keyboard)

    update.message.reply_text(' Grouping, please select: ', reply_markup=reply_markup)
    __store_message_id(bot, update)


def button(bot, update):
    global selection
    query = update.callback_query
    __store_message_id(bot, update)
    added_selection = int(query.data)

    logger.warning(added_selection)
    selection += (added_selection,)


    bot.edit_message_text(text="Selected: {} - Summary: {}".format(query.data, selection),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)
    __store_message_id(bot, update)

    # bot.send_message(text="Selected: {} - Summary: {}".format(query.data, selection),
    #                       chat_id=query.message.chat_id,
    #                       reply_to_message_id=query.message.message_id,
    #                       reply_markup=reply_markup)

    logger.warning(selection)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")
    __store_message_id(bot, update)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, error)


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