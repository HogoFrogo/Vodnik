import pygame 
from random import randint
from path_filler import GRAPHICS_FOLDER

from garbage import Garbage

class Mug(Garbage):
	img_path = GRAPHICS_FOLDER + "mug.png"
	x = 0
	y = 0
	max_speed=1 # 5
	speed_x = 1 # 5
	speed_y = 1 # 5
	direction =1
	name = "mug"
	picture = pygame.image.load(img_path)	
	width_half = 11

	def __init__(self,x,y):
		self.x=x
		self.y=y

	def draw(self,display_surface):
		display_surface.blit(self.picture, (self.x, self.y))

	def update(self):
		self.y+=self.speed_y