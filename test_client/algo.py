#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from wallet import *
from bollinger import *
from utils import *
import sys

class trader:

    def __init__(self, mode = "prod", delta = 4.898800390650705, size = 13, risk = 0.9432979912924092, bet = 0.9976807618992833, buyLimit = 0.9838575642658014, sellLimit = 0.9934152010364605):
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
            risk = self.bollinger.calcCurRisk(marketstate['bmin'], marketstate['bmax']) # multiplié par self.risk pour augmenter la tendance à jouer sur des marchés volatiles

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
            #print ("curstate for %s is %.3f, risk = %.3f so attractiveness = %.3f " % (marketplace, curstate, risk, attractiveness))

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
        self.wallet.executeOrders()
        return 1


def algo(mode):
    # 153 412
    t = trader(mode, *([1.6410694649597652, 80, 0.9975905442330391, 0.02758123838569393, 0.9908648350307403, 0.37539931496677914]))

    while t.update():
        t.runCycle()
    eprint('---Local---')
    eprint(t.wallet)
    t.wallet.sellAll('crypto')
    t.wallet.sellAll('forex')
    t.wallet.sellAll('raw_material')
    t.wallet.sellAll('stock_exchange')
    t.wallet.executeOrders() # apply order placed before
    eprint(t.wallet)
    eprint('---Server---')
    sys.stdout.write("EXIT\n")
    sys.stdout.flush()
    eprint('------------')
