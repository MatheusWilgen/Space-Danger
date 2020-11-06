import pygame
import time
import pygame
import random
from pygame.locals import *

SCREEN_SIZE = 600,500

Asteroide = [1,1]
Asteroide_lataria = pygame.Surface((20,20))
Asteroide_lataria.fill((255,0,0))

Nave = [100,100]
#Nave_lataria = pygame.Surface((20,20))
Nave_lataria = pygame.image.load('Desktop/Testes_com_Pygame/Nave_teste.png')
#Nave_lataria = pygame.image.load("millennium")
#Nave_lataria.fill((255,255,255))

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

#inicia o pygame
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Space Danger")


clock = pygame.time.Clock()

#----------------
position_x = 0
# 100 pixels por segundo
velocity_x = 100
#----------------

while True:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    
    if event.type == KEYDOWN:
        if event.key == K_UP:
            Nave[1] = Nave[1] - 10
        if event.key == K_DOWN:
            Nave[1] = Nave[1] + 10
        if event.key == K_RIGHT:
            Nave[0] = Nave[0] + 10
        if event.key == K_LEFT:
            Nave[0] = Nave[0] - 10

            
    #logica de varios asteroide
    Asteroide[1] = Asteroide[1] + 10
    if(Asteroide[1] >= 500):
        Asteroide[1] = 0
        Asteroide[0] = random.randint(0,600) 
	
    screen.fill((0,0,0))
    screen.blit(Nave_lataria , (Nave[0] , Nave[1]))
    
    screen.blit(Asteroide_lataria , (Asteroide[0] , Asteroide[1]))

    pygame.display.update()
