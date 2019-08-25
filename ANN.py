import numpy as np

#Brain Class: Representação da Rede Neural
class Brain (object):

    #Construtor: Recebe o tanhando da entrada, uma lista contendo os tamanhos da camada interna,
    #            o tamanho da saida, e se a rede sera inicializada com pesos 'uns' ou randomicos
    def __init__ (self, inputs:int, hidden:list, output:int, ones=True):

        #Define uma lista contendo a arquitetura (tamanho de suas camadas) da rede neural
        self.architecture = [inputs] + hidden + [output]

        #Expresao lambida que seleciona o método a ser usado para gerar os pesos
        funcGenereate = (lambda x: np.ones(x)) if ones else (lambda x: np.random.random(x))

        #Matriz de pesos da rede
        self.pesos = []
        for i in range(len(self.architecture)-1):
            weight = funcGenereate((self.architecture[i],  self.architecture[i + 1]))
            self.pesos.append( 2 * weight - 1)

    #Pensar: Recebe o array de entrada e retorna a saida correspondente
    def think (self, inputs: np.array):
        #Propagação das sinapses por dentro da rede neural
        sinapses = inputs
        for hidden in self.pesos:
            weights = np.dot(sinapses, hidden)
            sinapses = weights * Brain.sigmoid(weights)
        
        return sinapses

    #Função Sigmoidal de ativação dos neuronios
    @staticmethod
    def sigmoid (x):
        return 1 / (1 + np.exp(-x))

if __name__ == "__main__":
    a = Brain(2, [20], 1, ones=False)
    print(a.think(np.array([10, 20])))
