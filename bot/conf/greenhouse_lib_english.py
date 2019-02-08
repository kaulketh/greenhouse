#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

empty = ''
space = ' '
colon_space = ': '
pipe_space = '| '
line_break = '\n'
decimal = '.'

# time unit
# time units settings (0 == seconds, 1 == minutes)
time_units_index = 0
time_units_name = ('seconds', 'minutes')
time_units_sign = ('s', 'm')
time_units_conversion = (1, 60)
time_conversion = time_units_conversion[time_units_index]

# commands and descriptions
panic = 'Panic'
cancel = 'Cancel'
all_channels = 'All'
stop_bot = 'End'
live_stream = 'Take a look!'
reload = 'Reload'
group1 = ('Channel 1 to 3', 'Channel 1', 'Channel 2', 'Channel 3')
group2 = ('Channel 6 to 8', 'Channel 6', 'Channel 7', 'Channel 8')
group3 = ('Channel 4 and 5', 'Channel 4', 'Channel 5')

temp = 'Temperature'
hum = 'Humidity'
core = 'Core temperature'


# messages
msg_live = '[Click here for the live stream]({})'
msg_temperature = '`{}Current values\n{}, {}\n{}`'
msg_welcome = '`Hello {}!`'
msg_stop = '`  STANDBY  `'
msg_duration = '`Specify switching time for \'{}\' in ' + time_units_name[time_units_index] + ':`'
water_on = '`\'{}\' is switched on for {}' + time_units_sign[time_units_index] + '.`'
water_on_group = '`{} are switched on for {}' + time_units_sign[time_units_index] + '.`'
water_on_all = '`\'{}\' is switched on for {}' + time_units_sign[time_units_index] + '.`'
water_off = '`\'{}\' was switched off after {}' + time_units_sign[time_units_index] + '.\n\n`'
water_off_group = '`\'{}\' were switched off after {}' + time_units_sign[time_units_index] + '.\n\n`'
water_off_all = '`All was switched off after {}' + time_units_sign[time_units_index] + '.`\n\n'
msg_choice = '`Please select:`'
msg_new_choice = '`New choice or end?`'
msg_panic = '`PANIC MODE!`'
private_warning = '`Hello {}, this is a private bot!\nYour chat id: {} has been blocked.`'


if __name__ == '__main__':
    pass
