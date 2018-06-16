#!/usr/bin/env python3
#-*- coding: utf-8 -*-

try:
    from utils import *
except:
    from .utils import *
import sys
import os
import time

marketplace_list = ['crypto', 'raw_material', 'stock_exchange', 'forex']

class puller:
    # mode can be "prod" or "test"

    def __init__(self, mode = "prod", path = "./indexes/", maxEpoch = 360):
        self.mode = mode
        #self.index_db = "../push_index/.index.db"
        self.index = 0
        self.maxEpoch = maxEpoch
        self.data_set = {'crypto': [], 'forex': [], 'raw_material': [], 'stock_exchange': []}
        if mode == "train":
            self.buildDataSet(path)

    def buildDataSet(self, path):
        for marketplace in marketplace_list:
            try:
                with open(path + marketplace + ".txt", "r") as f:
                    for item in f:
                        self.data_set[marketplace].append(float(''.join(item.splitlines())))
            except ValueError:
                pass
            except:
                eprint("Can't open and read file")
                raise

    def getValueTest(self, lines, marketplace):
        my_value = -1
        for line in lines:
            if (line.split(':')[0] == marketplace):
                my_value = float(line.split(':')[1])
                break
        return my_value

    def getValueProd(self, marketplace):
        path = self.index_db
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

    def refreshDataTest(self):
        my_data = [sys.stdin.readline() for i in range(4)]
        values = [self.getValueTest(my_data, x) for x in marketplace_list]
        return dict(zip(marketplace_list, values))

    def refreshDataProd(self):
        values = [self.getValueProd(x) for x in marketplace_list]
        return dict(zip(marketplace_list, values))

    def refreshTrainData(self):
        values = dict()
        if self.index == self.maxEpoch:
            return {'crypto': -1}
        for key, value in self.data_set.items():
            values[key] = value[self.index]
        self.index += 1
        return values

    def pull(self):
        if self.mode == "train":
            return self.refreshTrainData()
        elif (self.mode == "test"):
            return self.refreshDataTest()
        else:
            return self.refreshDataProd()
