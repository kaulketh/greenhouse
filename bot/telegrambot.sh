#!/bin/sh
# enable autostart
# author: Thomas Kaulke, kaulketh@gmail.com

### BEGIN INIT INFO
# Provides:             telegrambot.sh
# Required-Start:       $start
# Required-Stop:        $shutdown
# Default-Start:        2 3 4 5
# Defaulst-Stop:        0 1 6
# Short-Description:    Greenhouse bot start script, please refer etc/init.d/telegrambot.sh
# Description:          Start /home/pi/scripts/TelegramBot/greenhouse.py
#                       to control rapsberrypi by admins mobile via telegram app.
#
### END INIT INFO

sudo hddledPi -d -p 4 &
sudo netledPi -d -p 5 &
sleep 2
sudo modprobe bcm2835-v4l2 && sleep 1.5 && sudo service motion start && sleep 1.5 && sudo service motion stop &
sleep 2
sudo python /home/pi/scripts/TelegramBot/greenhouse.py & sleep 1.5 && sudo python /home/pi/scripts/TelegramBot/peripherals/oled/display.py &

