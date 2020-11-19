import pygame
import random
from pygame.locals import *
import numpy as np
import pickle

from pybrain3.tools.shortcuts import buildNetwork
from pybrain3.datasets import SupervisedDataSet
from pybrain3.supervised.trainers import BackpropTrainer
from pybrain3.structure.modules import SoftmaxLayer
from pybrain3.structure.modules import SigmoidLayer

#Abre o objeto da rede neural treinado no programa "Rede_Neural.py"
arquivo = open("arquivo.p1", "rb")
modelo_carregado = pickle.load(arquivo)
arquivo.close()

pygame.init()#inicia o pygame

#tela
SCREEN_SIZE = [600, 500]
font = pygame.font.Font('freesansbold.ttf', 12)

#asteroide
Asteroide = [1, 1]
Asteroide_lataria = pygame.image.load('Imagens/Asteroide.png')
Asteroide_vel = 12
Asteroide_mask = pygame.mask.from_surface(Asteroide_lataria)

#nave
Nave = [300, 450]
Nave_lataria = pygame.image.load('Imagens/Nave_Padrao.png')
Nave_vel = 4
score = 0
Nave_mask = pygame.mask.from_surface(Nave_lataria)

#vetores para o dataset da rede neural
Posicao_nave_X = []
Delta_Diferenca_X= []
Delta_Diferenca_Y= []
Valores_Y=[]
CONTADOR = 0
#Variaveis para Normalização do dataset
MIN_X_Pos = 0
MIN_X = -SCREEN_SIZE[0]
MAX_X = SCREEN_SIZE[0]
MIN_Y = Nave[1] - SCREEN_SIZE[1]
MAX_Y = Nave[1] + Asteroide_lataria.get_height()
#----------------------------------

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Space Danger")#titulo da janela do jogo

clock = pygame.time.Clock()

#-----------------FUNÇÕES AUXILIARES--------------
#funcao para normalizar os dados entre 0 e 1 para treinar na rede
def normalize_vetor_X(x):
    global MIN_X
    global MAX_X
    return [(x[n] - MIN_X) / (MAX_X - MIN_X) for n in range(len(x))]

def normalize_vetor_X_Pos(x):
    global MIN_X_Pos
    global MAX_X
    return [(x[n] - MIN_X_Pos) / (MAX_X - MIN_X_Pos) for n in range(len(x))]

def normalize_vetor_Y(x):
    global MIN_Y
    global MAX_Y
    return [(x[n] - MIN_Y) / (MAX_Y - MIN_Y) for n in range(len(x))]

def normalize_x(x):
    global MIN_X
    global MAX_X
    return (x - MIN_X) / (MAX_X - MIN_X)

def normalize_x_pos(x):
    global MIN_X_Pos
    global MAX_X
    return (x - MIN_X_Pos) / (MAX_X - MIN_X_Pos)

def normalize_y(y):
    global MIN_Y
    global MAX_Y
    return (y - MIN_Y) / (MAX_Y - MIN_Y)

#Trata o comportamento da nave quando encosta nas bordas
def limites_nave():
    if Nave[0] >= SCREEN_SIZE[0] - Nave_lataria.get_width():
        Nave[0] = SCREEN_SIZE[0] - Nave_lataria.get_width()
    if Nave[0] <= 0:
        Nave[0] = 0

#comportamento do asteroide
def asteroide():
    Asteroide[1] = Asteroide[1] + Asteroide_vel
    if(Asteroide[1] >= SCREEN_SIZE[1]):
        Asteroide[1] = -Asteroide_lataria.get_height()
        #Asteroide[0] = random.randint(0,SCREEN_SIZE[0]-Asteroide_lataria.get_width())#para randomico
        Asteroide[0] = Nave[0] - int(Asteroide_lataria.get_width()/2) + random.randint(-Nave_lataria.get_width(),Nave_lataria.get_width())

def coletar_dados():
    Posicao_nave_X.append(Nave[0])
    Delta_Diferenca_X.append(Nave[0] - Asteroide[0])
    Delta_Diferenca_Y.append(Nave[1] - Asteroide[1])

#movimentação da nave
def Nave_movimenta():
    direcao = pygame.key.get_pressed()
    global CONTADOR
    CONTADOR += 1
    print(CONTADOR)
    if direcao[pygame.K_LEFT]:
        Nave[0] -= Nave_vel
        if CONTADOR > 10:
            coletar_dados()
            Valores_Y.append(0)
            CONTADOR = 0
    elif direcao[pygame.K_RIGHT]:
        Nave[0] += Nave_vel
        if CONTADOR > 10:
            coletar_dados()
            Valores_Y.append(1)
            CONTADOR = 0

def Nave_movimenta_AI():
    dir = modelo_carregado.activate([normalize_x_pos(Nave[0]) , normalize_x(Nave[0] - Asteroide[0]) , normalize_y(Nave[1] - Asteroide[1])])
    if dir < 0.5:
        Nave[0] -= Nave_vel
    elif dir > 0.5:
        Nave[0] += Nave_vel

def colisao():
    distancia_x = Asteroide[0] - Nave[0]
    distancia_y = Asteroide[1] - Nave[1]
    return Nave_mask.overlap(Asteroide_mask , (distancia_x , distancia_y)) != None

#Função responsável por atualizar os objetos na tela
def atualiza_tela():
    screen.fill((0, 0, 0)) #tela preta, esta linha sempre em primeiro

    score_font = font.render("Distancia = " + str(int(score)) + ' Km', True, (255, 255, 255)) #Texto de pontuação na tela
    screen.blit(score_font, (SCREEN_SIZE[0] - 180 , 10))

    screen.blit(Nave_lataria, (Nave[0], Nave[1])) #atualiza as posições da nave na tela
    screen.blit(Asteroide_lataria, (Asteroide[0], Asteroide[1])) #atualiza as posições do asteroide
    pygame.display.update()

while True:
    clock.tick(60) #FPS do jogo não passará de 60 FPS "clock.tick(frame_rate)"

    for event in pygame.event.get(): #Se o jogador apertar o x da janela o jogo para
        if event.type == QUIT:
            pygame.quit()

    score = (pygame.time.get_ticks()/1000) * 7.66 #7.66 é uma velocidade média em km/s da Estação Espacial Internacional
    if(colisao()):
        break

    #Nave_movimenta()
    Nave_movimenta_AI()

    limites_nave()
    asteroide()

    atualiza_tela() #Deixar sempre em último

#--prints para debuging----------
print(Posicao_nave_X)
Posicao_nave_X = normalize_vetor_X_Pos(Posicao_nave_X)
print(Posicao_nave_X)
print(Delta_Diferenca_X)
Delta_Diferenca_X = normalize_vetor_X(Delta_Diferenca_X)
print(Delta_Diferenca_X)
print(Delta_Diferenca_Y)
Delta_Diferenca_Y = normalize_vetor_Y(Delta_Diferenca_Y)
print(Delta_Diferenca_Y)
print(Valores_Y)
print(len(Delta_Diferenca_X))
print(len(Delta_Diferenca_Y))
print(len(Valores_Y))

#-------------------------------
#salvando o dataset - descomente para gerar outro dataset
"""
np.savetxt("Dataset_Posicao_X.txt", Posicao_nave_X)
np.savetxt("Dataset_Delta_X.txt", Delta_Diferenca_X)
np.savetxt("Dataset_Delta_Y.txt", Delta_Diferenca_Y)
np.savetxt("Dataset_Y.txt", Valores_Y)
"""

#-------------------------------

#tela final
r = g = b =0
while True:
    game_over_font = pygame.font.Font('freesansbold.ttf', 75)
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    game_over_screen = game_over_font.render('Game Over', True, (r, g, b))
    screen.blit(game_over_screen, (80 , (SCREEN_SIZE[1] / 2 ) - 75))
    pygame.display.update()
    pygame.time.wait(200)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()