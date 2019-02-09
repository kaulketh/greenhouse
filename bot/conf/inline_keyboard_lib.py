#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from __future__ import absolute_import
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import conf.greenhouse_config as conf


btn_live = InlineKeyboardButton(text=conf.lib.msg_live.format(str(conf.live)), url=str(conf.live))
btn_start = InlineKeyboardButton(text='Start',callback_data='/start')
btn_break = InlineKeyboardButton(text=)

kbd2 = [[InlineKeyboardButton(text='Google', url='www.google.de')],
            [InlineKeyboardButton(text='R+',  url='www.rammstein.de')]
            ]

keyboard2 = InlineKeyboardMarkup(inline_keyboard=[kbd2])

