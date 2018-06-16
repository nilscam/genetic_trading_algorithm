#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from pull import *
from utils import *
import math
import numpy as np

BRANGE = 100

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
