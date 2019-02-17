#!/usr/bin/python
# -*- coding: utf-8 -*-
# stop_and_restart.py
"""
Possibility to group some channels and switch at same time
author: Thomas Kaulke, kaulketh@gmail.com
"""


from __future__ import absolute_import
import conf
import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode

logger = logger.get_logger()
btn = ("Alle", "Kanal 1", "Kanal 2", "Kanal 3", "Kanal 4", "Kanal 5", "Kanal 6", "Kanal 7", "Kanal 8")
selection = ()


def group(bot, update):
    inline_keyboard = [
        [__get_inline_btn(btn[1], "1"), __get_inline_btn(btn[2], "2"), __get_inline_btn(btn[3], "3")],
        [__get_inline_btn(btn[4], "4"), __get_inline_btn(btn[5], "5"), __get_inline_btn(btn[6], "6")],
        [__get_inline_btn(btn[7], "7"), __get_inline_btn(btn[8], "8"), __get_inline_btn(btn[0], "0")],
        [__get_inline_btn("Fertig", "Fertig"), __get_inline_btn("Abbruch", "Abbruch")]
    ]

    global reply_markup
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    update.message.reply_text(' Grouping, please select: ', reply_markup=reply_markup)


def button(bot, update):
    global selection
    query = update.callback_query
    if not query == "Fertig" or not query == "Abbruch":
        added_selection = int(query.data)
        logger.info(added_selection)
        if not selection.__contains__(added_selection):
            selection += (added_selection,)

        bot.edit_message_text(text="Selected: {} - Summary: {}".format(query.data, selection),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup)
        logger.info(selection)
    elif query == "Fertig":
        return selection
    elif query == "Abbruch":
        return greenhouse.SELECTION


def __get_inline_btn(text, callback):
    return InlineKeyboardButton(text, callback_data=callback)


if __name__ == '__main__':
    pass
