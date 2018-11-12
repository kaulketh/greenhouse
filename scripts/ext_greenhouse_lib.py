#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke
from access import acces_token_to_repository

newline = '\n'
cmd_prefix = '/'
cmd_restart = cmd_prefix + 'RESTART'
cmd_update = cmd_prefix + 'UPDATE'
cmd_help = cmd_prefix + 'help'
cmd_all_on = cmd_prefix + 'all_on'
cmd_all_off = cmd_prefix + 'all_off'
cmd_group1_on = cmd_prefix + 'group1_on'
cmd_group1_off = cmd_prefix + 'group1_off'
cmd_group2_on = cmd_prefix + 'group2_on'
cmd_group2_off = cmd_prefix + 'group2_off'
cmd_group3_on = cmd_prefix + 'group3_on'
cmd_group3_off = cmd_prefix + 'group3_off'
cmd_live = cmd_prefix + 'live'
cmd_kill = cmd_prefix + 'kill'

msg_help = 'Usage and possible commands in special mode:' + \
    newline + cmd_help + ' - this info' + \
    newline + cmd_restart + ' - restart the whole RSBPi' + \
    newline + cmd_update + ' - update bot application' + \
    newline + cmd_kill + ' - stop this mode and restart default bot' + \
    newline + cmd_all_on + '- switch all on' + \
    newline + cmd_all_off + '- switch all off' + \
    newline + cmd_group1_on + '- switch group 1 on' + \
    newline + cmd_group1_off + '- switch group 1 off' + \
    newline + cmd_group2_on + '- switch group 2 on' + \
    newline + cmd_group2_off + '- switch group 2 off' + \
    newline + cmd_group3_on + '- switch group 3 on' + \
    newline + cmd_group3_off + '- switch group 3 off' + \
    newline + cmd_live + ' - Live stream'

msg_unknown = 'Unknown in this mode...!\nPlease use /help for more information.'

tmp_file = 'cmd.tmp'
del_tmp = 'rm -r ' + tmp_file
clear_monitor = 'rm -r /home/pi/Monitor/*'
get_pid1 = 'ps -o pid,args -C python | awk \'/greenhouse_telegrambot.py/ { print $1 }\''
get_pid2 = 'ps -o pid,args -C python | awk \'/ext_greenhouse.py/ { print $1 }\''
restart_bot = 'python /home/pi/scripts/TelegramBot/greenhouse_telegrambot.py &'
update_bot = 'bash /home/pi/scripts/TelegramBot/update_bot.sh ' + acces_token_to_repository + ' &'
