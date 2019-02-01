#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import time
import greenhouse


def mach_los():
    print('Ich mache was')
    return


def timer(wait):
    while True:
        print('Check, ob ich soll...')
        soll_ich = greenhouse.start_timer
        if soll_ich:
            time.sleep(wait)
            mach_los()
            greenhouse.stop
        else:
            print('Nichts zu tun...')
        time.sleep(1)


if __name__ == '__main__':
    timer(greenhouse.wait)

