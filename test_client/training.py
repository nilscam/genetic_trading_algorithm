#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from random import uniform
from random import randint
from algo import *
from utils import *
from algo import trader

class genetic:

    #genes d'un trader:
    # delta (0 / 5)
    # size (0 / 100)
    # multiplicateur de volatilité (0 / 1)
    # mise par tour de jeu (0 / 1)
    # seuil d'achat (0 / 1)
    # seuil de vente (-1 / 0)

    # à chaque epoch :
    # ajouter un individu full random pour ne pas faire converger la population
    list_genes = [[0, 5], [0, 100], [0, 1], [0, 1], [0, 1], [-1, 1]]

    def __init__(self, populationSize = 20):
        if populationSize < 5:
            print ("Population must be at least 5")
            raise
        self.populationSize = populationSize

    def genPropety(self, range):
        if range[1] == 100:
            return randint(range[0], range[1])
        else:
            return uniform(range[0], range[1])

    def generatePerson(self):
        genes = []
        for x in self.list_genes:
            genes.append(self.genPropety(x))
        return genes

    def generatePopulation(self):
        population = []
        for x in range(self.populationSize):
            population.append(self.generatePerson())
        return population

    def baise(self, gene1, gene2):
        combined_gene = [list(a) for a in zip(gene1, gene2)]

        childs = [[], []]
        for x in range(2):
            for i in range(len(self.list_genes)):
                #mutation pop 5% chance
                if randint(0,100) < 10:
                    mutation = self.genPropety(self.list_genes[i])
                    childs[x].append(mutation)
                else:
                    choice = randint(0, len(combined_gene[i]) - 1)
                    childs[x].append(combined_gene[i][choice])
                    combined_gene[i].pop(choice)

        return childs

    def recomputePopulation(self, sortedGenes):
        newGenes = []
        nbToDelete = int(self.populationSize / 2) + 1 # we add 1 random person each generation
        del sortedGenes[-nbToDelete:]

        # on garde toujours le premier
        newGenes.append(sortedGenes[0])

        nb = len(sortedGenes)
        for x in range(nb):
            if x == nb - 1:
                break
            childs = self.baise(sortedGenes[x], sortedGenes[x + 1])
            newGenes.append(childs[0])
            newGenes.append(childs[1])

        # we add a random person each generation
        newGenes.append(self.generatePerson())
        newGenes.append(self.generatePerson())
        newGenes.append(self.generatePerson())
        return newGenes


    def simulation(self, genes):
        t = trader("train", *genes)

        while t.update():
            t.runCycle()
        t.wallet.sellAll('crypto')
        t.wallet.sellAll('forex')
        t.wallet.sellAll('raw_material')
        t.wallet.sellAll('stock_exchange')
        money = t.wallet.money
        return money

    def run(self):
        population = self.generatePopulation()
        bestScore = 0
        bestGenes = []
        for x in range(300):
            print("---<Generation %d>---" % x)
            print("current best score is %.3f" % bestScore)

            #simulate all genes
            results = []
            for y in range(self.populationSize):
                results.append(self.simulation(population[y]))

            #sort genes
            sortedGenes = [z for _,z in sorted(zip(results,population), reverse=True)]
            bestScore = max(results)
            bestGenes = sortedGenes[0]

            #recompute population
            population = self.recomputePopulation(sortedGenes)

        print ("")
        print ("final result = %.3f" % bestScore)
        print (bestGenes)

def main():
    if len(sys.argv) == 8 and sys.argv[1] == "test":
        genes = [float(i) for i in sys.argv[2:]]
        genes[1] = int(genes[1])
        t = trader("train", *(genes))
        while t.update():
            t.runCycle()
        t.wallet.sellAll('crypto')
        t.wallet.sellAll('forex')
        t.wallet.sellAll('raw_material')
        t.wallet.sellAll('stock_exchange')
        money = t.wallet.money
        print (money)
        return
    population = genetic(10)
    population.run()

if (__name__ == '__main__'):
    main()
