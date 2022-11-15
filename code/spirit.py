import pygame 
from random import randint
from path_filler import GRAPHICS_FOLDER
from animated_object import AnimatedObject

class Spirit(AnimatedObject):
	img_path = GRAPHICS_FOLDER + "spirit/"
	x = 0
	y = 0
	speed_x = 0
	speed_y = 0.5
	direction =1
	i_max=1
	frame_index=0

	status="run"
	pictures = AnimatedObject.load_pictures(img_path,["run"])

	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.frame_index=0

	def draw(self,display_surface):
		# picture = self.pictures[self.frame_index]
		picture = self.get_picture()
		if self.direction == 1:
			picture_directed =pygame.transform.flip(picture, True, False)
		else:
			picture_directed = picture
		display_surface.blit(picture_directed, (self.x, self.y))

	def update(self):
		self.y-=self.speed_y