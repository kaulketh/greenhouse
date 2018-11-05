#!/bin/sh
### BEGIN INIT INFO
# Provides:             telegrambot.sh
# Required-Start:       $start
# Required-Stop:        $shutdown
# Default-Start:        2 3 4 5
# Defaulst-Stop:        0 1 6
# Short-Description:    TelegramBots, please refer etc/init.d/telegrambot.sh
# Description:          Start Telegrambot /home/pi/scripts/TelegramBot/greenhouse_telegrambot.py
#                       to control rapsberrypi by admins mobile via telegram app.
#
### END INIT INFO

sleep 5
sudo python /home/pi/scripts/TelegramBot/greenhouse_telegrambot.py &
sleep 5
sudo python /home/pi/scripts/TelegramBot/gpio.check.py &