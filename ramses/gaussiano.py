from util import *
import numpy as np
import scipy

class Gaussiano:
    def __init__(self, ficMod=None, ficLisUni=None):
        if ficMod and ficLisUni or not ficMod and not ficLisUni:
            raise ValueError("aprende a leer (instrucciones)")
        if ficMod:
            self.leeMod(ficMod)
        else:
            self.unidades = leeLis(ficLisUni)
            self.medUni = {}

    def escMod(self, ficMod):
        with open(ficMod, 'wb') as fpMod:
            np.save(fpMod, self.medUni)
            np.save(fpMod, self.varUni)

    def leeMod(self, ficMod):
        with open(ficMod, 'rb') as fpMod:
            self.medUni = np.load(fpMod, allow_pickle=True).item()
            self.varUni = np.load(fpMod, allow_pickle=True).item()
            self.unidades = self.medUni.keys()
            #self.gaussiana = scipy.stats.multivariate_normal(self.medUni, self.varUni)

    def initEnt(self):
        self.sumPrm = {unidad: 0 for unidad in self.unidades}
        self.numSen = {unidad: 0 for unidad in self.unidades}

        self.sumPrm2 = {unidad: 0 for unidad in self.unidades}

    def __add__(self, mod, prm):
        self.sumPrm[mod] += prm
        self.numSen[mod] += 1

        self.sumPrm2[mod] += prm**2

    def __call__(self, prm):
        maxProb = -np.inf
        for mod in self.unidades:
            #prob = scipy.stats.multivariate_normal(self.medUni[mod], self.varUni[mod]).logpdf(prm)
            prob = np.random.multivariate_normal(self.medUni[mod], np.diag(self.varUni[mod])).logpdf(prm)
            if prob > maxProb:
                maxProb = prob
                rec = mod
        return rec

    def recalMod(self):
        self.medUni={}
        self.varUni={}
        for unidad in self.unidades:
            self.medUni[unidad] = self.sumPrm[unidad] / self.numSen[unidad]
            self.varUni[unidad] = self.sumPrm2[unidad] / self.numSen[unidad] -self.medUni[unidad]**2

    def initEval(self):
        self.sumPrm_2 = {unidad: 0 for unidad in self.unidades}
        self.numSen = {unidad: 0 for unidad in self.unidades}

    def addEval(self, mod, senyal):
        self.sumPrm_2[mod] += senyal ** 2
        self.numSen[mod] += 1

    def recaEval(self):
        distancia_2 = 0
        totSen = 0
        for unidad in self.unidades:
            distancia_2 += self.numSen[unidad] * (self.sumPrm_2[unidad] / self.numSen[unidad] - self.medUni[unidad])
            totSen += self.numSen[unidad]

        self.distancia = (np.sum(distancia_2) / totSen) ** 0.5

    def printEval(self):
        print(f'{self.distancia = :.2f}')

    
