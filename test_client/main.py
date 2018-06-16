#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from algo import *
from utils import *

def main():
        if len(sys.argv) == 2 and sys.argv[1] == "indexdb":
            eprint("indexdb mode")
            algo("prod")
        else:
            eprint("stdin mode")
            algo("test")


if (__name__ == '__main__'):
    main()
