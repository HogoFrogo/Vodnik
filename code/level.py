from logging.config import fileConfig
import math
from multiprocessing.connection import wait
from time import sleep
from traceback import format_exc
import pygame
from objects.bottle import Bottle
from objects.mug import Mug
from objects.spirit import Spirit
from objects.fisherman import Fisherman
from objects.pneu import Pneu
from objects.garbage import Garbage
from objects.vodnik import Vodnik
from objects.fish import Fish
from random import randint
import settings
from path_filler import ROOT_FOLDER,GRAPHICS_FOLDER

screen_width = settings.screen_width
screen_height = settings.screen_height

SKY_FILE = GRAPHICS_FOLDER + "sky.png"
MOUNTAINS_FILE = GRAPHICS_FOLDER + "sky.png"
LAND_FILE = GRAPHICS_FOLDER + "land.png"
POND_FILE = GRAPHICS_FOLDER + "pond.png"
SHELF_FILE = GRAPHICS_FOLDER + "shelf.png"
GLASS_CONTAINER_FILE = GRAPHICS_FOLDER + "glass_container.png"
WATER_FILE = GRAPHICS_FOLDER + "water.png"
FOREGROUND_FILE = GRAPHICS_FOLDER + "foreground.png"
MODAL_WINDOW_IMAGE_FILE = GRAPHICS_FOLDER + "modal.png"
FONT_FILE = ROOT_FOLDER + 'kyrou_7_wide_bold.ttf'

LOCALE_END = "Konec"
LOCALE_SCORE = "Skóre"

class Level:
	sky_picture = pygame.image.load(SKY_FILE)
	mountains_picture = pygame.image.load(MOUNTAINS_FILE)
	land_picture = pygame.image.load(LAND_FILE)
	pond_picture = pygame.image.load(POND_FILE)
	shelf_picture = pygame.image.load(SHELF_FILE)
	glass_container_picture = pygame.image.load(GLASS_CONTAINER_FILE)
	water_picture = pygame.image.load(WATER_FILE)
	foreground_picture = pygame.image.load(FOREGROUND_FILE)
	# shelf_position = (80,700)
	shelf_position = (20,160)
	# glass_container_position = (1000, 700)
	glass_container_position = (220, 175)
	# playground_border_right = 1100
	# playground_border_right = 80
	playground_border_right = 305
	playground_border_left = 20
	# level_border = 50
	level_border = 12
	# shelf_border = 300
	shelf_border = 80
	# reachable_y = 500
	reachable_y = 125

	# spawn_limit_x_left = 100
	# spawn_limit_x_right = 900
	spawn_limit_x_left = 25
	spawn_limit_x_right = 225
	# spawn_y = 300
	spawn_y = 75

	# fisherman_width_half = 150
	# fisherman_tolerance = 20
	# playground_bottom = 915
	fisherman_width_half = 42
	fisherman_width = 85
	fisherman_tolerance = 7
	playground_bottom = 229

	# vodnik_position_x = 200
	# vodnik_position_y = 700
	vodnik_position_x = 50
	vodnik_position_y = 160

	# vodnik_width = 300
	vodnik_width = 36
	vodnik_width_half = 18
	# spirits_below_fisherman_y = 400
	spirits_below_fisherman_y = 100

	# fish_width = 135
	fish_width = 33

	# glass_container_border_y = 600
	glass_container_border_y = 150

	# garbage_up=100
	garbage_up=25

	# fisherman_y=100
	fisherman_y=18

	spirit_disappears=35
	spirit_tolerance= 29
	spirit_width_half = 9

	modal_width=round(settings.screen_width/2)
	modal_height=round(settings.screen_height/2)
	frame=0
	garbage_tolerance=13

	def __init__(self,current_level,surface,create_overworld,change_coins,change_health,change_jump,difficulty):
		# general setup
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None
		self.difficulty = difficulty
		self.state = 'begin'
		self.player_name = "Mr. Croak"
		self.score=0

		# overworld connection 
		self.create_overworld = create_overworld
		self.current_level = current_level

		fish_a = Fish(450,700)
		fish_b = Fish(630,830)
		fish_c = Fish(500,600)
		fish_d = Fish(800,660)
		fish_e = Fish(200,800)
		fish_f = Fish(300,550)
		fish_g = Fish(770,740)
		self.all_fish = {fish_a,fish_b,fish_c,fish_d,fish_e,fish_f,fish_g}
		#self.all_fish = {Fish(450,700)}
		self.all_fish = {Fish(112,175)}
		fish_2 =Fish(80,162)
		fish_2.direction=-1
		self.all_fish.add(fish_2)
		fish_3 =Fish(75,153)
		self.all_fish.add(fish_3)

		# fisherman = Fisherman(-300,100)
		fisherman = Fisherman(-75,self.fisherman_y)
		self.fishermen = [fisherman]

		# garbage_a = Bottle(850,300)
		# garbage_b = Pneu(630,300)
		garbage_a = Bottle(212,75)
		garbage_b = Pneu(157,75)
		self.all_garbage = [garbage_a,garbage_b]

		spirit = Spirit(157,75)
		self.spirits = {spirit}
		self.spirits.remove(spirit)

		self.vodnik = Vodnik(self.vodnik_position_x,self.vodnik_position_y)

		self.cover_surf = pygame.Surface((self.display_surface.get_width(), self.display_surface.get_height()))
		self.cover_surf.set_colorkey((255, 255, 255))
		self.cover_surf.fill((255,220,0))
		self.cover_surf.set_alpha(60) 
		
	def load_ingame_window_background(self):
		window = (self.modal_width,self.modal_height)
		background = pygame.Surface(window)
		background.fill((102, 187, 106))
		return background

	def enter_start_window(self):
		self.view_start_window(self.level_name,self.level_img,self.croak_speak_sound)		

	def view_image(self,img_path):
		picture = pygame.image.load(img_path)
		#picture = pygame.transform.scale(myimage, (280, 140))
		
		self.display_surface.blit(picture, (0, 0))

	def view_image_2(self,picture,coordinates=(0,0)):
		self.display_surface.blit(picture, coordinates)

	def view_image(self,picture):
		self.display_surface.blit(picture, (0, 0))


	def run(self):
		self.frame+=1
		self.get_input()
		#draw_sky
		self.view_image_2(self.sky_picture)
		#draw_mountains
		self.view_image_2(self.mountains_picture)
		#draw_land
		self.view_image_2(self.land_picture)
		#draw_pond
		self.view_image_2(self.pond_picture)

		#draw_shelf
		self.view_image_2(self.shelf_picture,self.shelf_position)

		#draw_fishermen
		for fisherman in self.fishermen:
			if not fisherman.status=="go_home_fish" and not fisherman.status=="go_home_mug":
				if fisherman.x>self.playground_border_right:
					fisherman.direction=-1
				elif fisherman.x<self.playground_border_left:
					fisherman.direction=1
			fisherman.update()
			fisherman.draw(self.display_surface)

		#draw_glass_container
		self.view_image_2(self.glass_container_picture,self.glass_container_position)

		#draw_vodnik
		self.vodnik.update()
		self.vodnik.draw(self.display_surface)

		#draw_spirits
		spirit = Spirit(0,0)
		to_be_removed={spirit}
		to_be_removed.remove(spirit)
		for spirit in self.spirits:
			if spirit.y<self.spirit_disappears:
				to_be_removed.add(spirit)
			spirit.update()
			spirit.draw(self.display_surface)
		for spirit in to_be_removed:
			self.spirits.remove(spirit)
		#draw_fish
		for fish in self.all_fish:
			if fish.x+self.fish_width>self.playground_border_right and fish.status=="run" and fish.direction==1:
				fish.turn()
			elif fish.x<self.playground_border_left and fish.status=="run" and fish.direction==-1:
				fish.turn()
			fish.update()
			fish.draw(self.display_surface)
		
		#draw_garbage
		for garbage in self.all_garbage:
			if garbage.y>self.playground_bottom:
				garbage.speed_y=0
			garbage.update()
			garbage.draw(self.display_surface)

		#draw_water
		self.view_image_2(self.water_picture)

		#draw_foreground
		self.view_image_2(self.foreground_picture)

		self.vodnik.draw_inventory(self.display_surface)
		
		#draw_score
		# font = pygame.font.Font('../nevis.ttf', 24)
		font = pygame.font.Font(FONT_FILE, 7)
		text = font.render(LOCALE_SCORE + ": {0}".format(self.score), True, pygame.color.Color('Black'))
		# self.display_surface.blit(text, (20, 20))
		self.display_surface.blit(text, (5, 5))
		
		pygame.display.flip()

		self.check_end()
		self.check_fisherman()
		self.check_fish()
		self.check_garbage()

		if randint(0,200)<1:
			self.all_garbage.append(Pneu(randint(self.spawn_limit_x_left,self.spawn_limit_x_right),self.spawn_y))
		level = round(self.frame/1300)
		if randint(0,150)<1+level:
			if randint(0,1)==1:
				self.fishermen.append(Fisherman(-300,self.fisherman_y))
			else:
				self.fishermen.append(Fisherman(1300,self.fisherman_y))

	def check_end(self):
		if not self.all_fish:
			self.state="end"
			self.view_window(LOCALE_SCORE + ": {}".format(self.score),MODAL_WINDOW_IMAGE_FILE)

	

	def view_window(self,text_content,image_path,dialog_sound=""):
			if dialog_sound != "":
				dialog_sound.play()
			next_state=self.state
			self.state = 'modal'
			background = self.load_ingame_window_background()
			#Insert text
			# font = pygame.font.SysFont('Arial', 24)

			myimage = pygame.image.load(image_path)
			imagerect = myimage.get_rect()
			picture = pygame.transform.scale(myimage, (self.modal_width, self.modal_height))
			
			x1, y1 = background.get_width()//2, background.get_height()//2
			background.blit(picture, (x1 - picture.get_width() // 2, y1 - picture.get_height() // 2))
			
			font = pygame.font.Font(FONT_FILE, 13)
			text = font.render(LOCALE_END, True, pygame.color.Color('Black'))
			# background.blit(text, (20, 20))
			background.blit(text, (20, 15))
			
			font = pygame.font.Font(FONT_FILE, 7)
			text = font.render(text_content, True, pygame.color.Color('Black'))
			# background.blit(text, (20, 20))
			background.blit(text, (20, 35))
			
			x, y = self.display_surface.get_width()//2, self.display_surface.get_height()//2
			self.display_surface.blit(background,(x - background.get_width() // 2, y - background.get_height() // 2))

			pygame.display.flip()
			sleep(2)
			# wait(200)
			while self.state == 'modal':
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_k:
							self.state = next_state

	def check_fisherman(self):
		to_be_removed = ""
		for fisherman in self.fishermen:
			if fisherman.status=="sitting":
				if randint(0,200)<1:
					self.all_garbage.append(Bottle(fisherman.x+self.fisherman_width_half,self.spawn_y))
			if fisherman.status == "run" and fisherman.x in range(fisherman.goal-fisherman.speed_x,fisherman.goal+fisherman.speed_x):
				fisherman.speed_x=0
				fisherman.change_status("sitting")
			
			if not fisherman.fish=="":
				fisherman.time_to_catch-=1
				if fisherman.time_to_catch==0:
					fisherman.change_status("catching")
					self.all_fish.remove(fisherman.fish)
				if fisherman.time_to_catch==-30:
					fisherman.go_home("fish")
			else:
				fisherman.time_to_catch=120
			if fisherman.status=="drowning":
				fisherman.time_to_drown-=1
				if fisherman.time_to_drown<1:
					print("dead")
					self.spirits.add(Spirit(fisherman.x+self.fisherman_width_half-self.spirit_width_half,fisherman.y+self.spirits_below_fisherman_y))
					to_be_removed = fisherman
			if fisherman.status=="angry":
				fisherman.time_to_cool_down-=1
				if fisherman.time_to_cool_down==0:
					garbage = fisherman.inventory
					fisherman.inventory=""
					self.all_garbage.append(garbage)
					fisherman.change_status("sitting")
					fisherman.time_to_cool_down=fisherman.time_to_cool_down_max
			if fisherman.status=="happy":
				fisherman.time_to_cool_down-=1
				if fisherman.time_to_cool_down==0:
					fisherman.go_home("mug")
		if not to_be_removed=="":
			self.fishermen.remove(to_be_removed)

	def check_fish(self):
		for fish in self.all_fish:
			for fisherman in self.fishermen:
				if fisherman.status=="sitting" and fisherman.fish=="":
					if fish.direction==1 and round(fish.x)+self.fish_width in range(fisherman.x+self.fisherman_width_half-self.fisherman_tolerance,fisherman.x+self.fisherman_width_half+self.fisherman_tolerance) and fish.status=="run":
						fisherman.catch(fish)
					elif fish.direction==-1 and round(fish.x) in range(fisherman.x+self.fisherman_width_half-self.fisherman_tolerance,fisherman.x+self.fisherman_width_half+self.fisherman_tolerance) and fish.status=="run":
						fisherman.catch(fish)



	def check_garbage(self):
		#cleaned_garbage = {Pneu(630,300)}
		to_be_removed = ""
		for garbage in self.all_garbage:
			# print(garbage.x)
			if garbage.x>self.glass_container_position[0]-20 and garbage.y>self.glass_container_border_y and isinstance(garbage,Bottle):
				to_be_removed = garbage
		if not to_be_removed=="":
			self.all_garbage.remove(to_be_removed)
			self.score += to_be_removed.score

	def get_input(self):
		keys = pygame.key.get_pressed()
		self.vodnik.speed_x = 0
		if keys[pygame.K_d]:
			self.vodnik.go_right()
		if keys[pygame.K_a]:
			self.vodnik.go_left()
		if keys[pygame.K_k]:
			to_be_removed=""
			if self.vodnik.empty_hands and not keys[pygame.K_w]:
				for garbage in self.all_garbage:
					if garbage.y > self.reachable_y and (garbage.x+garbage.width_half) in range(self.vodnik.x-self.garbage_tolerance,self.vodnik.x+self.vodnik_width+self.garbage_tolerance):
						to_be_removed = garbage
						break
				if not to_be_removed=="":
					self.vodnik.pick_up(to_be_removed)
					self.all_garbage.remove(to_be_removed)
				elif self.vodnik.x<self.shelf_border:
					self.vodnik.pick_up(Mug(0,0))
			else:
				if keys[pygame.K_w] and isinstance(self.vodnik.inventory,Mug):
					success = False
					for spirit in self.spirits:
						if self.vodnik.x+self.vodnik_width_half in range(spirit.x+self.spirit_width_half-self.spirit_tolerance,spirit.x+self.spirit_width_half+self.spirit_tolerance):
							success = True
							self.vodnik.drop_inventory()
							to_be_removed=spirit
							self.score += 100
							break
					if success:
						self.spirits.remove(to_be_removed)
		if keys[pygame.K_l]:
			if self.vodnik.empty_hands == False:
				self.vodnik.inventory.x=self.vodnik.x+self.vodnik_width_half-self.vodnik.inventory.width_half
				self.vodnik.inventory.y=self.vodnik.y
				self.vodnik.inventory.speed_y = self.vodnik.inventory.max_speed
				if keys[pygame.K_w]:
					self.vodnik.inventory.y=self.vodnik.y-self.garbage_up
					success = False
					to_be_moved =""
					for fisherman in self.fishermen:
						if self.vodnik.x+self.vodnik_width_half in range(fisherman.x,fisherman.x+self.fisherman_width) and fisherman.status=="catching":
							success= True
							print("catching!")
							if isinstance(self.vodnik.inventory,Garbage):
								fisherman.drop_fish()
								if isinstance(self.vodnik.inventory,Pneu):
									fisherman.change_status("drowning")
									self.score+=50
									to_be_moved = fisherman
								elif isinstance(self.vodnik.inventory,Bottle):
									fisherman.change_status("angry")
									fisherman.inventory=self.vodnik.inventory
								elif isinstance(self.vodnik.inventory,Mug):
									fisherman.change_status("happy")
									self.score -= 20
							break
					if not success:
						for fisherman in self.fishermen:
							# if fisherman.status=="catching":
							if self.vodnik.x+self.vodnik_width_half in range(fisherman.x,fisherman.x+self.fisherman_width) and fisherman.status=="sitting":
								success= True
								print("sitting!")
								if isinstance(self.vodnik.inventory,Pneu):
									fisherman.change_status("drowning")
									self.score+=50
									to_be_moved = fisherman
								elif isinstance(self.vodnik.inventory,Bottle):
									fisherman.change_status("angry")
									fisherman.inventory=self.vodnik.inventory
								elif isinstance(self.vodnik.inventory,Mug):
									fisherman.change_status("happy")
									self.score -= 20
								break
						if not success:
							self.all_garbage.append(self.vodnik.inventory)
						if not to_be_moved=="":
							self.fishermen.remove(to_be_moved)
							self.fishermen.append(to_be_moved)
				else:
					self.all_garbage.append(self.vodnik.inventory)
				self.vodnik.drop_inventory()

		if self.vodnik.x+self.vodnik_width > self.playground_border_right and self.vodnik.direction==1:
			self.vodnik.speed_x = 0
		elif self.vodnik.x<self.playground_border_left and self.vodnik.direction==-1:
			self.vodnik.speed_x = 0