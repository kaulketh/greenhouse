#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: sd582 - https://forum-raspberrypi.de/user/24027-sd582/
# http://www.sc2web.net/Downloads/tm1637.zip
# https://forum-raspberrypi.de/forum/thread/15042-led-4-segment-i2c-display/?postID=137411#post137411
# +
# author: KyleKing - https://github.com/KyleKing
# https://github.com/timwaizenegger/raspberrypi-examples/blob/master/actor-led-7segment-4numbers/tm1637.py

import sys
import os
import time
import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode(IO.BCM)

HexDigits = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f, 0x77, 0x7c, 0x39, 0x5e, 0x79, 0x71]

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_TYPICAL = 2
BRIGHT_HIGHEST = 7
OUTPUT = IO.OUT
INPUT = IO.IN
LOW = IO.LOW
HIGH = IO.HIGH


class TM1637:
    __doublePoint = False
    __Clkpin = 0
    __Datapin = 0
    __brightnes = BRIGHT_TYPICAL;
    __currentData = [0, 0, 0, 0];

    def __init__(self, pinClock, pinData, brightnes):
        self.__Clkpin = pinClock
        self.__Datapin = pinData
        self.__brightnes = brightnes;
        IO.setup(self.__Clkpin, OUTPUT)
        IO.setup(self.__Datapin, OUTPUT)

    # end  __init__

    def Clear(self):
        b = self.__brightnes;
        point = self.__doublePoint;
        self.__brightnes = 0;
        self.__doublePoint = False;
        data = [0x7F, 0x7F, 0x7F, 0x7F];
        self.Show(data);
        self.__brightnes = b;  # restore saved brightnes
        self.__doublePoint = point;

    # end  Clear

    def Show(self, data):
        for i in range(0, 4):
            self.__currentData[i] = data[i];

        self.start();
        self.writeByte(ADDR_AUTO);
        self.stop();
        self.start();
        self.writeByte(STARTADDR);
        for i in range(0, 4):
            self.writeByte(self.coding(data[i]));
        self.stop();
        self.start();
        self.writeByte(0x88 + self.__brightnes);
        self.stop();

    # end  Show

    def Show1(self, DigitNumber, data):  # show one Digit (number 0...3)
        if (DigitNumber < 0 or DigitNumber > 3):
            return;  # error

        self.__currentData[DigitNumber] = data;

        self.start();
        self.writeByte(ADDR_FIXED);
        self.stop();
        self.start();
        self.writeByte(STARTADDR | DigitNumber);
        self.writeByte(self.coding(data));
        self.stop();
        self.start();
        self.writeByte(0x88 + self.__brightnes);
        self.stop();

    # end  Show1

    def SetBrightnes(self, brightnes):  # brightnes 0...7
        if (brightnes > 7):
            brightnes = 7;
        elif (brightnes < 0):
            brightnes = 0;

        if (self.__brightnes != brightnes):
            self.__brightnes = brightnes;
            self.Show(self.__currentData);

    # end if
    # end  SetBrightnes

    def ShowDoublepoint(self, on):  # shows or hides the doublepoint
        if (self.__doublePoint != on):
            self.__doublePoint = on;
            self.Show(self.__currentData);

    # end if
    # end  ShowDoublepoint

    def writeByte(self, data):
        for i in range(0, 8):
            IO.output(self.__Clkpin, LOW)
            if (data & 0x01):
                IO.output(self.__Datapin, HIGH)
            else:
                IO.output(self.__Datapin, LOW)
            data = data >> 1
            IO.output(self.__Clkpin, HIGH)
        # endfor

        # wait for ACK
        IO.output(self.__Clkpin, LOW)
        IO.output(self.__Datapin, HIGH)
        IO.output(self.__Clkpin, HIGH)
        IO.setup(self.__Datapin, INPUT)

        while (IO.input(self.__Datapin)):
            time.sleep(0.001)
            if (IO.input(self.__Datapin)):
                IO.setup(self.__Datapin, OUTPUT)
                IO.output(self.__Datapin, LOW)
                IO.setup(self.__Datapin, INPUT)
        # endif
        # endwhile
        IO.setup(self.__Datapin, OUTPUT)

    # end writeByte

    def start(self):
        IO.output(self.__Clkpin, HIGH)  # send start signal to TM1637
        IO.output(self.__Datapin, HIGH)
        IO.output(self.__Datapin, LOW)
        IO.output(self.__Clkpin, LOW)

    # end start

    def stop(self):
        IO.output(self.__Clkpin, LOW)
        IO.output(self.__Datapin, LOW)
        IO.output(self.__Clkpin, HIGH)
        IO.output(self.__Datapin, HIGH)

    # end stop

    def coding(self, data):
        if (self.__doublePoint):
            pointData = 0x80
        else:
            pointData = 0;

        if (data == 0x7F):
            data = 0
        else:
            data = HexDigits[data] + pointData;
        return data


# end coding

# end class TM1637


# =============================================================
# -----------  Test -------------

Display = TM1637(23, 24, BRIGHT_TYPICAL)

Display.Clear()

anzeige = [8, 8, 8, 8]
Display.Show(anzeige)
print
"8888  - Taste bitte"
scrap = raw_input()

anzeige = [1, 2, 3, 4]
Display.Show(anzeige)
print
"1234  - Taste bitte"
scrap = raw_input()

Display.Show1(1, 5)
Display.Show1(2, 4)

print
"1544  - Taste bitte"
scrap = raw_input()

Display.Show1(0, 1)
Display.Show1(3, 0)

print
"1540  - Taste bitte"
scrap = raw_input()

Display.ShowDoublepoint(True)
Display.SetBrightnes(4)

print
"15:40  heller - Taste bitte"
scrap = raw_input()

Display.Clear()

print
"Display abgeschaltet"
