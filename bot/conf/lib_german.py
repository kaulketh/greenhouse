#!/usr/bin/python
# -*- coding: utf-8 -*-
# lib_german.py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

import lib_global as global_lib

empty = global_lib.empty
space = global_lib.space
colon_space = global_lib.colon_space
pipe_space = global_lib.pipe_space
line_break = global_lib.line_break
decimal = ','

# time units
time_units_index = global_lib.time_units_index
time_units_name = ('Sekunden', 'Minuten', 'Stunden')
time_units_sign = global_lib.time_units_sign
time_units_conversion = global_lib.time_units_conversion
time_conversion = global_lib.time_conversion

# commands and descriptions
panic = 'Panik'
cancel = 'Abbrechen'
all_channels = 'Alles'
stop_bot = 'Beenden'
live_stream = 'Schau mal!'
reload = 'Aktualisieren'
emergency_stop = 'NOT - STOP'
grouping = 'Gruppierung'
btn_finished = 'Fertig'
btn_cancel = cancel

channel_1 = 'Kanal 1'
channel_2 = 'Kanal 2'
channel_3 = 'Kanal 3'
channel_4 = 'Kanal 4'
channel_5 = 'Kanal 5'
channel_6 = 'Kanal 6'
channel_7 = 'Kanal 7'
channel_8 = 'Kanal 8'

temp = 'Temperatur'
hum = 'Luftfeuchtigkeit'
core = 'Kern-Temperatur'

# messages
msg_grouping = '`Gruppierung, bitte auswählen!`'
msg_grouping_selection = '`Ausgewählte Gruppe {}`'
msg_live = '[Hier gehts zum Live Stream]({})'
msg_temperature = '`{}Aktuelle Werte\n{}, {}\n{}`'
msg_welcome = '`Hallo {}!`'
msg_stop = '` S T A N D B Y  \n Neustart ->` /start'
msg_duration = '`Schaltzeit für \'{}\' in ' + time_units_name[time_units_index] + ' angeben:`'
water_on = '`\'{}\' wird jetzt für {}' + time_units_sign[time_units_index] + ' eingeschaltet.`'
water_off = '`\'{}\' nach {}' + time_units_sign[time_units_index] + ' abgeschalten.\n\n`'
msg_choice = '`Bitte auswählen:`'
msg_new_choice = '`Neue Auswahl oder Beenden?`'
msg_panic = '*PANIK-MODUS*'
private_warning = '`Hallo {}, dies ist ein privater Bot!\nDeine ChatID: {} ist geblockt worden.`'


if __name__ == '__main__':
    pass
