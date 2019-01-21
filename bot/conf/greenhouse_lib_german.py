#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

empty = ''
space = ' '
colon_space = ': '
pipe_space = '| '
line_break = '\n'
decimal = ','

# time unit
# time units settings (0 == seconds, 1 == minutes)
time_units_index = 0
time_units_name = ('Sekunden', 'Minuten')
time_units_sign = ('s', 'm')
time_units_conversion = (1, 60)
time_conversion = time_units_conversion[time_units_index]

# commands and descriptions
panic = 'Panik'
cancel = 'Abbrechen'
all_channels = 'Alles'
stop_bot = 'Beenden'
live_stream = 'Schau mal!'
reload = 'Aktualisieren'
group1 = ('Kanal 1 bis 3', 'Kanal 1', 'Kanal 2', 'Kanal 3')
group2 = ('Kanal 6 bis 8', 'Kanal 6', 'Kanal 7', 'Kanal 8')
group3 = ('Kanal 4 und 5', 'Kanal 4', 'Kanal 5')

temp = 'Temperatur'
hum = 'Luftfeuchtigkeit'
core = 'Kern-Temperatur'

# messages
msg_live = '[Hier gehts zum Live Stream]({})'
msg_temperature = '**`{}Aktuelle Werte`**`\n{}, {}\n{}`'
msg_welcome = '`Hallo {}!`'
msg_stop = '`Na dann, tschüss {}!`'
msg_duration = '`Schaltzeit für \'{}\' in ' + time_units_name[time_units_index] + ' angeben:`'
water_on = '`\'{}\' wird jetzt für {}' + time_units_sign[time_units_index] + ' eingeschaltet.`'
water_on_group = '`{} werden jetzt für {}' + time_units_sign[time_units_index] + ' eingeschalten.`'
water_on_all = '`\'{}\' wird jetzt für {}' + time_units_sign[time_units_index] + ' eingeschalten.`'
water_off = '`\'{}\' nach {}' + time_units_sign[time_units_index] + ' abgeschalten.\n\n`'
water_off_group = '`\'{}\' wurden nach {}' + time_units_sign[time_units_index] + ' abgeschalten.\n\n`'
water_off_all = '`Alles wurde nach {}' + time_units_sign[time_units_index] + ' wieder abgeschalten.`\n\n'
msg_choice = '`Bitte auswählen:`'
msg_new_choice = '`Neue Auswahl oder Beenden?`'
msg_panic = 'PANIK-MODUS!'
private_warning = '`Hallo {}, dies ist ein privater Bot!\nDeine ChatID: {} ist geblockt worden.`'
