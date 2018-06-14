#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from bollinger import *
import sys

class wallet:

    def __init__(self, mode):
        self.money = 10000
        self.crypto = 0
        self.raw_material = 0
        self.forex = 0
        self.stock_exchange = 0
        self.curPrice = {}

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
        self.sell(self.__dict__[marketplace], marketplace)

class trader:

    #genes d'un trader:
    # delta (0 / 5)
    # size (0 / 100)
    # multiplicateur de volatilité (0 / 1)
    # multiplicateur de mise (0 / 1)
    # seuil d'achat (0 / 1)
    # seuil de vente (-1 / 0)

    def __init__(self, mode = "prod", delta = 2, size = 20, risk = 0.5, bet = 0.5, buyLimit = -0.5, sellLimit = 0.5):
        self.risk = risk
        self.bet = bet
        self.buyLimit = buyLimit
        self.sellLimit = sellLimit
        self.wallet = wallet(mode)
        self.bollinger = bollinger(mode, delta, size)
        self.watch(size)

    def runCycle(self):
        ratios = {}
        for marketplace in marketplace_list:

            #récupère des statistiques sur le marché
            marketstate = self.bollinger.process(marketplace)

            #volatilité actuelle du marché (0 / 1)
            risk = self.bollinger.calcCurRisk(marketstate.bmin, marketstate.bmax)

            #etat de la valeur du marché actuelle par rapport aux coubres de bollinger (-1 / 1)
            curstate = self.bollinger.findCur(self.wallet.getPrice(1, marketplace), marketstate.bands)

            # interet que l'algo doit porter à ce marché
            attractiveness = self.bollinger.smoothing(risk * curstate)

            #si le marché est haut dans les bandes de bollinger, je vend mes actions si attractiveness est inférieur à sellLimit
            if attractiveness > 0:
                if attractiveness > sellLimit:
                    self.wallet.sellAll(marketplace)
            #sinon si le marché est en bas dans les bandes de bollinger, j'achète des actions si attractiveness est supérieur à buyLimit
            elif
                ratio[marketplace] = attractiveness

        #softmax the list
        keys = []
        values = []
        for key, value in ratios.iteritems():
            keys.append(key)
            values.append(value)
        updateRatios = dict(zip(keys, self.bollinger.softmax(values)))



    def watch(self, nb):
        for i in range(nb):
            self.update()

    def update(self):
        self.wallet.setCurPrice(self.bollinger.pull())


def algo(mode):
    #init variables
    w = wallet(mode)
    b = bollinger()
    b.feed(w.curPrice)

    #loop algo
    while not -1 in w.curPrice.values():
        print(b.process('crypto'))
        update(w, b)
