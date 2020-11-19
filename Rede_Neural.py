#------Imports segundo vídeo--------------------------

from pybrain3.tools.shortcuts import buildNetwork
from pybrain3.datasets import SupervisedDataSet
from pybrain3.supervised.trainers import BackpropTrainer
from pybrain3.structure.modules import SoftmaxLayer
from pybrain3.structure.modules import SigmoidLayer

#para a funcoes de arquivo
import numpy as np
#para salvar a rede
import pickle

#---------------------Fim dos Imports----------------------

# ----------------------Segundo Video--------------------------------------

# Criando a rede Neural
rede = buildNetwork(3, 5, 1)
'''
print(rede['in'])
print(rede['hidden0'])  #Mostra que a camada oculta possui a função sigmoide
print(rede['out'])
print(rede['bias'])
'''
# Base de dados, dois atributos previsores e uma classe
base = SupervisedDataSet(3, 1)
# Adicionando os elementos(XOR)
'''
base.addSample((0, 0), (0,))  # Resultado 0
base.addSample((0, 1), (1,))  # Resultado 1
base.addSample((1, 0), (1,))  # Resultado 1
base.addSample((1, 1), (-1,))  # Resultado 0
'''

#Incluindo o dataset do jogo
"""
Array_X = [0,0,1,1]
Array_Y = [0,1,0,1]
Array_Saida = [0, 1, 1, -1]
"""
Posicao_nave_X = np.loadtxt("Dataset_Posicao_X.txt")
Array_X = np.loadtxt("Dataset_Delta_X.txt")
Array_Y = np.loadtxt("Dataset_Delta_Y.txt")
Array_Saida = np.loadtxt("Dataset_Y.txt")

for i in range(len(Array_X)):
   base.addSample((Posicao_nave_X[i] , Array_X[i] , Array_Y[i]) , (Array_Saida[i],))

print(base['input'])
print(base['target'])

# Treinamento
treinamento = BackpropTrainer(rede, dataset=base, learningrate=0.01, momentum = 0.01)

# Controlado o número de épocas(30000 épocas)
for i in range(1, 30000):
   erro = treinamento.train()
   # Printando o erro e limitando a quantidade de vezes que o mesmo vai ser printado para melhor visualização. Nesse caso, será printado de 1000 em 1000
   if i % 100 == 0:
      print("Erro: %s" % erro)


arquivo = open('arquivo.p1', 'wb')
pickle.dump(rede, arquivo)
arquivo.close()

# Conferindo se a rede está aprendendo certo
for i in range(len(Array_X)):
   print(rede.activate([Posicao_nave_X[i] , Array_X[i] , Array_Y[i]]))
