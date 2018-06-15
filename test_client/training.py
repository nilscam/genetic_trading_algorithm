#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from algo import *
from utils import *

def main():
        if len(sys.argv) == 2 and sys.argv[1] == "test":
            eprint("test mode")
            algo("test")
        else:
            eprint("prod mode")
            algo("prod")


if (__name__ == '__main__'):
    main()
