#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import math
try:
    from utils import *
except:
    from .utils import *

class wallet:

    def __init__(self, mode):
        self.mode = mode
        self.money = 10000
        self.crypto = 0
        self.raw_material = 0
        self.forex = 0
        self.stock_exchange = 0
        self.curPrice = {}
        self.buyOrder = {'crypto': 0, 'forex': 0, 'raw_material': 0, 'stock_exchange': 0}
        self.sellOrder = {'crypto': 0, 'forex': 0, 'raw_material': 0, 'stock_exchange': 0}

    def __str__(self):
        eprint("---Wallet:---")
        eprint("Money: %.3f" % (self.money))
        eprint("crypto: %d, estimated at %.3f" % (self.crypto, self.curPrice['crypto']))
        eprint("raw_material: %d, estimated at %.3f" % (self.raw_material, self.curPrice['raw_material']))
        eprint("forex: %d, estimated at %.3f" % (self.forex, self.curPrice['forex']))
        eprint("stock_exchange: %d, estimated at %.3f" % (self.stock_exchange, self.curPrice['stock_exchange']))
        return ("------------")

    def setCurPrice(self, curPrice):
        self.curPrice = curPrice

    def getPrice(self, nb, marketplace):
        return nb * self.curPrice[marketplace]

    def buy(self, nb, marketplace):
        if nb == 0:
            return
        price = self.getPrice(nb, marketplace)
        if price <= self.money:
            if self.mode != "train":
                print("BUY:%d:%s" % (nb, marketplace), flush=True)
            #can't check if transaction is validate
            self.__dict__[marketplace] += nb
            self.money -= price

    def sell(self, nb, marketplace):
        if nb == 0:
            return
        price = self.getPrice(nb, marketplace)
        if self.__dict__[marketplace] >= nb:
            if self.mode != "train":
                print("SELL:%d:%s" % (nb, marketplace), flush=True)
            #can't check if transaction is validate
            self.__dict__[marketplace] -= nb
            self.money += price

    def placeBuyOrder(self, nb, marketplace):
        self.buyOrder[marketplace] += nb
        print("BUY:%d:%s" % (nb, marketplace), flush=True)

    def placeSellOrder(self, nb, marketplace):
        self.sellOrder[marketplace] += nb
        print("SELL:%d:%s" % (nb, marketplace), flush=True)

    def executeOrders(self):
        for marketplace, number in self.buyOrder.items():
            self.buy(number, marketplace)
            self.buyOrder[marketplace] = 0
        for marketplace, number in self.sellOrder.items():
            self.sell(number, marketplace)
            self.sellOrder[marketplace] = 0

    def sellAll(self, marketplace):
        if self.__dict__[marketplace] != 0:
            #self.placeSellOrder(self.__dict__[marketplace], marketplace) # for put local in same env than server
            self.sell(self.__dict__[marketplace], marketplace) # for server

    # buy as many shares as possible for this price rounded up
    def buyFor(self, maxMoney, marketplace):
        if self.curPrice[marketplace] <= self.money:
            if maxMoney > self.money:
                maxMoney = self.money
            nb = math.ceil(maxMoney / self.curPrice[marketplace])
            if not nb == 1:
                nb -= 1
            #self.placeBuyOrder(nb, marketplace) # for put local in same env than server
            self.buy(nb, marketplace) # for server
