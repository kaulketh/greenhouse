#!/usr/bin/python
# -*- coding: utf-8 -*-
# string_utils.py.py
"""
functions for string handling
author: Thomas Kaulke, kaulketh@gmail.com
"""



def main():
    test_string = "12500s"


    print (test_string)

    for i in test_string:
        #if i.isdigit():
        #    print ("digit " + str(i))
        #if i.isdecimal():
        #    print ("decimal " + str(i))
        if i.isnumeric():
            print ("numeric " + str(i))
        #if i.isalnum():
        #    print ("alnum " + str(i))
        if i.isalpha():
            print ("alpha " + str(i))

    return


if __name__ == '__main__':
    main()


