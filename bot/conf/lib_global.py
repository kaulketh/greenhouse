#!/usr/bin/python
# -*- coding: utf-8 -*-
# lib_global.py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

import sys

empty = ''
space = ' '
colon_space = ': '
pipe_space = '| '
line_break = '\n'

"""
timeout if no user activity 
"""
timeout = 120


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

file_paths = {
        'file_log_greenhouse': '/greenhouse.log',
        'file_log_debug': '/greenhouse_console.log',
        'file_log_update': '/update_bot.log',
        'latest_release': '/greenhouseLatestRelease.id',
        'commit_id': '/greenhouseRepoCommit.id',
        'cloned_branch': '/greenhouseRepoBranch.name',
        'bot_dir': '/home/pi/scripts/TelegramBot/',
        'bot_backup': '/home/pi/backups/greenhouse.tgz'
    }

file_log_greenhouse = file_paths['file_log_greenhouse']
file_log_debug = file_paths['file_log_debug']
file_log_update = file_paths['file_log_update']
latest_release = file_paths['latest_release']
commit_id = file_paths['commit_id']
cloned_branch = file_paths['cloned_branch']
bot_dir = file_paths['bot_dir']
bot_backup = file_paths['bot_backup']


def get_path(var):
    if file_paths.__contains__(var):
        print(file_paths[var])


if __name__ == '__main__':
    get_path(sys.argv[1])
