# My Greenhouse
> Thank you for inspiring me, [Stefan Weigert](https://www.stefan-weigert.de/php_loader/raspi.php) and [Felix Stern](https://tutorials-raspberrypi.de/automatisches-raspberry-pi-gewaechshaus-selber-bauen/)

	
#### 1. Telegram app
install the app and create bot
```
Name: 	ThK1220RealGreenhouse
TOKEN: 	<api_token>
ChatID:	<chat_id>
```
* [Web](https://telegram.org/)
* [Ios](https://itunes.apple.com/de/app/telegram-messenger/id686449807?mt=8)
* [Android](https://play.google.com/store/apps/details?id=org.telegram.messenger&hl=de)


#### 2. Raspberry Pi OS image
* download [latest stretch lite w/o desktop](https://downloads.raspberrypi.org/raspbian_lite_latest) 
* prepare sd card / flash image, e.g. use [Etcher](https://etcher.io/?ref=etcher_footer) 
* _**enable SSH access**_ (e.g. mkdir ssh in dir boot on sd card)


#### 3. Boot raspi and connect via ssh

			
#### 4. Configure (static) IP
adapt /etc/[dhcpcd.conf](configs/dhcpcd.conf)
```
sudo service dhcpcd status 
sudo service dhcpcd start // if not yet started 
sudo systemctl enable dhcpcd 
sudo nano /etc/dhcpcd.conf
sudo reboot
```
* [elektronik-kompendium](https://www.elektronik-kompendium.de/sites/raspberry-pi/1912151.htm) (I recommend variant 2)
 

_**Retest and doublecheck network conection and settings before executing next steps!!!!!**_



#### 5. Make updates and adapt main config
```
sudo apt-get update --yes && sudo apt-get upgrade --yes
sudo raspi-config
    Hostname:	greenhouse
    User:		pi
    Password:	******************
sudo rpi-update //update firmware
sudo reboot
```

	
#### 6. Install and configure dyn dns client (ddclient)
```
sudo apt-get update
sudo apt-get install libio-socket-ssl-perl
sudo apt-get install ddclient // ignore config let it empty e.g can be configured due next steps
```			
use e.g. [FreeDNS](http://freedns.afraid.org) and update [ddclient.conf](configs/ddclient.conf) accordingly the dns provider
```
sudo nano /etc/ddclient.conf
```	
other possible method could be e.g insert crontabs
```	
    0,5,10,15,20,25,30,35,40,45,50,55 * * * * sleep 31 ; wget -O - http://freedns.afraid.org/dynamic/update.php?******************************************** >> /tmp/freedns_greenhouse_my_to.log 2>&1 &
    3,8,13,18,23,28,33,38,43,48,53,58 * * * * sleep 44 ; wget -O - http://freedns.afraid.org/dynamic/update.php?******************************************** >> /tmp/freedns_greenhouse_chickenkiller_com.log 2>&1 &
```				
* [Dyn dns client with ssl](https://hexaju.wordpress.com/2013/03/20/raspberry-pi-as-dyndns-client-with-ssl/)
 


#### 7. Install and configure remote ftp access to easier file transfer
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
* [Raspberry Pi remote access](https://www.raspberrypi.org/documentation/remote-access/ftp.md)
 


#### 8. Configure the live stream
install motion and update /etc/motion/[motion.conf](configs/motion.conf)
```	
sudo apt-get install motion -y
sudo nano /etc/motion/motion.conf   //additional: output_pictures off
sudo nano /etc/default/motion
mkdir /home/pi/Monitor
sudo chgrp motion /home/pi/Monitor
chmod g+rwx /home/pi/Monitor
sudo service motion start
```			
* [Raspberry live stream 1](https://tutorials-raspberrypi.de/raspberry-pi-ueberwachungskamera-livestream-einrichten/)
* [Raspberry live stream 2](https://www.datenreise.de/raspberry-pi-ueberwachungskamera-livestream/)


#### 9. Configure port forwarding in router accordingly the dns and port settings
[my live url](http://greenhouse.my.to:8082/)

					
##### 10. Install required packages (python, python-telegram-bot and telepot)
```
sudo apt-get install build-essential python-dev python-pip python-smbus python-openssl git --yes //python
sudo pip install python-telegram-bot
sudo pip install telepot
```	

#### 11. Add/create python scripts in pi user directory
_**Make them executable and chown root:root!**_
* [scripts/TelegramBot/greenhouse_telegrambot.py](scripts/greenhouse_telegrambot.py)
* [scripts/TelegramBot/ext_greenhouse.py](scripts/ext_greenhouse.py)
* [scripts/TelegramBot/greenhouse_config.py](scripts/greenhouse_config.py) contains settings
* [scripts/TelegramBot/greenhouse_strings_german.py](scripts/greenhouse_strings_german.py) contains strings for descriptions and messages
* [scripts/TelegramBot/greenhouse_strings_english.py](scripts/greenhouse_strings_english.py) if required, same like German version, if used adapt imports!
* [scripts/TelegramBot/access.py] external file, contains api token, chat IDs and other sensitive data

#### 12. Enable autostart
Add the program to be run at startup to the init.d directory, insert **[telegrambot.sh](scripts/telegrambot.sh)** in **/etc/init.d** as root
```
sudo chmod +x telegrambot.sh
sudo update-rc.d telegrambot.sh defaults
sudo reboot
```
* [how to](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#init)
