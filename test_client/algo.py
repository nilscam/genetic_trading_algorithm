#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from puller import *
import sys

class marketplaceStats:
    # max, min, median, linear_gradient
    def __init__(self):
        self.max = -99999999999
        self.min = 99999999999

class tradeAnalyzer:

    def __init__(self):
        self.data = {'crypto': [], 'forex': [], 'raw_material': [], 'stock_exchange': []}
        

    def feed(self, epoch):
        
    

class wallet:

    def __init__(self):
        self.money = 10000
        self.crypto = 0
        self.raw_material = 0
        self.forex = 0
        self.stock_exchange = 0
        self.puller = puller("test")
        self.curPrice = self.puller.pull()

    def getPrice(self, nb, marketplace):
        return nb * self.curPrice[marketplace]

    def buy(self, nb, marketplace):
        price = self.getPrice(nb, marketplace)
        if price <= self.money:
            print("BUY:%d:%s" % (nb, marketplace), flush=True)
            #can't check if transaction is validate
            self.__dict__[marketplace] += nb
            self.money -= price

    def sell(self, nb, marketplace):
        price = self.getPrice(nb, marketplace)
        if self.__dict__[marketplace] >= nb:
            print("SELL:%d:%s" % (nb, marketplace), flush=True)
            #can't check if transaction is validate
            self.__dict__[marketplace] -= nb
            self.money += price

    def pull(self):
        self.curPrice = self.puller.pull()

def algo():
    w = wallet()
    
