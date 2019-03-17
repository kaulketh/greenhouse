#!/usr/bin/python
# -*- coding: utf-8 -*-
# lib_english.py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""
import lib_global as global_lib

empty = global_lib.empty
space = global_lib.space
colon_space = global_lib.colon_space
pipe_space = global_lib.pipe_space
line_break = global_lib.line_break
decimal = '.'

# time units
time_units_index = global_lib.time_units_index
time_units_name = ('seconds', 'minutes', 'hours')
time_units_sign = global_lib.time_units_sign
time_units_conversion = global_lib.time_units_conversion
time_conversion = global_lib.time_conversion

# commands and descriptions
panic = 'Panic'
cancel = 'Cancel'
all_channels = 'All'
stop_bot = 'End'
live_stream = 'Take a look!'
emergency_stop = 'EMERGENCY STOP'
grouping = 'Grouping'
btn_finished = 'Finished'
btn_cancel = cancel
reload = 'Reload'
group1 = ('Channel 1 to 3', 'Channel 1', 'Channel 2', 'Channel 3')
group2 = ('Channel 6 to 8', 'Channel 6', 'Channel 7', 'Channel 8')
group3 = ('Channel 4 and 5', 'Channel 4', 'Channel 5')

temp = 'Temperature'
hum = 'Humidity'
core = 'Core temperature'

# messages
msg_grouping = '`Grouping, please select`'
msg_grouping_selection = '`Selected group {}`'
msg_live = '[Click here for the live stream]({})'
msg_temperature = '`{}Current values\n{}, {}\n{}`'
msg_welcome = '`Hello {}!`'
msg_stop = '` S T A N D B Y  \n Restart ->` /start'
msg_duration = '`Specify switching time for \'{}\' in ' + time_units_name[time_units_index] + ':`'
water_on = '`\'{}\' is switched on for {}' + time_units_sign[time_units_index] + '.`'
water_off = '`\'{}\' was switched off after {}' + time_units_sign[time_units_index] + '.\n\n`'
msg_choice = '`Please select:`'
msg_new_choice = '`New choice or end?`'
msg_panic = '`PANIC MODE!`'
private_warning = '`Hello {}, this is a private bot!\nYour chat id: {} has been blocked.`'


if __name__ == '__main__':
    pass
