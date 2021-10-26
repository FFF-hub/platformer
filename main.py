import pygame
from pygame.locals import *
import numpy
from random import randint
 
pygame.init()
pygame.mixer.init()

RES = (256*3, 192*3)
FLAGS = pygame.RESIZABLE
screen = pygame.display.set_mode(RES, vsync = 1)

GAME_RUNNING = True

GAME_CLOCK = pygame.time.Clock()

bcg0 = pygame.image.load("vis/Untitled.png").convert()
bcg00 = pygame.transform.scale(bcg0, RES)

class Box:
	def __init__(s):
		s.img0 = pygame.image.load("vis/box0.png").convert()
		s.scale_factor = 4
		s.avatar = pygame.transform.scale(s.img0, (8*s.scale_factor, 8*s.scale_factor))
		s.x = [0, 8]
		s.y = [0, 8]
		
	def Draw(s):
		global screen
		screen.blit(s.avatar, (s.x[0], s.y[0]))
		
	def get_geo(s):
		return s.x, s.y
		
class Double(Box):
	def __init__(s):
		super().__init__()
		s.geo = [(s.x, s.y), (s.x, s.y)]
		

class Player:
	"""Player class, responsible for players inputs, physics and drawing"""
	def __init__(s):
		s.img0 = pygame.image.load("vis/player0.png").convert_alpha()
		s.scale_factor = 4
		s.avatar = pygame.transform.scale(s.img0, (8*s.scale_factor, 8*s.scale_factor))
		s.pressed_keys = []
		s.x = [0, 0, 0.5] # [pos, vel, acc]
		s.y = [0, 0, 1]
		
		s.g_acc = 2
		
		s.lr_keys_idle = False
		
		s.max_xv = 10
		s.max_yv = 30
		
		s.jump = False
		
		s.acc_lr = False
		
	def Inputs(s):
		""" take inputs from keyboard """
		s.pressed_keys = pygame.key.get_pressed()
		
		
	def Physics(s):
		""" transform inputs into behavior """
		if s.pressed_keys[pygame.K_RIGHT] and abs(s.x[1]) < s.max_xv:
			s.x[1] += s.x[2]
		elif s.pressed_keys[pygame.K_LEFT] and abs(s.x[1]) < s.max_xv:
			s.x[1] -= s.x[2]
			
		if s.pressed_keys[pygame.K_UP]:
			s.y[1] = -1 * s.max_yv
		
		if not s.pressed_keys[pygame.K_RIGHT] and not s.pressed_keys[pygame.K_LEFT]:
			s.lr_keys_idle = True
		else:
			s.lr_keys_idle = False
		
		if s.lr_keys_idle and (s.x[1] - 0) > 0:
			s.x[1] -= s.x[2]
		elif s.lr_keys_idle and (s.x[1] - 0) < 0:
			s.x[1] += s.x[2]
			
		if s.x[1] >= s.max_xv:
			s.x[1] -= 1
		elif s.x[1] <= -1 * s.max_xv:
			s.x[1] += 1
			
		if not s.jump and not (s.y[0] + s.y[1] >= RES[1]):
			if s.y[1] < s.max_yv:
				s.y[1] += s.g_acc
			
		
		if (s.y[0] + 32) + s.y[1] >= RES[1]:
			s.y[0] = RES[1] - 32
			s.y[1] = 0	
		
		s.x[0] += s.x[1]
		s.y[0] += s.y[1]
		
	def Draw(s):
		""" execute behavior aka: show the resoult """
		global screen
		screen.blit(s.avatar, (s.x[0], s.y[0]))
		
		
""" add class block, floor, and rendering method
	create fast collision detection algorithm"""
		
Gameur = Player()
Box0 = Box()

while GAME_RUNNING:
	
	GAME_CLOCK.tick(60)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME_RUNNING = False
	
	Gameur.Inputs()
	
	Gameur.Physics()
	
	
	screen.blit(bcg00, (0, 0))
	Box0.Draw()
	Gameur.Draw()
	
	pygame.display.update()

pygame.mixer.quit()
pygame.quit()
