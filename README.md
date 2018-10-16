# Greenhouse

## inspired by:
*   [Stefan Weigert](https://www.stefan-weigert.de/php_loader/raspi.php)
*    [Automatisches Raspberry Pi Gewächshaus selber bauen](https://tutorials-raspberrypi.de/automatisches-raspberry-pi-gewaechshaus-selber-bauen/)

	
## Install Telegram App at mobile
## Create a bot
	* Name: 	ThK1220RealGreenhouse
	* TOKEN: 	************************************
	* ChatID:	*******************

## install linux image
https://downloads.raspberrypi.org/raspbian_lite_latest
https://etcher.io/?ref=etcher_footer

*   recommended Raspi image stretch lite w/o desktop
*   use e.g. etcher for flashing sd card
*   prepare sd card / flash image

### enable ssh access for terminal
*   e.g. mkdir ssh in dir boot on sd card
			
### configure static IP //here 192.168.0.100
*   https://www.elektronik-kompendium.de/sites/raspberry-pi/1912151.htm (I recommend variant 2)
```
sudo service dhcpcd status 
sudo service dhcpcd start // if not yet started 
sudo systemctl enable dhcpcd 
sudo nano /etc/dhcpcd.conf 
    interface eth0
    static ip_address=192.168.0.100/24
    static routers=192.168.0.1
    static domain_name_servers=192.168.0.254
sudo reboot
```
			
**retest and doublecheck network conection and settings before executing next steps!!!!!**

### make updates and config
```
sudo apt-get update --yes && sudo apt-get upgrade --yes
sudo raspi-config
    Hostname:	greenhouse
    User:		pi
    Password:	******************
sudo rpi-update //update firmware
sudo reboot
```
	
### configure dyn dns client (ddclient)
*   https://hexaju.wordpress.com/2013/03/20/raspberry-pi-as-dyndns-client-with-ssl/
```
sudo apt-get update
sudo apt-get install libio-socket-ssl-perl
sudo apt-get install ddclient // ignore config let it empty e.g can be configured due next steps
```			
*   e.g. http://freedns.afraid.org
*   update config accordingly the dns provider
```
sudo nano /etc/ddclient.conf
    syslog=yes
    daemon=600
    ssl=yes
    protocol=freedns	
    use=web, web=checkip.dyndns.com, web-skip='Current IP Address: '
    server=freedns.afraid.org
    login=--------------
    password='*************'
    greenhouse.my.to
    greenhouse.chickenkiller.com
	
other possible method could be e.g insert cron jobs as sudo
    0,5,10,15,20,25,30,35,40,45,50,55 * * * * sleep 31 ; wget -O - http://freedns.afraid.org/dynamic/update.php?******************************************** >> /tmp/freedns_greenhouse_my_to.log 2>&1 &
    3,8,13,18,23,28,33,38,43,48,53,58 * * * * sleep 44 ; wget -O - http://freedns.afraid.org/dynamic/update.php?******************************************** >> /tmp/freedns_greenhouse_chickenkiller_com.log 2>&1 &
```				

### configure remote ftp access //better to transfer files
*   https://www.raspberrypi.org/documentation/remote-access/ftp.md
```
sudo apt-get install pure-ftpd
sudo groupadd ftpgroup
sudo useradd ftpuser -g ftpgroup -s /sbin/nologin -d /dev/null
sudo mkdir /home/pi/FTP
sudo chown -R ftpuser:ftpgroup /home/pi/FTP
sudo pure-pw useradd upload -u ftpuser -g ftpgroup -d /home/pi/FTP -m
sudo pure-pw mkdb
sudo ln -s /etc/pure-ftpd/conf/PureDB /etc/pure-ftpd/auth/60puredb 
sudo service pure-ftpd restart
```

### configure live stream
*   https://tutorials-raspberrypi.de/raspberry-pi-ueberwachungskamera-livestream-einrichten/
*   https://www.datenreise.de/raspberry-pi-ueberwachungskamera-livestream/
```	
sudo apt-get install motion -y
sudo nano /etc/motion/motion.conf   //additional: output_pictures off
sudo nano /etc/default/motion
mkdir /home/pi/Monitor
sudo chgrp motion /home/pi/Monitor
chmod g+rwx /home/pi/Monitor
sudo service motion start
```			

### configure port forwarding in router accordingly the dns and port settings
here http://greenhouse.my.to:8082/
					
### install required packages
```
sudo apt-get install build-essential python-dev python-pip python-smbus python-openssl git --yes //python
sudo pip install python-telegram-bot
sudo pip install telepot
```	
	
### add/create in pi user directory
*   scripts/TelegramBot/greenhouse_telegrambot.py
*   scripts/TelegramBot/ext_greenhouse.py
*   **make sure they are executable and chown root:root**
	
	
### enable autostart of custom scripts
*   https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#init
*   Add the program to be run at startup to the init.d directory, insert **telegrambot.sh** in **/etc/init.d** as root
```
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
			
sudo chmod +x telegrambot.sh
sudo update-rc.d telegrambot.sh defaults
sudo reboot
```