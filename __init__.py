GPU = False
try:
    import cupy as cp
    print("GPU")
    GPU = True
except:
    import numpy as np
    print("CPU")
import matplotlib.pyplot as plt
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
            weight = funcGenereate((self.architecture[i + 1], self.architecture[i]))
            self.pesos.append( 2 * weight - 1)

    def think (self, inputs):
        '''Pensar: Recebe o array de entrada e retorna a saida correspondente'''
        #Propagação das sinapses por dentro da rede neural
        sinapses = inputs
        if GPU:
            sinapses = cp.asarray(sinapses)
        
        for hidden in self.pesos:
            weights = np.dot( hidden, sinapses)
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
    a = Brain(2, [100]*10, 1, ones=False)

    # Grab some test data.
    X, Y, Z = axes3d.get_test_data(0.05)
    full = 0
    z = []
    for i in range(120):
        for j in range(120):
            t = time.time()
            entry = np.array([X[i][j], Y[i][j]]).T
            out = a.think(entry)
            z.append(float(out))
            full += time.time() - t
    
    print("{:.10f}".format(full/(120*120)))

    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    Z = np.array(z)
    Z.shape = (120, 120)

    try:
        Z = np.asnumpy(Z)
    except:
        pass


    # Plot a basic wireframe.
    ax.plot_surface(X, Y, Z, cmap='viridis')

    plt.show()