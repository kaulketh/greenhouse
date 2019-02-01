#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import time
import threading
import greenhouse


def mach_los(wait):
    t = threading.Timer(greenhouse.stop, wait)
    t.start()
    print('Ich mache was')
    greenhouse.start_timer = False
    return


while True:
    print('Check, ob ich soll...')
    if greenhouse.start_timer:
        mach_los(greenhouse.wait)
    else:
        print('Nichts zu tun...')
    time.sleep(1)
