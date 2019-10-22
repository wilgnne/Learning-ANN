GPU = False
try:
    import cupy as cp
    cp.array([0])
    print("GPU")
    GPU = True
except:
    print("CPU")

import numpy as np
import time, pickle

class Brain (object):
    '''Brain Class: Representação da Rede Neural

    Construtor: Recebe o tanhando da entrada, 
    uma lista contendo os tamanhos da camada interna, 
    o tamanho da saida, 
    e se a rede sera inicializada com pesos 'uns' ou randomicos'''

    def __init__ (self, inputs:int, hidden:list, output:int, ones=True):
        #Define uma lista contendo a arquitetura (tamanho de suas camadas) da rede neural
        self.architecture = [inputs] + hidden + [output]

        #Expresao lambida que seleciona o método a ser usado para gerar os pesos
        funcGenereate = (lambda x: np.ones(x)) if ones else (lambda x: np.random.random(x))
        if GPU:
            funcGenereate = (lambda x: cp.ones(x)) if ones else (lambda x: cp.random.random(x))

        #Matriz de pesos da rede
        self.pesos = []
        for i in range(len(self.architecture)-1):
            weight = funcGenereate((self.architecture[i], self.architecture[i + 1]))
            self.pesos.append( 10 * weight - 5)

    def think (self, inputs):
        '''Pensar: Recebe o array de entrada e retorna a saida correspondente'''
        #Propagação das sinapses por dentro da rede neural
        sinapses = inputs
        xp = np
        if GPU:
            sinapses = cp.asarray(sinapses)
            xp = cp
        
        for hidden in self.pesos:
            weights =  xp.dot(sinapses, hidden)
            sinapses = Brain.sigmoid(weights)
        
        return sinapses
    
    def serialize(self, path, name):
        try:
            os.mkdir(f'{path}/{name}')
        except:
            pass
        binary_file = open(f'{path}/{name}.bin',mode='wb')
        pickle.dump(self, binary_file)
        binary_file.close()
    
    @staticmethod
    def deserialize (path):
        binary_file = open(path,mode='rb')
        return pickle.load(binary_file)

    @staticmethod
    def sigmoid (x):
        '''Função Sigmoidal de ativação dos neuronios'''
        return 1 / (1 + np.exp(-x))


if __name__ == "__main__":
    from mpl_toolkits.mplot3d import axes3d
    import matplotlib.pyplot as plt
    while True:
        a = Brain(2, [20, 30, 15, 5], 1, ones=False)
        print(len(a.pesos))
        full = 0
        z = []
        resolution = 512
        for i in range(resolution):
            for j in range(resolution):
                ia = 200 * (i / resolution) - 100
                ja = 200 * (j / resolution) - 100
                entry = np.array([ja, ia])
                out = a.think(entry)
                z.append(float(out))
                print("{:.2f}".format(100*full /(resolution*resolution)))
                full += 1

        Z = np.array(z)
        Z.shape = (resolution, resolution)

        try:
            Z = np.asnumpy(Z)
        except:
            pass
        
        plt.imshow(Z, cmap="gray")
        plt.show()