#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import os
import math
import numpy as np

BRANGE = 100
marketplace_list = ['crypto', 'raw_material', 'stock_exchange', 'forex']

class puller:
    # mode can be "prod" or "test"

    def __init__(self, mode):
        self.mode = mode

    def getInputTest(self):
        lines = []
        i = 0
        for line in sys.stdin:
            if i > 3:
                break;
            else:
                lines.append(line)
                i += 1
        return lines

    def getValueTest(self, lines, marketplace):
        my_value = -1
        for line in lines:
            if (line.split(':')[0] == marketplace):
                my_value = float(line.split(':')[1])
                break
        return my_value

    def refreshDataTest(self):
        my_data = self.getInputTest()
        values = [self.getValueTest(my_data, x) for x in marketplace_list]
        return dict(zip(marketplace_list, values))

    def getValueProd(self, marketplace):
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

    def refreshDataProd(self):
        values = [self.getValueProd(x) for x in marketplace_list]
        return dict(zip(marketplace_list, values))

    def pull(self):
        if (self.mode == "test"):
            return self.refreshDataTest()
        else:
            return self.refreshDataProd()


class bollinger:

    #bollinger bands implementation

    def __init__(self, mode = "prod", delta = 2, size = 20):
        self.data = {'crypto': [], 'forex': [], 'raw_material': [], 'stock_exchange': []}
        self.delta = delta
        self.size = size
        self.puller = puller(mode)

    def feed(self, epoch):
        for key, value in epoch.items():
            self.data[key].append(value)

    # activation function based on gauss function
    # e ^ (-x ^ 2)
    def calcCurRisk(self, bmin, bmax):
        res = bmin / bmax
        return math.exp((-res ** 2))

    # activation function to smooth result of market attractiveness
    # ((x ^ 2 + 1) ^ 0.5 - 1) / 2 + x
    def smoothing(self, x):
        return ((x ** 2 + 1) ** 0.5 - 1) / 2 + x

    # softmax function implementation
    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def process(self, marketplace):
        data_set = self.data[marketplace][-self.size:]
        mean = np.mean(data_set)
        std = np.std(data_set)
        #bmax = [(mean + (self.delta * x / 100) * std) for x in range(BRANGE)]
        #bmin = [(mean - (self.delta * x / 100) * std) for x in range(BRANGE)]
        bmax = mean + self.delta * std
        bmin = mean - self.delta * std
        bands = [(mean - (self.delta * x / 100) * std) for x in range(BRANGE)]
        bands.reverse()
        bands += [(mean + (self.delta * x / 100) * std) for x in range(BRANGE)]
        return {'mean': mean, 'std': std, 'bmax': bmax, 'bmin': bmin, 'bands': bands}

    def findCur(self, curPrice, bands):
        if curPrice <= bands[0]:
            return -1.0
        for x in range(len(bands) - 1):
            if curPrice > bands[x] and curPrice < bands[x + 1]:
                return (x + 1) / BRANGE - 1
        return 1.0

    def pull(self):
        newdata = self.puller.pull()
        self.feed(newdata)
        return newdata
