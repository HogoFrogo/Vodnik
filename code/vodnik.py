import pygame 
from random import randint
from path_filler import GRAPHICS_FOLDER

from animated_object import AnimatedObject
from pneu import Pneu

class Vodnik(AnimatedObject):
	img_path = GRAPHICS_FOLDER + "vodnik/"
	x = 0
	y = 0
	max_speed= 5 # 5
	speed_x = 0
	direction =1
	empty_hands = True
	inventory = ""
	# inventory_x = 1000
	# inventory_y = 50
	inventory_x = 270
	inventory_y = 200

	status="run"
	frame_index=0
	pictures = AnimatedObject.load_pictures(img_path,["run"])
	
	def __init__(self,x,y):
		self.x=x
		self.y=y

	def draw(self,display_surface):
		# picture = pygame.image.load(self.img_path)	
		picture = self.get_picture()
		if self.direction == 1:
			picture_directed =pygame.transform.flip(picture, True, False)
		else:
			picture_directed = picture
		display_surface.blit(picture_directed, (self.x, self.y))

	def draw_inventory(self,display_surface):
		display_surface.blit(pygame.image.load(GRAPHICS_FOLDER + "inventory.png"),(self.inventory_x-7,self.inventory_y-7))
		if not self.empty_hands and not self.inventory=="":
			if isinstance(self.inventory,Pneu):
				display_surface.blit(pygame.image.load(self.inventory.img_path),(self.inventory_x,self.inventory_y+5))
			else:
				display_surface.blit(pygame.image.load(self.inventory.img_path),(self.inventory_x+10,self.inventory_y+5))

	def update(self): 
		self.x+=self.speed_x*self.direction

	def go_right(self):
		self.direction = 1
		self.speed_x = self.max_speed

	def go_left(self):
		self.direction = -1
		self.speed_x = self.max_speed

	def pick_up(self,object):
		self.empty_hands = False
		self.inventory = object

	def drop_inventory(self):
		self.inventory=""
		self.empty_hands=True