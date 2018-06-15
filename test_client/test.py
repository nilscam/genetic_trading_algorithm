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

def loopstdin():
    lines = []
    i = 0
    for line in sys.stdin:
        if i > 3:
            break;
        else:
            lines.append(line)
            i += 1
    return dict(zip([x.split(':')[0] for x in lines], [x.split(':')[1] for x in lines]))

def loopindexdb():
    markets = ['crypto', 'raw_material', 'stock_exchange', 'forex']
    return dict(zip(markets, [GetValue(x) for x in markets]))

if (__name__ == '__main__'):
    while True:
        stdin = loopstdin()
        stddb = loopindexdb()
        for key, value in stdin.items():
            eprint("%s: stdin = %.3f, stddb = %.3f" % (key, float(value), stddb[key]))
