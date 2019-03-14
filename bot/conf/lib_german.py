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

group1 = ('Kanal 1 bis 3', 'Kanal 1', 'Kanal 2', 'Kanal 3')
group2 = ('Kanal 6 bis 8', 'Kanal 6', 'Kanal 7', 'Kanal 8')
group3 = ('Kanal 4 und 5', 'Kanal 4', 'Kanal 5')

temp = 'Temperatur'
hum = 'Luftfeuchtigkeit'
core = 'Kern-Temperatur'

# messages
msg_grouping = '`Gruppierung, bitte auswählen!`'
msg_grouping_selection = '`Auswahl: {}`'
msg_live = '[Hier gehts zum Live Stream]({})'
msg_temperature = '`{}Aktuelle Werte\n{}, {}\n{}`'
msg_welcome = '`Hallo {}!`'
msg_stop = '` S T A N D B Y  \n Neustart ->` /start'
msg_duration = '`Schaltzeit für \'{}\' in ' + time_units_name[time_units_index] + ' angeben:`'
water_on = '`\'{}\' wird jetzt für {}' + time_units_sign[time_units_index] + ' eingeschaltet.`'
water_on_group = '`{} werden jetzt für {}' + time_units_sign[time_units_index] + ' eingeschalten.`'
water_on_all = '`\'{}\' wird jetzt für {}' + time_units_sign[time_units_index] + ' eingeschalten.`'
water_off = '`\'{}\' nach {}' + time_units_sign[time_units_index] + ' abgeschalten.\n\n`'
water_off_group = '`\'{}\' wurden nach {}' + time_units_sign[time_units_index] + ' abgeschalten.\n\n`'
water_off_all = '`Alles wurde nach {}' + time_units_sign[time_units_index] + ' wieder abgeschalten.`\n\n'
msg_choice = '`Bitte auswählen:`'
msg_new_choice = '`Neue Auswahl oder Beenden?`'
msg_panic = '*PANIK-MODUS*'
private_warning = '`Hallo {}, dies ist ein privater Bot!\nDeine ChatID: {} ist geblockt worden.`'


if __name__ == '__main__':
    pass
