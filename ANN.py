import numpy as np

class Brain (object):

    def __init__ (self, inputs:int, hidden:list, output:int, ones=True):
        self.architecture = [inputs] + hidden + [output]
        funcGenereate = (lambda x: np.ones(x)) if ones else (lambda x: np.random.random(x))

        self.pesos = []
        for i in range(len(self.architecture)-1):
            weight = funcGenereate((self.architecture[i],  self.architecture[i + 1]))
            self.pesos.append( 2 * weight - 1)

    def think (self, inputs: np.array):
        
        sinapses = inputs
        for hidden in self.pesos:
            weights = np.dot(sinapses, hidden)
            sinapses = weights * Brain.sigmoid(weights)
        
        return sinapses
    
    @staticmethod
    def sigmoid (x):
        return 1 / (1 + np.exp(-x))



if __name__ == "__main__":
    a = Brain(2, [20], 1, ones=False)
    print(a.think(np.array([10, 20])))
