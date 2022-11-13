import pygame 
from random import randint
import math
import os

from animated_object import AnimatedObject

class Fisherman(AnimatedObject):
	img_path = "../graphics/fisherman/"
	x = 0
	y = 0
	max_speed= 4 # 15
	speed_x = 4 # 15
	direction =1
	time_to_catch = 120
	time_to_drown = 60
	time_to_cool_down_max = 100
	time_to_cool_down = 100
	empty_hands = True
	inventory = ""
	status="run"
	fish=""

	i_max=1
	frame_index=0
	pictures = AnimatedObject.load_pictures(img_path,["run","angry","catching","drowning","go_home_fish","go_home_mug","happy","sitting"])

	def __init__(self,x,y):
		self.x=x
		self.y=y
		# self.goal=randint(100,1000)
		self.goal=randint(25,248)
		self.frame_index=0

	def draw(self,display_surface):
		picture = self.get_picture()

		if self.direction == 1:
			picture_directed =pygame.transform.flip(picture, True, False)
		else:
			picture_directed = picture
		display_surface.blit(picture_directed, (self.x, self.y))

	def update(self):
		self.x+=self.speed_x*self.direction

	def go_home(self,type):
		self.change_status("go_home_"+type)
		self.direction=-self.direction
		self.speed_x=self.max_speed
