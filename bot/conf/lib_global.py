#!/usr/bin/python
# -*- coding: utf-8 -*-
# lib_global.py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

empty = ''
space = ' '
colon_space = ': '
pipe_space = '| '
line_break = '\n'

"""
timeout if no user activity 
"""
timeout = 60


""" language settings
0 - English
1 - German
"""
language_index = 1

""" time units settings 
0 == seconds
1 == minutes
2 == hours
"""
time_units_index = 0
time_units_conversion = (1, 60, 3600)
time_units_sign = ('s', 'm', 'h')
time_conversion = time_units_conversion[time_units_index]


# TODO: make accessible in bash and vice versa!!!!
file_log_greenhouse = '/greenhouse.log'
file_log_debug = '/greenhouse_console.log'
file_log_update = '/update_bot.log'
latest_release = '/greenhouseLatestRelease.id'
commit_id = '/greenhouseRepoCommit.id'
cloned_branch = '/greenhouseRepoBranch.name'
bot_dir = '/home/pi/scripts/TelegramBot/'
bot_backup = '/home/pi/backups/greenhouse.tgz'


if __name__ == '__main__':
    pass
