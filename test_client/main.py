#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import subprocess as sub
import os
from algo import *

def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

def GetValue(marketplace):
    path = "../push_index/.index.db"
    try:
        os.mkfifo(path)
    except OSError:
        pass

    my_value = -1
    fifo = open(path, "r")

    for line in fifo:
        if (line.split(':')[0] == marketplace):
            my_value = float(line.split(':')[1])
            break
    fifo.close()
    return my_value

def main():
        if len(sys.argv) == 2 and sys.argv[1] == "test":
                algo("test")
        else:
                algo("prod")

        #display earned money and leave
        sys.stdout.write("STATS\n")
        sys.stdout.flush()
        sys.stdout.write("EXIT\n")
        sys.stdout.flush()


if (__name__ == '__main__'):
    main()
