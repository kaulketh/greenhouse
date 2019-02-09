#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import conf.greenhouse_config as conf

btn_live = InlineKeyboardButton(text=conf.lib.msg_live.format(str(conf.live)), url=str(conf.live))
btn_start = InlineKeyboardButton(text='Start', callback_data='/start')
btn_break = InlineKeyboardButton(text=conf.lib.cancel, callback_data='/stop')
kbd_break = [[InlineKeyboardButton(text=conf.lib.cancel, callback_data='/stop')]]
markup_break = InlineKeyboardMarkup(inline_keyboard=kbd_break)

def __get_markup(button):
    keyboard = [[[button]]]
    markup = InlineKeyboardMarkup(keyboard)
    return markup


#def get_reply(update, button, text=None):
#    return update.message.reply_text(text, reply_markup=__get_markup(button))

def get_reply(update, text):
    keyboard = [[[InlineKeyboardButton(text=str(conf.lib.cancel), callback_data='/stop')]]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return update.message.reply_text(text, reply_markup=markup)
