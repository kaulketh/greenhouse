#!/usr/bin/python
# -*- coding: utf-8 -*-
# script for panic mode
# author: Thomas Kaulke

import sys
import time
import telepot
import RPi.GPIO as GPIO
import os
import commands
import subprocess
import tempfile,os
import logging

logging.basicConfig(filename='./home/pi/scripts/TelegramBot/greenhouse.log', format='%(asctime)s %(levelname)-8s %(name)-25s %(message)s',datefmt='[%Y-%m-%d %H:%M:%S]', level=logging.INFO)

# def board pins/channels, refer hardware/rspi_gpio.info
GPIO.setmode(GPIO.BOARD)
TOMATO_01=29
TOMATO_02=31
TOMATO_03=33
CHILI_01=36
CHILI_02=38
CHILI_03=40

Vegetables = (TOMATO_01, TOMATO_02, TOMATO_03, CHILI_01, CHILI_02, CHILI_03)
Tomatoes = (TOMATO_01, TOMATO_02, TOMATO_03)
Chilis = (CHILI_01, CHILI_02, CHILI_03)

# comment if warnings required
GPIO.setwarnings(False)

# API Token          
apiToken = '<token>'


# time stamp
def timestamp():
        return time.strftime('[%d.%m.%Y %H:%M:%S]\n')

# live stream address
live = 'http://<url>'


# switch functions
def switch_on(pin):
    logging.info('switch on: ' + str(pin))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    return

def switch_off(pin):
    logging.info('switch off: ' + str(pin))
    GPIO.output(pin,GPIO.HIGH)
    GPIO.cleanup(pin)
    return

# water a group of targets
def water_on_group(group):
        for member in group:
                switch_on(member)
        return

# water off for a  group of targets
def water_off_group(group):
        for member in group:
                switch_off(member)
        return



# Assign output of os.system to a variable and prevent it from being displayed on the screen , https://stackoverflow.com/a/32433981
def readcmd(cmd):
    ftmp = tempfile.NamedTemporaryFile(suffix='.out', prefix='tmp', delete=False)
    fpath = ftmp.name
    if os.name=="nt":
        fpath = fpath.replace("/","\\") # forwin
    ftmp.close()
    os.system(cmd + " > " + fpath)
    data = ""
    with open(fpath, 'r') as file:
        data = file.read()
        file.close()
    os.remove(fpath)
    return data
	
# Assign default output (stdout 1 and stderr 2) to file and read in variable and get back
def readcmd_2(cmd):
    os.system(cmd +' > tblog.txt 2>&1')
    data = ""
    file = open('tblog.txt','r')
    data = file.read()
    file.close()
    return data

# kill the still running greenhouse bot script
PID1 = readcmd_2('ps -o pid,args -C python | awk \'/greenhouse_telegrambot.py/ { print $1 }\'')
logging.info('got PID of running greenhouse_telegrambot.py to kill it... %s' % PID1)
readcmd_2('kill -9 ' + PID1)

# Send message to defined API with given text(msg)
def sendmsg(msg):
    os.system('curl -s -k https://api.telegram.org/bot' + apiToken + '/sendMessage -d text="' + msg + '" -d chat_id=<chat_id>')
    logging.info('Message send: ' + msg)
    return


def handle(msg):

    chat_id = msg['chat']['id']
    command = msg['text']

    logging.info('Got command: %s' % command)

    # commands
    if command == '/RESTART':
        sendmsg(readcmd_2('sudo reboot'))
    elif command =='/all_on':
        sendmsg(timestamp()+'Water on for all.')
        water_on_group(Vegetables)
    elif command == '/all_off':
        sendmsg('All off.')
        water_off_group(Vegetables)
    elif command == '/tom_on':
        sendmsg(timestamp()+'Tomatoes on')
        water_on_group(Tomatoes)
    elif command == '/tom_off':
        sendmsg('All Tomatoes off again.')
        water_off_group(Tomatoes)
    elif command == '/chi_on':
        sendmsg(timestamp()+'Chilis on')
        water_on_group(Chilis)
    elif command == '/chi_off':
        sendmsg('All Chilis off again.')
        water_off_group(Chilis)
    elif command == '/kill':
        #clear monitor directory
        readcmd_2('rm -r /home/pi/Monitor/*')
        PID2 = readcmd_2('ps -o pid,args -C python | awk \'/ext_greenhouse.py/ { print $1 }\'')
        logging.info('got own PID to kill me by myself and also prepare the other bot for proper using: %s' % PID2)
        readcmd_2('python /home/pi/scripts/TelegramBot/greenhouse_telegrambot.py &')
        sendmsg('Process killed!\nEnable default bot... Run it with /start')
        readcmd_2('kill -9 ' + PID2)
    elif command == '/start':
        sendmsg('External input possible, bot is ready to use!')
    elif command == '/live':
        sendmsg(live)
    elif command == '/help':
        sendmsg('Usage and possible commands in special mode:\n/help - this info\n/RESTART - restart the whole RSBPi\n/kill - break this mode and restart default bot\n/all_on - water on for all\n/all_off - all off\n/tom_on - Water on for the tomatoes\n/tom_off - For tomatoes water off\n/chi_on - Water for the chilis on\n/chi_off - Water off for chilis\n/live - Live stream')
    else:
        sendmsg('Unknown in this mode...!\nPlease use /help for more information.')


bot = telepot.Bot(apiToken)
bot.message_loop(handle)
logging.info('I am listening...')

while 1:
    try:
        time.sleep(10)

    except KeyboardInterrupt:
        logging.warning('Program interrupted')
        exit()

    except:
        logging.error('Other error or exception occured!')


