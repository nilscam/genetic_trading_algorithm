#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys

class puller:
    # mode can be "prod" or "test"
    marketplace_list = ['crypto', 'raw_material', 'stock_exchange', 'forex']

    def __init__(self, mode):
        self.mode = mode

    def getInputTest(self):
        lines = []
        i = 0
        for line in sys.stdin:
            if i > 3:
                break;
            else:
                lines.append(line)
                i += 1
        return lines

    def getValueTest(self, lines, marketplace):
        my_value = -1
        for line in lines:
            if (line.split(':')[0] == marketplace):
                my_value = float(line.split(':')[1])
                break
        return my_value

    def refreshDataTest(self):
        my_data = self.getInputTest()
        values = [self.getValueTest(my_data, x) for x in puller.marketplace_list]
        return dict(zip(puller.marketplace_list, values))

    def getValueProd(self, marketplace):
        path = "../push_index/.index.db"
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

    def refreshDataProd(self):
        values = [self.getValueProd(my_data, x) for x in puller.marketplace_list]
        return dict(zip(puller.marketplace_list, values))

    def pull(self):
        if (self.mode == "test"):
            return self.refreshDataTest()
        else:
            return self.refreshDataProd()
        
