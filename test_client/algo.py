#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from bollinger import *
import sys
import math

class wallet:

    def __init__(self, mode):
        self.money = 10000
        self.crypto = 0
        self.raw_material = 0
        self.forex = 0
        self.stock_exchange = 0
        self.curPrice = {}

    def __str__(self):
        print("---Wallet:---")
        print("Money: %d" % (self.money))
        print("crypto: %d, estimated at %.3f" % (self.crypto, self.curPrice['crypto']))
        print("raw_material: %d, estimated at %.3f" % (self.raw_material, self.curPrice['raw_material']))
        print("forex: %d, estimated at %.3f" % (self.forex, self.curPrice['forex']))
        print("stock_exchange: %d, estimated at %.3f" % (self.stock_exchange, self.curPrice['stock_exchange']))
        return ("-------------")

    def setCurPrice(self, curPrice):
        self.curPrice = curPrice

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

    def sellAll(self, marketplace):
        if self.__dict__[marketplace] != 0:
            self.sell(self.__dict__[marketplace], marketplace)

    # buy as many shares as possible for this price rounded up
    def buyFor(self, maxMoney, marketplace):
        if self.curPrice[marketplace] <= self.money:
            if maxMoney > self.money:
                maxMoney = self.money
            nb = math.ceil(maxMoney / self.curPrice[marketplace])
            if not nb == 1:
                nb -= 1
            self.buy(nb, marketplace)


class trader:

    #genes d'un trader:
    # delta (0 / 5)
    # size (0 / 100)
    # multiplicateur de volatilité (0 / 1)
    # mise par tour de jeu (0 / 1)
    # seuil d'achat (0 / 1)
    # seuil de vente (-1 / 0)

    def __init__(self, mode = "prod", delta = 2, size = 20, risk = 0.5, bet = 0.8, buyLimit = -0.9, sellLimit = 0.9):
        self.risk = risk
        self.bet = bet
        self.buyLimit = buyLimit
        self.sellLimit = sellLimit
        self.wallet = wallet(mode)
        self.bollinger = bollinger(mode, delta, size)
        self.watch(int(size / 2 + 1))

    def runCycle(self):
        ratios = {}
        for marketplace in marketplace_list:

            #récupère des statistiques sur le marché
            marketstate = self.bollinger.process(marketplace)

            #volatilité actuelle du marché (0 / 1)
            risk = self.bollinger.calcCurRisk(marketstate['bmin'], marketstate['bmax'])

            #etat de la valeur du marché actuelle par rapport aux coubres de bollinger (-1 / 1)
            curstate = self.bollinger.findCur(self.wallet.getPrice(1, marketplace), marketstate['bands'])

            # interet que l'algo doit porter à ce marché
            attractiveness = self.bollinger.smoothing(risk * curstate)

            #si le marché est haut dans les bandes de bollinger, je vend mes actions si attractiveness est supérieur à sellLimit
            if attractiveness > 0:
                if attractiveness > self.sellLimit:
                    self.wallet.sellAll(marketplace)
            #sinon si le marché est en bas dans les bandes de bollinger, j'achète des actions si attractiveness est inférieur à buyLimit
            elif attractiveness < self.buyLimit:
                ratios[marketplace] = attractiveness

        #softmax the list
        keys = []
        values = []
        for key, value in ratios.items():
            if value < self.buyLimit:
                keys.append(key)
                values.append(value)

        #buy actions
        if values:
            betRatios = dict(zip(keys, self.bollinger.softmax(values)))
            toBet = self.wallet.money * self.bet
            for key, value in betRatios.items():
                self.wallet.buyFor(toBet / value, key)


    def watch(self, nb):
        for i in range(nb):
            self.update()

    def update(self):
        curState = self.bollinger.pull()
        if curState['crypto'] == -1:
            return 0
        self.wallet.setCurPrice(curState)
        return 1


def algo(mode):
    t = trader(mode)

    while t.update():
        t.runCycle()
    print(t.wallet)
    t.wallet.sellAll('crypto')
    t.wallet.sellAll('forex')
    t.wallet.sellAll('raw_material')
    t.wallet.sellAll('stock_exchange')
    print(t.wallet)
