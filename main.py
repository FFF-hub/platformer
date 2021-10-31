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

# THIS IS RETARDED, DONT USE THIS! (CODE BELOW)
#class Box:
#	def __init__(s):
#		s.img0 = pygame.image.load("vis/box0.png").convert()
#		s.scale_factor = 4
#		s.avatar = pygame.transform.scale(s.img0, (8*s.scale_factor, 8*s.scale_factor))
#		s.x = [0, 8]
#		s.y = [0, 8]
#		
#	def Draw(s):
#		global screen
#		screen.blit(s.avatar, (s.x[0], s.y[0]))
#		
#	def get_geo(s):
#		return s.x, s.y
#		
#class Double(Box):
#	def __init__(s):
#		super().__init__()
#		s.mask = [1, 1]
#		
#	#def get_geo(s):
		
class Shape:
	""" General Class responsible for creating shapes """
	def __init__(s, geometry, position, color, width):
		s.geometry = geometry			# geometry of the shape
		s.position = position			# position on the screen
		s.old_position = position		# used to checked if object moved
		s.color = color
		s.width = width
		s.moved = False
		for i in range(0, len(s.geometry)):
			s.geometry[i][0] += s.position[0]
			s.geometry[i][1] += s.position[1]

	def R(s, Angle):
		""" Rotate Shape around self [0, 0] point """
		# work in progres
		s.geometry = s.geometry
		
	def T(s, position):
		""" Update Shape geometry if changed """
		if (s.position[0] - position[0] != 0 or
		    s.position[1] - position[1] != 0):
			s.moved = True
		if s.moved:
			for i in range(0, len(s.geometry)):
				s.geometry[i][0] += position[0] - s.position[0]
				s.geometry[i][1] += position[1] - s.position[1]
			s.moved = False
			s.position = position		

	def Draw(s, screen):
		""" Draw Shape on particular screen """
		pygame.draw.polygon(screen, s.color, s.geometry, s.width)

		
class BlockFactory:
	""" Factory that creates Shapes of predefined geometry """
	def __init__(s):
		s.sf = 6		# scale factor

	def get_square(s) -> Shape:
		""" Returns a square shape
			[]
		 """
		return Shape([[0, 0],
					  [0, 8 * s.sf],
					  [8 * s.sf, 8 * s.sf],
					  [8 * s.sf, 0]],
					  (0, 0),
					  (0, 0, 0),
					   0)
	
	def get_double(s) -> Shape:
		""" Return a double block
			[][]
		 """
		return Shape([[0, 0],
					  [0, 8 * s.sf],
					  [8 * 2 * s.sf, 8 * s.sf],
					  [8 * 2 * s.sf, 0]],
					  (0, 0),
					  (0, 0, 0),
					   0)

	def get_quad(s) -> Shape:
		""" Returns a square shape
			[][]
			[][]
		 """
		return Shape([[0, 0],
					  [0, 8 * 2 * s.sf],
					  [8 * 2 * s.sf, 8 * 2 * s.sf],
					  [8 * 2 * s.sf, 0]],
					  (0, 0),
					  (0, 0, 0),
					   0)

	def get_line(s) -> Shape:
		""" Returns a square shape
			[][][][]
		 """
		return Shape([[0, 0],
					  [0, 8 * s.sf],
					  [8 * 4 * s.sf, 8 * s.sf],
					  [8 * 4 * s.sf, 0]],
					  (0, 0),
					  (0, 0, 0),
					   0)

	def get_lblock(s) -> Shape:
		""" Returns a square shape
			[]
			[]
			[][]
		 """
		return Shape([[0, 0],
					  [0, 8 * 3 * s.sf],
					  [8 * 2 * s.sf, 8 * 3 * s.sf],
					  [8 * 2 * s.sf, 8 * 2 * s.sf],
					  [8 * s.sf, 8 * 2 * s.sf],
					  [8 * s.sf, 0]],
					  (0, 0),
					  (0, 0, 0),
					   0)

	def get_tblock(s) -> Shape:
		""" Returns a square shape
			[]
			[][]
			[]
		 """
		return Shape([[0, 0],
					  [0, 8 * 3 * s.sf],
					  [8 * s.sf, 8 * 3 * s.sf],
					  [8 * s.sf, 8 * 2 * s.sf],
					  [8 * 2 * s.sf, 8 * 2 * s.sf],
					  [8 * 2 * s.sf, 8 * s.sf],
					  [8 * s.sf, 8 * s.sf],
					  [8 * s.sf, 0]],
					  (0, 0),
					  (0, 0, 0),
					   0)



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
		
		# gravity falling and maximum down Y velocity limiter
		if not (s.y[0] + s.y[1] >= RES[1]):
			if s.y[1] < s.max_yv:
				s.y[1] += s.g_acc
		
		# Jumping 
		if s.pressed_keys[pygame.K_UP] and not s.jump:
			if not s.jump:
				s.jump = True
				s.y[1] = -1 * s.max_yv/1.2
		
		if (s.y[0] + 32) + s.y[1] >= RES[1]:
			s.jump = False
			s.y[0] = RES[1] - 32
			s.y[1] = 0	
		
		s.x[0] += s.x[1]
		s.y[0] += s.y[1]
	
	def get_pos(s):
		return s.x[0], s.y[0]
		
	def get_vel(s):
		return s.x[1], s.y[1]
		
	def get_acc(s):
		return s.x[2], s.y[2]
	
	def Draw(s):
		""" execute behavior aka: show the result """
		global screen
		screen.blit(s.avatar, (s.x[0], s.y[0]))
		
		
""" add class block, floor, and rendering method
	create fast collision detection algorithm"""
		
Gameur = Player()
BF = BlockFactory()
Double01 = BF.get_tblock()
Double01.T((200, 200))
Double01.color = (255, 255, 255)
Double01.width = 0

xd = 0

while GAME_RUNNING:
	
	GAME_CLOCK.tick(60)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME_RUNNING = False
	
	Gameur.Inputs()
	
	Gameur.Physics()
	
	
	screen.blit(bcg00, (0, 0))
	Gameur.Draw()
	xd += 0.5
	Double01.T((xd, 0)) 
	Double01.Draw(screen)
		
	#print(Gameur.ground_contact, Gameur.jump)
	
	pygame.display.update()

pygame.mixer.quit()
pygame.quit()
