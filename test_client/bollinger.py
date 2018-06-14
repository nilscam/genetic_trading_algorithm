#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import numpy as np

class bollinger:

    #bollinger bands implementation

    def __init__(self, delta = 2, size = 20):
        self.data = {'crypto': [], 'forex': [], 'raw_material': [], 'stock_exchange': []}
        self.delta = delta
        self.size = size

    def feed(self, epoch):
        for key, value in epoch:
            self.data[key].append(value)

    def process(self, marketplace):
        data_set = self.data[marketplace][-size:]
        mean = np.mean(data_set)
        std = np.std(data_set)
        bmax = mean + self.delta * std
        bmin = mean - self.delta * std
        return {'mean': mean, 'std': std, 'bmax': bmax, 'bmin': bmin}
