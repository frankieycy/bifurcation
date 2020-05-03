import numpy as np

progressBars = ['-','\\','|','/']

def F(adjParam, population):
    return population*np.exp(adjParam*(1-population))

class breedModel:
    def __init__(self, breedMap, initPopulation, adjParamBins, iters):
        self.breedMap = breedMap
        self.initPopulation = initPopulation
        self.adjParamBins = adjParamBins
        self.iters = iters
        self.evolution = {key: None for key in self.adjParamBins}

    def evolve(self):
        counter = 0
        for adjParam in self.adjParamBins:
            print('Evolving r = %.4f | %c %.2f %%\r' % \
                (adjParam, progressBars[counter%4], 100.*counter/len(self.adjParamBins)), end='')
            counter += 1
            populations = []
            oldPopulation = self.initPopulation
            for i in range(self.iters):
                newPopulation = self.breedMap(adjParam, oldPopulation)
                populations.append(newPopulation)
                oldPopulation = newPopulation
            self.evolution[adjParam] = populations
        return self.evolution

    def getLastPopulations(self, n):
        assert self.evolution[self.adjParamBins[0]] != None
        return {key: val[-n:] for key, val in self.evolution.items()}

    def printLastPopulations(self, n):
        lastPopulations = self.getLastPopulations(n)
        f = open('breedModel.txt', 'w')
        for key, val in lastPopulations.items():
            for population in val:
                f.write('%.4f %.4f\n' % (key, population))
        f.close()
