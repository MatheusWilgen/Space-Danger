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
rede = buildNetwork(2, 5, 1)  # Núm. 2, significa que termos 2 neuronios na camada de entrada. Núm. 3, significa que temos 3 neuronios na camada oculta. Núm. 1. significa que temos uma saída
'''
print(rede['in'])
print(rede['hidden0'])  #Mostra que a camada oculta possui a função sigmoide
print(rede['out'])
print(rede['bias'])
'''
# Base de dados, dois atributos previsores e uma classe
base = SupervisedDataSet(2, 1)
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
Array_X = np.loadtxt("Dataset_Delta_X.txt", dtype=int)
Array_Y = np.loadtxt("Dataset_Delta_Y.txt", dtype=int)
Array_Saida = np.loadtxt("Dataset_Y.txt", dtype=int)

for i in range(len(Array_X)):
   base.addSample((Array_X[i], Array_Y[i]), (Array_Saida[i],))

print(base['input'])
print(base['target'])

# Treinamento
treinamento = BackpropTrainer(rede, dataset=base, learningrate=0.01, momentum=0.06)

# Controlado o número de épocas(30000 épocas)
for i in range(1, 30000):
   erro = treinamento.train()
   # Printando o erro e limitando a quantidade de vezes que o mesmo vai ser printado para melhor visualização. Nesse caso, será printado de 1000 em 1000
   if i % 100 == 0:
       print("Erro: %s" % erro)

# Conferindo se a rede está aprendendo certo


arquivo = open('arquivo.p', 'w')
pickle.dump(rede, arquivo)
arquivo.close()


for i in range(len(Array_X)):
   print(rede.activate([Array_X[i] , Array_Y[i]]))



#print(rede.activate([371, 179])) # espera-se que o resultado seja 1
#print(rede.activate([0, 120]))
#print(rede.activate([40, 230]))

