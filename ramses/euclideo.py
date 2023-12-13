from util import *
import numpy as np

class Euclideo:
    def __init__(self, ficMod=None, ficLisUni=None):
        if ficMod and ficLisUni or not ficMod and not ficLisUni:
            raise ValueError("Lee las instrucciones BOBO")
        
        if ficMod:
            self.leeMod(ficMod)
        else: 
            self.unidades = leeLis(ficLisUni)
            self.medUni = {}

    def escMod(self, ficMod):
        with open(ficMod, 'wb') as fpMod:
            np.save(fpMod, self.medUni)

    def leeMod(self, ficMod):
        with open(ficMod, 'rb') as fpMod:
            self.medUni = np.load(fpMod)
            self.unidades = self.medUni.keys()

    def initEnt(self):
        self.sumPrm = {unidad: 0 for unidad in self.unidades}
        self.numSen = {unidad: 0 for unidad in self.unidades}

    def __add__(self, mod, senyal):
        self.sumPrm[mod] += senyal
        self.numSen[mod] += 1

    def recalMod(self):
        for unidad in self.unidades:
            self.medUni[unidad] = self.sumPrm[unidad] / self.numSen[unidad]

    def initEval(self):
        self.sumPrm_2 = {unidad: 0 for unidad in self.unidades}
        self.numSen = {unidad: 0 for unidad in self.unidades}

    def addEval(self, mod, senyal):
        self.sumPrm_2[mod] += senyal ** 2
        self.numSen[mod] += 1
    
    def recalEval(self):
        distancia_2 = 0
        totSen = 0
        for unidad in self.unidades:
            distancia_2 += self.numSen[unidad] * (self.sumPrm_2[unidad] / self.numSen[unidad] - self.medUni[unidad])
            totSen += self.numSen[unidad]

        self.distancia = (np.sum(distancia_2) / totSen) ** 0.5

    def printEval(self):
        print(f'{self.distancia = :.2f}')

