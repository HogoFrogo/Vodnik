import pygame 
from random import randint
from path_filler import GRAPHICS_FOLDER

class Garbage():
	img_path = GRAPHICS_FOLDER + "garbage.png"
	x = 0
	y = 0
	max_speed=1 # 5
	speed_x = 1 # 5
	speed_y = 1 # 5
	direction =1
	score = 10
	name = "garbage"
	width_half = 15

	def __init__(self,x,y):
		self.x=x
		self.y=y

	def draw(self,display_surface):
		picture = pygame.image.load(self.img_path)	
		if self.direction == 1:
			picture_directed =pygame.transform.flip(picture, True, False)
		else:
			picture_directed = picture
		display_surface.blit(picture_directed, (self.x, self.y))

	def update(self):
		self.y+=self.speed_y