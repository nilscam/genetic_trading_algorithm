#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import os

def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

def GetValue(marketplace):
    path = "../push_index/.index.db"
    try:
        os.mkfifo(path)
    except OSError:
        pass

    my_value = -1
    try:
        fifo = open(path, "r")
    except:
        return -1

    for line in fifo:
        if (line.split(':')[0] == marketplace):
            my_value = float(line.split(':')[1])
            break
    fifo.close()
    return my_value
