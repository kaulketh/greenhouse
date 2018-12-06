#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

from access import token, thk

newline = '\n'
cmd_prefix = '/'
cmd_restart = '{0}RESTART'.format(cmd_prefix)
cmd_update = cmd_prefix + 'UPDATE'
cmd_logrotate: str = '{0}LOG_ROTATE'.format(cmd_prefix)
cmd_help = '{0}help'.format(cmd_prefix)
cmd_all_on = '{0}all_on'.format(cmd_prefix)
cmd_all_off = '{0}all_off'.format(cmd_prefix)
cmd_group1_on = '{0}group1_on'.format(cmd_prefix)
cmd_group1_off = '{0}group1_off'.format(cmd_prefix)
cmd_group2_on = '{0}group2_on'.format(cmd_prefix)
cmd_group2_off = '{0}group2_off'.format(cmd_prefix)
cmd_group3_on = '{0}group3_on'.format(cmd_prefix)
cmd_group3_off = '{0}group3_off'.format(cmd_prefix)
cmd_live = '{0}live'.format(cmd_prefix)
cmd_kill = '{0}kill'.format(cmd_prefix)

msg_help = 'Usage and possible commands in special mode:{0}{1} - this info{2}{3} - restart the whole RSBPi{4}{5} - ' \
           'force update{6}{7} - force archiving and cleaning of log files{8}{9} - stop this mode and restart default ' \
           'bot{10}{11}- switch all on{12}{13}- switch all off{14}{15}- switch group 1 on{16}{17}- switch group 1 ' \
           'off{18}{19}- switch group 2 on{20}{21}- switch group 2 off{22}{23}- switch group 3 on{24}{25}- switch ' \
           'group 3 off{26}{27} - Live stream'.format(
            newline, cmd_help, newline, cmd_restart, newline, cmd_update, newline, cmd_logrotate, newline, cmd_kill,
            cmd_all_on, newline, newline, cmd_all_off, newline, cmd_group1_on, newline, cmd_group1_off, newline,
            cmd_group2_on, newline, cmd_group2_off, newline, cmd_group3_on, newline, cmd_group3_off, newline, cmd_live)

msg_unknown = 'Unknown in this mode...!\nPlease use /help for more information.'
msg_update = 'Update possibility checked manually, info is available in separate log file.'

tmp_file = 'cmd.tmp'
del_tmp = 'rm -r ' + tmp_file

get_pid1 = 'ps -o pid,args -C python | awk \'/greenhouse_telegrambot.py/ { print $1 }\''
get_pid2 = 'ps -o pid,args -C python | awk \'/ext_greenhouse.py/ { print $1 }\''
restart_bot = 'python /home/pi/scripts/TelegramBot/greenhouse_telegrambot.py &'
update_bot = 'bash /home/pi/scripts/TelegramBot/update_bot.sh '+ str(token) + ' ' + str(thk) +' &'
logrotate_bot = 'logrotate -f /etc/logrotate.conf &' 
