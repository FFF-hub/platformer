import pygame
from pygame.locals import *
import numpy
from random import randint
 
pygame.init()
pygame.mixer.init()

RES = (256, 192)
FLAGS = pygame.RESIZABLE
screen = pygame.display.set_mode(RES, flags = FLAGS, vsync = 1)

GAME_RUNNING = True

GAME_CLOCK = pygame.time.Clock()

bcg0 = pygame.image.load("vis/Untitled.png").convert()

while GAME_RUNNING:
	
	GAME_CLOCK.tick(60)
	
	for event in pygame.event.get():
		if event.type == VIDEORESIZE:
			screen = pygame.display.set_mode((event.w, event.h), flags = FLAGS, vsync = 1)
			bcg00 = pygame.transform.scale(bcg0, (event.w, event.h))
		if event.type == pygame.QUIT:
			GAME_RUNNING = False
	
	screen.blit(bcg00, (0, 0))

	pygame.display.update()

pygame.mixer.quit()
pygame.quit()
