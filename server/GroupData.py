#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Extern
import os
import sys
import string
import signal

# Intern
from StatusCode import StatusCode

class GroupData:
    # Datas
    current_money = 10000
    shares = {
        'crypto' : 0,
        'raw_material' : 0,
        'stock_exchange' : 0,
        'forex' : 0
    }
    transaction = {
        'crypto' : 0,
        'raw_material' : 0,
        'stock_exchange' : 0,
        'forex' : 0
    }

    def GetValue(self, marketplace):
        path = "../push_index/.index.db"
        try:
            os.mkfifo(path)
        except OSError:
            pass

        my_value = -1
        try:
            fifo = open(path, "r")
        except:
            return -1

        for line in fifo:
            if (line.split(':')[0] == marketplace):
                my_value = float(line.split(':')[1])
                break
        fifo.close()
        return my_value

    def BalanceAccount(self, shares, marketplace, last_value, balance):
        self.current_money += (shares * last_value) * balance
        for key, value in self.shares.items():
            if (key == marketplace):
                self.shares[key] -= shares * balance
        for key, value in self.transaction.items():
            if (key == marketplace):
                self.transaction[key] += 1

    def Buy(self, shares, marketplace):
        last_value = self.GetValue(marketplace)
        print ("---Buying---")

        # Shares ok ?
        if shares <= 0:
            print(StatusCode.failure.get(405))
            return

        # If there is no value yet
        if last_value == -1:
            print(StatusCode.failure.get(501))
            return

        # Enough money ?
        if self.current_money < shares * last_value:
            print(StatusCode.failure.get(400))
            return

        print ("buy %d shares at %.3f price -> total cost = %.3f" % (shares, last_value, shares * last_value))
        # Buy
        self.BalanceAccount(shares, marketplace, last_value, -1)
        print(StatusCode.success.get(200))
        print ("cur money = %.3f" % self.current_money)

    def Sell(self, shares, marketplace):
        last_value = self.GetValue(marketplace)
        print ("---Selling---")

        # Shares ok ?
        if shares <= 0:
            print(StatusCode.failure.get(405))
            return

        # If there is no value yet
        if last_value == -1:
            print(StatusCode.failure.get(501))
            return

        # Enough shares ?
        for key, value in self.shares.items():
            if (key == marketplace):
                if (self.shares[key] < shares):
                    print(StatusCode.failure.get(402))
                    return

        print ("sell %d shares at %.3f price -> total cost = %.3f" % (shares, last_value, shares * last_value))

        # Sell
        self.BalanceAccount(shares, marketplace, last_value, 1)
        print(StatusCode.success.get(200))
        print ("cur money = %.3f" % self.current_money)

    def Dump(self):
        print('marketplace;shares')
        for key, value in self.shares.items():
            print(key + ";" + str(self.shares[key]))
        print('\ncurrent_money;' + str(self.current_money))

    def FullDump(self):
        print('marketplace;nb_transaction')
        for key, value in self.transaction.items():
            print(key + ";" + str(self.transaction[key]))
        print()
        self.Dump()

    def WriteLogStats(self, fifo):
        fifo.write('marketplace;nb_transaction\n')
        for key, value in self.transaction.items():
            fifo.write(key + ";" + str(self.transaction[key]) + '\n')
        fifo.write('\nmarketplace;shares\n')
        for key, value in self.shares.items():
            fifo.write(key + ";" + str(self.shares[key]) + '\n')
        fifo.write('\ncurrent_money;' + str(self.current_money) + '\n')
