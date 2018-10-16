# My Greenhouse
*   Thanks for inspiring me [Stefan Weigert](https://www.stefan-weigert.de/php_loader/raspi.php) and [Felix Stern](https://tutorials-raspberrypi.de/automatisches-raspberry-pi-gewaechshaus-selber-bauen/)

	
#### Install Telegram app at mobile
*   [Web](https://telegram.org/)
*   [Ios](https://itunes.apple.com/de/app/telegram-messenger/id686449807?mt=8)
*   [Android](https://play.google.com/store/apps/details?id=org.telegram.messenger&hl=de)
*   Create bot
```
Name: 	ThK1220RealGreenhouse
TOKEN: 	************************************
ChatID:	*******************
```


#### Linux image
*   [raspbian lite latest](https://downloads.raspberrypi.org/raspbian_lite_latest)
*   [etcher](https://etcher.io/?ref=etcher_footer)

*   recommended Raspi image stretch lite w/o desktop
*   use e.g. etcher for flashing sd card
*   prepare sd card / flash image


#### Enable ssh access for terminal
*   e.g. mkdir ssh in dir boot on sd card

			
#### Configure static IP
*  [elektronik-kompendium](https://www.elektronik-kompendium.de/sites/raspberry-pi/1912151.htm) (I recommend variant 2)
```
sudo service dhcpcd status 
sudo service dhcpcd start // if not yet started 
sudo systemctl enable dhcpcd 
sudo nano /etc/[dhcpcd.conf](https://gitlab.bekast.de/tkaulke/greenhouse/blob/master/configs/dhcpcd.conf)
sudo reboot
```
			
**retest and doublecheck network conection and settings before executing next steps!!!!!**


#### Updates and configs
```
sudo apt-get update --yes && sudo apt-get upgrade --yes
sudo raspi-config
    Hostname:	greenhouse
    User:		pi
    Password:	******************
sudo rpi-update //update firmware
sudo reboot
```

	
#### Configure dyn dns client (ddclient)
*   [Dyn dns client with ssl](https://hexaju.wordpress.com/2013/03/20/raspberry-pi-as-dyndns-client-with-ssl/)
```
sudo apt-get update
sudo apt-get install libio-socket-ssl-perl
sudo apt-get install ddclient // ignore config let it empty e.g can be configured due next steps
```			
*   e.g. [FreeDNS](http://freedns.afraid.org)
*   update config accordingly the dns provider
```
sudo nano /etc/[ddclient.conf](https://gitlab.bekast.de/tkaulke/greenhouse/blob/master/configs/ddclient.conf)
    
other possible method could be e.g insert cron jobs as sudo
    0,5,10,15,20,25,30,35,40,45,50,55 * * * * sleep 31 ; wget -O - http://freedns.afraid.org/dynamic/update.php?******************************************** >> /tmp/freedns_greenhouse_my_to.log 2>&1 &
    3,8,13,18,23,28,33,38,43,48,53,58 * * * * sleep 44 ; wget -O - http://freedns.afraid.org/dynamic/update.php?******************************************** >> /tmp/freedns_greenhouse_chickenkiller_com.log 2>&1 &
```				


#### Configure remote ftp access to easier file transfer
*   [Raspberry Pi remote access](https://www.raspberrypi.org/documentation/remote-access/ftp.md)
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


#### Configure live stream
*   [Raspberry live stream 1](https://tutorials-raspberrypi.de/raspberry-pi-ueberwachungskamera-livestream-einrichten/)
*   [Raspberry live stream 2](https://www.datenreise.de/raspberry-pi-ueberwachungskamera-livestream/)
```	
sudo apt-get install motion -y
sudo nano /etc/motion/motion.conf   //additional: output_pictures off
sudo nano /etc/default/motion
mkdir /home/pi/Monitor
sudo chgrp motion /home/pi/Monitor
chmod g+rwx /home/pi/Monitor
sudo service motion start
```			


#### Configure port forwarding in router accordingly the dns and port settings
here [my live url](http://greenhouse.my.to:8082/)

					
#### Install required packages
```
sudo apt-get install build-essential python-dev python-pip python-smbus python-openssl git --yes //python
sudo pip install python-telegram-bot
sudo pip install telepot
```	

#### Add/create in pi user directory
*   [scripts/TelegramBot/greenhouse_telegrambot.py](https://gitlab.bekast.de/tkaulke/greenhouse/blob/master/scripts/greenhouse_telegrambot.py)
*   [scripts/TelegramBot/ext_greenhouse.py](https://gitlab.bekast.de/tkaulke/greenhouse/blob/master/scripts/ext_greenhouse.py)
*   **make sure they are executable and chown root:root**
	

#### Enable autostart
*   [how to](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#init)
*   Add the program to be run at startup to the init.d directory, insert **[telegrambot.sh](https://gitlab.bekast.de/tkaulke/greenhouse/blob/master/scripts/telegrambot.sh)** in **/etc/init.d** as root
```
sudo chmod +x telegrambot.sh
sudo update-rc.d telegrambot.sh defaults
sudo reboot
```