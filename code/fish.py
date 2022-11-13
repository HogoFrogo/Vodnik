import pygame 
from random import randint
import math

from animated_object import AnimatedObject

class Fish(AnimatedObject):
	img_path = "../graphics/fish/"
	x = 0
	y = 0
	speed_max = 0.7
	speed_x = 0.7 # 5
	direction =1
	# picture = pygame.image.load(img_path+"{}.png".format(0))

	status="run"
	pictures = AnimatedObject.load_pictures(img_path,["run","turn","eating"])

	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.frame_index = 0

	def draw(self,display_surface):
		self.picture = self.get_picture()
		if self.direction == 1:
			picture_directed =pygame.transform.flip(self.picture, True, False)
		else:
			picture_directed = self.picture
		display_surface.blit(picture_directed, (self.x, self.y))

	def update(self):
		self.x+=self.speed_x*self.direction
		if self.status=="turn":
			self.turning-=1
			print(self.turning)
			if self.turning<0:
				self.change_status("run")
				self.speed_x=self.speed_max
				self.direction=-self.direction

	def turn(self):
		self.change_status("turn")
		self.speed_x = 0
		self.turning = 5