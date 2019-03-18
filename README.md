# My Greenhouse
> Control a greenhouse by using Telegram app and a Raspberry Pi.
> I did not reinvent the wheel.

> Thank you for inspiring me, [Stefan Weigert](https://www.stefan-weigert.de/php_loader/raspi.php) and [Felix Stern](https://tutorials-raspberrypi.de/automatisches-raspberry-pi-gewaechshaus-selber-bauen/)

---
> ![release](https://img.shields.io/github/release/kaulketh/greenhouse.svg?color=darkblue) ![size](https://img.shields.io/github/repo-size/kaulketh/greenhouse.svg?color=blue) ![commit](https://img.shields.io/github/last-commit/kaulketh/greenhouse.svg?color=darkviolet) ![platform](https://img.shields.io/badge/platform-linux-blue.svg?color=yellow) ![languages](https://img.shields.io/github/languages/count/kaulketh/greenhouse.svg?color=yellowgreen) ![coverage](https://img.shields.io/github/languages/top/kaulketh/greenhouse.svg?color=darkgreen&style=flat) ![python](https://img.shields.io/pypi/pyversions/telepot.svg?color=darkgreen&style=flat) [![license](https://img.shields.io/github/license/kaulketh/greenhouse.svg?color=darkred)](https://unlicense.org/) 

> This repository is used to gather and show information and experiences during the building of a smart control possibility.
> All code is written or adapted by myself and w/o any copyrights. I have tried to use no copyright protected stuff.
> Almost everything published already exists, to be found on the net, and was adapted and used only by me accordingly.

> And please excuse the mistakes made and violations of any conventions, I am new to this matter.
> Do not be afraid to correct or improve me and inform me accordingly.


### Table of Contents
- [Installation and usage](#Installation-and-usage)
- [Telegram app](#telegram-app)
- Raspberry Pi requirements
    - [Raspberry Pi OS](#raspberry-pi-os-image)
    - [First boot](#boot-raspi-and-connect-via-ssh)
    - [Configure IP](#configure-static-ip)
    - [Updates and main config](#make-updates-and-adapt-main-config)
    - [Dyn dns client](#install-and-configure-dyn-dns-client-ddclient)
    - [Remote ftp access](#install-and-configure-remote-ftp-if-required)
    - [Live stream](#configure-the-live-stream)
- [Router port forwarding](#configure-port-forwarding-in-router-accordingly-the-dns-and-port-settings)
- [Required packages](#install-required-packages-python-python-telegram-bot-python-pip-telepot-and-wiringpi)
- [Add/create scripts](#add-scripts-in-pi-user-directory)
- [Autostart](#enable-autostart-of-the-bot-application)
- [Additional](#additional-functionality)
- [Hardware](https://github.com/kaulketh/greenhouse/blob/master/hardware/HARDWARE.md)
- [License](#License)

---
### Installation and usage
> Currently no installation routine is planned.
> Feel free to use, adapt, download or copy all the published stuff.
> Main programming language is Python and shell scripting is used also. 

	
### Telegram app
##### Install the app and create bot

```
Name: 	ThK1220RealGreenhouse
TOKEN: 	<api_token>
ChatID:	<chat_id>
```

* [Web](https://telegram.org/)
* [Ios](https://itunes.apple.com/de/app/telegram-messenger/id686449807?mt=8)
* [Android](https://play.google.com/store/apps/details?id=org.telegram.messenger&hl=de)

---

### Raspberry Pi OS image
* download [latest stretch lite w/o desktop](https://downloads.raspberrypi.org/raspbian_lite_latest) 
* prepare sd card / flash image, e.g. use [Etcher](https://etcher.io/?ref=etcher_footer) 
* _**enable SSH access**_ 
    * As of the November 2016 release, Raspbian has the SSH server disabled by default. You will have to enable it manually. 
    * For headless setup, SSH can be enabled by placing a file named "ssh", without any extension, onto the boot partition of the SD card.

---

### Boot raspi and connect via ssh

---
			
### Configure (static) IP
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

---

### Make updates and adapt main config

```
sudo apt-get update --yes && sudo apt-get upgrade --yes
sudo raspi-config
    Hostname:	greenhouse
    User:		pi
    Password:	******************
sudo rpi-update //update firmware
sudo reboot
```
---
### Install and configure dyn dns client (ddclient)
#### ignore config let it empty e.g can be configured due next steps
```
sudo apt-get update
sudo apt-get install libio-socket-ssl-perl
sudo apt-get install ddclient
```

#### use e.g. [FreeDNS](http://freedns.afraid.org) and update [ddclient.conf](configs/ddclient.conf) accordingly the dns provider

```

sudo nano /etc/ddclient.conf

```


##### other possible method could be e.g insert crontabs
```
0,5,10,15,20,25,30,35,40,45,50,55 * * * * sleep 31 ; wget -O - http://freedns.afraid.org/dynamic/update.php?******************************************** >> /tmp/freedns_greenhouse_my_to.log 2>&1 &
3,8,13,18,23,28,33,38,43,48,53,58 * * * * sleep 44 ; wget -O - http://freedns.afraid.org/dynamic/update.php?******************************************** >> /tmp/freedns_greenhouse_chickenkiller_com.log 2>&1 &
```
* [how-to dyndns client with ssl](https://hexaju.wordpress.com/2013/03/20/raspberry-pi-as-dyndns-client-with-ssl/)
 
---

### Install and configure remote ftp if required
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
 
---
### Configure the live stream
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

---

### Configure port forwarding in router accordingly the dns and port settings
##### [my live url](http://greenhouse.my.to:8082/)

---					
### Install required packages (python, python-telegram-bot, python-pip, telepot and wiringpi)
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

---

### Add scripts in pi user directory
##### e.g in this case in scripts/TelegramBot

_**Make them executable and chown root:root!**_
* access.py - external file, content will not provided, contains api token, chat IDs and other sensitive data
* [greenhouse_config.py](bot/conf/greenhouse_config.py) - settings and properties
* [greenhouse.py](bot/greenhouse.py) - main bot
* [lib_global.py](bot/conf/lib_global.py) - global constants and settings 
* [lib_german.py](bot/conf/lib_german.py) - constants, strings for descriptions and messages
* [ext_greenhouse.py](bot/ext_greenhouse.py) - extended bot
* [lib_ext_greenhouse.py](bot/conf/lib_ext_greenhouse.py) - constants, strings for commands and texts
* [lib_english.py](bot/conf/lib_english.py) - English translation of German version, is set in global lib
* [gpio_check.py](bot/peripherals/gpio_check.py) - to check state of GPIOs and logs state, in case it is wished
* [update_bot.sh](bot/update_bot.sh) - to updates all scripts from this repository by using last commit and branch
   
---
### Enable autostart of the bot application
##### Add the program as service. To enable autostart add it to the init.d directory, insert [telegrambot.sh](bot/telegrambot.sh) in **/etc/init.d** as root and execute commands as followed.

```
sudo chmod +x telegrambot.sh
sudo update-rc.d telegrambot.sh defaults
sudo reboot
```

* [how to](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#init)

---

### Additional functionality
##### Add as required or wished

##### Crontabs examples

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

##### Logrotate to compress and clear log files
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
---
## License

[![license](https://img.shields.io/github/license/kaulketh/greenhouse.svg?color=darkred)](https://unlicense.org/)

- **[License](https://github.com/kaulketh/greenhouse/blob/master/LICENSE    )**
