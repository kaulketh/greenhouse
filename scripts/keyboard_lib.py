#!/usr/bin/python
# -*- coding: utf-8 -*-

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


kbd2 = [InlineKeyboardButton(text=chr(0x1F4F7) + 'Schnappschuss', url='www.google.de'),
            InlineKeyboardButton(text=chr(0x25B6) + chr(0xFE0F) + 'Alarme ein',  url='www.rammstein.de')
            ]
keyboard2 = InlineKeyboardMarkup(inline_keyboard=[kbd2])

