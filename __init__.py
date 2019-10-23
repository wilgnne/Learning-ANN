GPU = False
try:
    import cupy as cp
    cp.array([0])
    print("GPU")
    GPU = True
except:
    print("CPU")

import numpy as np
import time, pickle, random

class Brain (object):
    '''Brain Class: Representação da Rede Neural

    Construtor: Recebe o tanhando da entrada, 
    uma lista contendo os tamanhos da camada interna, 
    o tamanho da saida, 
    e se a rede sera inicializada com pesos 'uns' ou randomicos'''

    def __init__ (self, inputs:int, hidden:list, output:int, ones=False):
        #Define uma lista contendo a arquitetura (tamanho de suas camadas) da rede neural
        self.architecture = [inputs] + hidden + [output]

        #Expresao lambida que seleciona o método a ser usado para gerar os pesos
        funcGenereate = (lambda x: np.ones(x)) if ones else (lambda x: np.random.random(x))
        if GPU:
            funcGenereate = (lambda x: cp.ones(x)) if ones else (lambda x: cp.random.random(x))

        #Matriz de pesos da rede
        self.pesos = []
        u = -5
        v = 5
        for i in range(len(self.architecture)-1):
            weight = funcGenereate((self.architecture[i], self.architecture[i + 1]))
            self.pesos.append( (v - u) * weight + u)

    def think (self, inputs):
        '''Pensar: Recebe o array de entrada e retorna a saida correspondente'''
        #Propagação das sinapses por dentro da rede neural
        sinapses = inputs
        xp = np
        if GPU:
            sinapses = cp.asarray(sinapses)
            xp = cp
        
        for i in range(len(self.pesos)):
            weights =  xp.dot(sinapses, self.pesos[i])
            sinapses = Brain.sigmoid(weights)
        
        return sinapses
    
    def serialize(self, path, name):
        try:
            os.mkdir(f'{path}')
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
        xp = np
        if GPU:
            xp = cp
        return 1 / (1 + xp.exp(-x))


if __name__ == "__main__":
    from mpl_toolkits.mplot3d import axes3d
    import matplotlib.pyplot as plt
    while True:
        a = Brain(3, [30, 15], 1)
        print(len(a.pesos))
        full = 0
        xy = []
        xz = []
        yz = []
        resolution = 64
        u = 0
        v = 1
        for i in range(1, resolution+1):
            for j in range(1, resolution+1):
                for k in range(1, resolution + 1):
                    ia = (v - u) * (i / resolution) + u
                    ja = (v - u) * (j / resolution) + u
                    ka = (v - u) * (k / resolution) + u
                    entry = np.array([ka, ja, ia])
                    out = a.think(entry)
                    if k == 1:
                        xy.append(float(out))
                    if i == 1:
                        xz.append(float(out))
                    if j == 1:
                        yz.append(float(out))
                    
                    print("{:.2f}".format(100*full /(resolution*resolution*resolution)))
                    full += 1

        XY = np.array(xy)
        XY.shape = (resolution, resolution)

        XZ = np.array(xz)
        XZ.shape = (resolution, resolution)

        YZ = np.array(yz)
        YZ.shape = (resolution, resolution)

        try:
            XY = np.asnumpy(XY)
            XZ = np.asnumpy(XZ)
            YZ = np.asnumpy(YZ)
        except:
            pass
        
        XY[0][0] = 0
        XY[0][1] = 1

        XZ[0][0] = 0
        XZ[0][1] = 1

        YZ[0][0] = 0
        YZ[0][1] = 1
        

        fig, axs = plt.subplots(2, 2)
        ax = axs[0, 0]
        pcm = ax.pcolormesh(XY, cmap="viridis")
        fig.colorbar(pcm, ax=ax)

        ax = axs[1, 0]
        pcm = ax.pcolormesh(XZ, cmap="viridis")
        fig.colorbar(pcm, ax=ax)

        ax = axs[1, 1]
        pcm = ax.pcolormesh(YZ, cmap="viridis")
        fig.colorbar(pcm, ax=ax)

        plt.show()

        save = int(input("Salvar? 1/0: "))
        if save:
            a.serialize("..", "brain")
            break