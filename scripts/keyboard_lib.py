#!/usr/bin/python
# -*- coding: utf-8 -*-

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


kbd2 = [[InlineKeyboardButton(text='Google', url='www.google.de')],
            [InlineKeyboardButton(text='R+',  url='www.rammstein.de')]
            ]

keyboard2 = InlineKeyboardMarkup(inline_keyboard=[kbd2],resize_keyboard=True, one_time_keyboard=False)

