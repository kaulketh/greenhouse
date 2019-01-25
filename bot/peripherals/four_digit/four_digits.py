#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: sd582 - https://forum-raspberrypi.de/user/24027-sd582/
# http://www.sc2web.net/Downloads/tm1637.zip
# https://forum-raspberrypi.de/forum/thread/15042-led-4-segment-i2c-display/?postID=137411#post137411
# +
# author: KyleKing - https://github.com/KyleKing
# https://github.com/timwaizenegger/raspberrypi-examples/blob/master/actor-led-7segment-4numbers/tm1637.py
# adaptions: Thomas Kaulke, kaulketh@gmail.com

import math
import RPi.GPIO as IO
from time import sleep

IO.setwarnings(False)
IO.setmode(IO.BOARD)

""" http://www.uize.com/examples/seven-segment-display.html """
#               0    1     2     3     4     5     6     7     8     9
hex_digits = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f,
              # A    b     C     d     E     F     G     H     h     I
              0x77, 0x7c, 0x39, 0x5e, 0x79, 0x71, 0x7d, 0x76, 0x74, 0x06,
              # J    K     L     l     n     O     o     P     r     S
              0x1f, 0x76, 0x38, 0x06, 0x54, 0x3f, 0x5c, 0x73, 0x50, 0x6d,
              # U    V     Y     Z     -     _     °     '    empty  t
              0x3e, 0x3e, 0x6e, 0x5b, 0x40, 0x08, 0x63, 0x02, 0x00, 0x78,
              # u     /    ---------animation clockwise-----------   c
              0x1c, 0x52, 0x40, 0x20, 0x01, 0x02, 0x04, 0x08, 0x10, 0x58]


ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
# DEBUG = False


class TM1637:
    __double_point = False
    __clk_pin = 0
    __data_pin = 0
    __brightness = 1.0  # default to max brightness
    __current_data = [0, 0, 0, 0]

    def __init__(self, clk, dio, brightness):
        self.__clk_pin = clk
        self.__data_pin = dio
        self.__brightness = brightness
        IO.setup(self.__clk_pin, IO.OUT)
        IO.setup(self.__data_pin, IO.OUT)

    def cleanup(self):
        """turn off display, and cleanup GPIO"""
        self.clear()
        IO.cleanup()

    def clear(self):
        b = self.__brightness
        point = self.__double_point
        self.__brightness = 0
        self.__double_point = False
        data = [0x7F, 0x7F, 0x7F, 0x7F]
        self.show(data)
        # Restore previous settings:
        self.__brightness = b
        self.__double_point = point

    def show_int(self, i):
        s = str(i)
        self.clear()
        for i in range(0, len(s)):
            self.show1(i, int(s[i]))

    def show(self, data):
        for i in range(0, 4):
            self.__current_data[i] = data[i]

        self.start()
        self.write_byte(ADDR_AUTO)
        self.br()
        self.write_byte(STARTADDR)
        for i in range(0, 4):
            self.write_byte(self.coding(data[i]))
        self.br()
        self.write_byte(0x88 + int(self.__brightness))
        self.stop()

    def show1(self, digit_number, data):
        """show one Digit (number 0...3)"""
        if digit_number < 0 or digit_number > 3:
            return  # error

        self.__current_data[digit_number] = data

        self.start()
        self.write_byte(ADDR_FIXED)
        self.br()
        self.write_byte(STARTADDR | digit_number)
        self.write_byte(self.coding(data))
        self.br()
        self.write_byte(0x88 + int(self.__brightness))
        self.stop()

    def set_brightness(self, percent):
        """Accepts percent brightness from 0 - 1"""
        max_brightness = 7.0
        brightness = math.ceil(max_brightness * percent)
        if brightness < 0:
            brightness = 0
        if self.__brightness != brightness:
            self.__brightness = brightness
            self.show(self.__current_data)

    def show_doublepoint(self, on):
        """Show or hide double point divider"""
        if self.__double_point != on:
            self.__double_point = on
            self.show(self.__current_data)

    def write_byte(self, data):
        for i in range(0, 8):
            IO.output(self.__clk_pin, IO.LOW)
            if data & 0x01:
                IO.output(self.__data_pin, IO.HIGH)
            else:
                IO.output(self.__data_pin, IO.LOW)
            data = data >> 1
            IO.output(self.__clk_pin, IO.HIGH)

        # wait for ACK
        IO.output(self.__clk_pin, IO.LOW)
        IO.output(self.__data_pin, IO.HIGH)
        IO.output(self.__clk_pin, IO.HIGH)
        IO.setup(self.__data_pin, IO.IN)

        while IO.input(self.__data_pin):
            sleep(0.001)
            if IO.input(self.__data_pin):
                IO.setup(self.__data_pin, IO.OUT)
                IO.output(self.__data_pin, IO.LOW)
                IO.setup(self.__data_pin, IO.IN)
        IO.setup(self.__data_pin, IO.OUT)

    def start(self):
        """send start signal to TM1637"""
        IO.output(self.__clk_pin, IO.HIGH)
        IO.output(self.__data_pin, IO.HIGH)
        IO.output(self.__data_pin, IO.LOW)
        IO.output(self.__clk_pin, IO.LOW)

    def stop(self):
        IO.output(self.__clk_pin, IO.LOW)
        IO.output(self.__data_pin, IO.LOW)
        IO.output(self.__clk_pin, IO.HIGH)
        IO.output(self.__data_pin, IO.HIGH)

    def br(self):
        """terse break"""
        self.stop()
        self.start()

    def coding(self, data):
        if self.__double_point:
            point_data = 0x80
        else:
            point_data = 0

        if data == 0x7F:
            data = 0
        else:
            data = hex_digits[data] + point_data
        return data
