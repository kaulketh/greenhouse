# My Greenhouse
> Thank you for inspiring me, [Stefan Weigert](https://www.stefan-weigert.de/php_loader/raspi.php) and [Felix Stern](https://tutorials-raspberrypi.de/automatisches-raspberry-pi-gewaechshaus-selber-bauen/)

	
### 1. Telegram app
##### Install the app and create bot

```
Name: 	ThK1220RealGreenhouse
TOKEN: 	<api_token>
ChatID:	<chat_id>
```
* [Web](https://telegram.org/)
* [Ios](https://itunes.apple.com/de/app/telegram-messenger/id686449807?mt=8)
* [Android](https://play.google.com/store/apps/details?id=org.telegram.messenger&hl=de)


### 2. Raspberry Pi OS image
* download [latest stretch lite w/o desktop](https://downloads.raspberrypi.org/raspbian_lite_latest) 
* prepare sd card / flash image, e.g. use [Etcher](https://etcher.io/?ref=etcher_footer) 
* _**enable SSH access**_ 
    * As of the November 2016 release, Raspbian has the SSH server disabled by default. You will have to enable it manually. 
    * For headless setup, SSH can be enabled by placing a file named "ssh", without any extension, onto the boot partition of the SD card.


### 3. Boot raspi and connect via ssh

			
### 4. Configure (static) IP
##### adapt /etc/[dhcpcd.conf](configs/dhcpcd.conf)

```
sudo service dhcpcd status 
sudo service dhcpcd start // if not yet started 
sudo systemctl enable dhcpcd 
sudo nano /etc/dhcpcd.conf
sudo reboot
```
* [how-to at elektronik-kompendium](https://www.elektronik-kompendium.de/sites/raspberry-pi/1912151.htm) (I recommend variant 2)
* [also helpful, how-to for wlan](https://unix.stackexchange.com/questions/92799/connecting-to-wifi-network-through-command-line)
* [another how-to at elektronik-kompendium](https://www.elektronik-kompendium.de/sites/raspberry-pi/1912221.htm)
 

_**Retest and doublecheck network conection and settings before executing next steps!!!!!**_



### 5. Make updates and adapt main config
```
sudo apt-get update --yes && sudo apt-get upgrade --yes
sudo raspi-config
    Hostname:	greenhouse
    User:		pi
    Password:	******************
sudo rpi-update //update firmware
sudo reboot
```

	
### 6. Install and configure dyn dns client (ddclient)
```
sudo apt-get update
sudo apt-get install libio-socket-ssl-perl
sudo apt-get install ddclient // ignore config let it empty e.g can be configured due next steps
```			
##### use e.g. [FreeDNS](http://freedns.afraid.org) and update [ddclient.conf](configs/ddclient.conf) accordingly the dns provider
```
sudo nano /etc/ddclient.conf
```	
##### other possible method could be e.g insert crontabs
```	
    0,5,10,15,20,25,30,35,40,45,50,55 * * * * sleep 31 ; wget -O - http://freedns.afraid.org/dynamic/update.php?******************************************** >> /tmp/freedns_greenhouse_my_to.log 2>&1 &
    3,8,13,18,23,28,33,38,43,48,53,58 * * * * sleep 44 ; wget -O - http://freedns.afraid.org/dynamic/update.php?******************************************** >> /tmp/freedns_greenhouse_chickenkiller_com.log 2>&1 &
```				
* [how-to dyndns client with ssl](https://hexaju.wordpress.com/2013/03/20/raspberry-pi-as-dyndns-client-with-ssl/)
 


### 7. Install and configure remote ftp access to easier file transfer
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
* [how-to remote access](https://www.raspberrypi.org/documentation/remote-access/ftp.md)
 


### 8. Configure the live stream
##### install motion and update /etc/motion/[motion.conf](configs/motion.conf)
```	
sudo apt-get install motion -y
sudo nano /etc/motion/motion.conf   //additional: output_pictures off
sudo nano /etc/default/motion
mkdir /home/pi/Monitor
sudo chgrp motion /home/pi/Monitor
chmod g+rwx /home/pi/Monitor
sudo service motion start
```			
* [How-to 1 live stream](https://tutorials-raspberrypi.de/raspberry-pi-ueberwachungskamera-livestream-einrichten/)
* [How-to 2 live stream](https://www.datenreise.de/raspberry-pi-ueberwachungskamera-livestream/)


### 9. Configure port forwarding in router accordingly the dns and port settings
##### [my live url](http://greenhouse.my.to:8082/)

					
### 10. Install required packages (python, python-telegram-bot, telepot and wiringpi)
```
sudo apt-get install build-essential python-dev python-pip python-smbus python-openssl git --yes //python
sudo pip install python-telegram-bot
sudo pip install telepot
```

##### First check that wiringPi is not already installed.
```
gpio -v
```

##### If you get something, then you have it already installed. The next step is to work out if it’s installed via a standard package or from source. If you installed it from source, then you know what you’re doing – carry on – but if it’s installed as a package, you will need to remove the package first. To do this:
```
sudo apt-get purge wiringpi
hash -r
```

##### WiringPi is maintained under GIT for ease of change tracking. If required to install do it like described as followed.
```
sudo apt-get install git-core
sudo apt-get update
sudo apt-get upgrade
cd git
git clone git://git.drogon.net/wiringPi
cd ~/wiringPi
git pull origin
cd ~/wiringPi
./build
```

* [how to to install wiringpi](http://wiringpi.com/download-and-install/)
	
### 11. Add/create python scripts in pi user directory under scripts/TelegramBot
_**Make them executable and chown root:root!**_
* access.py - external file, content will not provided, contains api token, chat IDs and other sensitive data
* [greenhouse_config.py](scripts/greenhouse_config.py) - contains settings and properties
* [greenhouse_telegrambot.py](scripts/greenhouse_telegrambot.py) - main bot
* [greenhouse_lib_german.py](scripts/greenhouse_lib_german.py) - file with constants, contains strings for descriptions and messages
* [ext_greenhouse.py](scripts/ext_greenhouse.py) - extended bot
* [ext_greenhouse_lib.py](scripts/ext_greenhouse_lib.py) - some constants, contains strings for commands and texts
* [greenhouse_lib_english.py](scripts/greenhouse_lib_english.py) - if required, same like German version, if used adapt imports!
* [gpio_check.py](scripts/gpio_check.py) - to check state of GPIOs and logs if state == low, is added in autostart in telegrambot.sh
* [update_bot.sh](scripts/update_bot.sh) - to updates all scripts from the repository by using last commit ID and a git access token
   


### 12. Enable autostart of the bot application
##### Add the program as service. To enable autostart add it to the init.d directory, insert [telegrambot.sh](scripts/telegrambot.sh) in **/etc/init.d** as root and execute commands as followed.

```
sudo chmod +x telegrambot.sh
sudo update-rc.d telegrambot.sh defaults
sudo reboot
```

* how to](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#init)


### 13. Additional functionalities
##### Add crontabs

```
# update check every 10 minutes
0,10,20,30,40,50 * * * * bash /home/pi/scripts/TelegramBot/update_bot.sh <access token repository> <chat id> <api token>
	
# update check every hour
0 * * * * bash /home/pi/scripts/TelegramBot/update_bot.sh <access token repository> <chat id> <api token>

# backup bot every day at 1:30AM
30 1 * * * tar -zcf /home/pi/backups/greenhouse.tgz --exclude='*.pyc' /home/pi/scripts/TelegramBot/

# also move log backups to backup folder
31 1 * * * mv -v /*.gz /home/pi/backups/
```

##### Add logrotate to compress and clear log files
* see http://znil.net/index.php/Logfiles_in_Logrotate_aufnehmen_-_automatisches_packen,_rotieren_und_leeren_von_Logs 

```
sudo nano /etc/logrotate.conf
```

```
/update_bot.log {
	missingok
	daily
	rotate 1
	compress
	dateext
	create 644 root root
}

/greenhouse.log {
	missingok
	daily
	rotate 1
	compress
	dateext
	create 644 root root
}
```	
