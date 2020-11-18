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

arquivo = open("arquivo.p", "rb")
modelo_carregado = pickle.load(arquivo)

pygame.init()#inicia o pygame

#vetores para o dataset da rede neural
Delta_Diferenca_X= []
Delta_Diferenca_Y= []
Valores_Y=[]
contador = 0
flag = False
#----------------------------------

#tela
SCREEN_SIZE = 600, 500
font = pygame.font.Font('freesansbold.ttf', 12)

#asteroide
Asteroide = [1, 1]
Asteroide_lataria = pygame.image.load('Imagens/Asteroide.png')
Asteroide_vel = 5
Asteroide_mask = pygame.mask.from_surface(Asteroide_lataria)

#nave
Nave = [300, 450]
Nave_lataria = pygame.image.load('Imagens/Nave_Padrao.png')
Nave_vel = 4
score = 0
Nave_mask = pygame.mask.from_surface(Nave_lataria)


screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Space Danger")#titulo da janela do jogo

clock = pygame.time.Clock()

#-----------------FUNÇÕES AUXILIARES--------------
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
        Asteroide[0] = random.randint(0,SCREEN_SIZE[0]-Asteroide_lataria.get_width()) 

#movimentação da nave
def Nave_movimenta():
    direcao = pygame.key.get_pressed()
    if direcao[pygame.K_LEFT]:
        Nave[0] -= Nave_vel
        if contador == 20:
            Valores_Y.append(-1)
    elif direcao[pygame.K_RIGHT]:
        Nave[0] += Nave_vel
        if contador == 20:
            Valores_Y.append(1)
    else:
        if contador == 20:
            Valores_Y.append(0)
    #flag = False

def Nave_movimenta_AI():
    dir = modelo_carregado.activate([Nave[0] - Asteroide[0] , Nave[1] - Asteroide[1]])
    if dir < -0.5:
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

    Nave_movimenta()
    #Nave_movimenta_AI()

    limites_nave()
    asteroide()
    
    #dataset
    if(contador == 20):
        Delta_Diferenca_X.append(Nave[0] - Asteroide[0])
        Delta_Diferenca_Y.append(Nave[1] - Asteroide[1])
        contador = 0
        #flag = True
    #flag = False
    contador += 1

    atualiza_tela() #Deixar sempre em último

#--prints para debuging----------
print(Delta_Diferenca_X)
print(Delta_Diferenca_Y)
print(Valores_Y)
print(len(Delta_Diferenca_X))
print(len(Delta_Diferenca_Y))
print(len(Valores_Y))
#-------------------------------
#salvando o dataset

np.savetxt("Dataset_Delta_X.txt", Delta_Diferenca_X, fmt='%i')
np.savetxt("Dataset_Delta_Y.txt", Delta_Diferenca_Y, fmt='%i')
np.savetxt("Dataset_Y.txt", Valores_Y, fmt='%i')

#print(modelo_carregado.activate([21 , 100]))
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