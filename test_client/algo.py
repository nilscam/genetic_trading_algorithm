#!/usr/bin/env python3
#-*- coding: utf-8 -*-

try:
    from wallet import *
    from bollinger import *
    from utils import *
except:
    from .wallet import *
    from .bollinger import *
    from .utils import *

import sys

class trader:

    def __init__(self, mode = "prod", delta = 2, size = 20, risk = 0.5, bet = 0.5, buyLimit = 0.5, sellLimit = 0.5):
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
    #t = trader(mode, *([1.6410694649597652, 80, 0.9975905442330391, 0.02758123838569393, 0.9908648350307403, 0.37539931496677914]))

    # 267 669
    #t = trader(mode, *([2.5549499263635695, 95, 0.9973661444332922, 0.9972612298137682, -0.3134370664919579, 0.3707476541173418]))

    # 527 793
    # t = trader(mode, *([4.996287266643122, 74, 0.9970885632936157, 0.9988256445383916, -0.26962819438164254, 0.2984888872850986]))

    t = trader(mode, *([4.568550956536216, 95, 0.9707551498268774, 0.9914757981519937, -0.228886578491877, 0.19344993064699723]))

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
