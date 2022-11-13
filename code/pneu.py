import pygame 
from random import randint
import math

from garbage import Garbage

class Pneu(Garbage):
	img_path = "../graphics/tire.png"
	x = 0
	y = 0
	speed_x = 1 # 5
	speed_y = 1 # 5
	direction =1
	name = "tire"
	picture = pygame.image.load(img_path)	
	width_half = 21

	def __init__(self,x,y):
		self.x=x
		self.y=y

	def draw(self,display_surface):
		if self.direction == 1:
			picture_directed =pygame.transform.flip(self.picture, True, False)
		else:
			picture_directed = self.picture
		display_surface.blit(picture_directed, (self.x, self.y))

	def update(self):
		self.y+=self.speed_y