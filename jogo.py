import pygame
import random
from pygame.locals import *

pygame.init()#inicia o pygame

#tela
SCREEN_SIZE = 600, 500
font = pygame.font.Font('freesansbold.ttf', 12)

#asteroide
Asteroide = [1, 1]
Asteroide_lataria = pygame.image.load('Imagens/Asteroide.png')
Asteroide_vel = 2

#nave
Nave = [300, 450]
Nave_lataria = pygame.image.load('Imagens/Nave_Padrao.png')
Nave_vel = 4
score = 0


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
    if direcao[pygame.K_RIGHT]:
        Nave[0] += Nave_vel
    
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

    Nave_movimenta()
    limites_nave()
    asteroide()
    atualiza_tela() #Deixar sempre em último