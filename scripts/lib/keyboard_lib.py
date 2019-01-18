#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com


from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


kbd2 = [[InlineKeyboardButton(text='Google', url='www.google.de')],
            [InlineKeyboardButton(text='R+',  url='www.rammstein.de')]
            ]

keyboard2 = InlineKeyboardMarkup(inline_keyboard=[kbd2])

