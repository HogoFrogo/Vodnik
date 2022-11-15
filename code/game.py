
import pygame

from level import Level
from path_filler import ROOT_FOLDER,GRAPHICS_FOLDER,AUDIO_FOLDER

ICON_FILE = GRAPHICS_FOLDER + 'icon.png'
GAME_MUSIC_FILE = AUDIO_FOLDER + 'bleeps-and-bloops-classic-arcade-game-116838.mp3'
HIGHSCORE_FILE = ROOT_FOLDER + 'highscores.txt'
HIGHSCORE_FILE_2 = ROOT_FOLDER + "highscore.json"

class Game:
	def __init__(self, screen, music_volume=50,sounds_volume=50):
		# game attributes
		self.max_level = 7
		self.max_health = 100
		self.cur_health = 100
		self.coins = 0
		self.max_jump = 48
		self.cur_jump = 0
		self.screen = screen
		programIcon = pygame.image.load(ICON_FILE)
		pygame.display.set_icon(programIcon)
		pygame.mouse.set_visible(False)

		self.music_volume = music_volume
		self.sounds_volume = sounds_volume

		self.player_name = ""

		self.level_bg_music =""
		# audio 
		try:
			self.level_bg_music = pygame.mixer.Sound(GAME_MUSIC_FILE)
		except:
			print("Music not loaded.")

		self.status = 'run'

		# user interface 
		self.level = Level(0,self.screen,self.create_overworld,self.change_coins,self.change_health,self.change_jump,"easy")
		self.status = 'level'
		if(not self.level_bg_music==""):
			self.level_bg_music.play(loops = -1)


	def create_level(self,current_level,difficulty):
		print("sounds_volume_in_level")
		print(self.sounds_volume)
		self.level = Level(current_level,self.screen,self.create_overworld,self.change_coins,self.change_health,self.change_jump,difficulty)
		self.status = 'level'
		#self.level_bg_music = pygame.mixer.Sound(levels[current_level]['level_bg_music'])
		# self.level_bg_music.set_volume(self.music_volume)
		# self.level_bg_music.play(loops = -1)
		#self.level.change_sounds_volume(self.sounds_volume)

	def create_overworld(self,current_level,new_max_level,difficulty):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		if(not self.level_bg_music==""):
			self.level_bg_music.stop()

	def change_coins(self,amount):
		self.coins += amount

	def change_health(self,amount):
		self.cur_health += amount
		if(self.cur_health>self.max_health):
			self.cur_health = self.max_health

	def change_jump(self,amount):
		self.cur_jump += amount
		if(self.cur_jump>self.max_jump):
			self.cur_jump = self.max_jump

	def change_music_volume(self,new_music_volume):
		self.music_volume = new_music_volume
		if(not self.level_bg_music==""):
			self.level_bg_music.set_volume(new_music_volume)

	def change_sounds_volume(self,new_sounds_volume):
		print(new_sounds_volume)
		self.sounds_volume = new_sounds_volume

	def check_game_over(self):
		if self.cur_health <= 0:
			self.status = 'end'
			if(not self.level_bg_music==""):
				self.level_bg_music.stop()

	def load_score_board(self):
		with open(HIGHSCORE_FILE, 'r') as f:
			option = f.readline().split(" = ")
			player_1 = [option[0], int(option[1])]
			option = f.readline().split(" = ")
			player_2 = [option[0], int(option[1])]
			option = f.readline().split(" = ")
			player_3 = [option[0], int(option[1])]
			option = f.readline().split(" = ")
			player_4 = [option[0], int(option[1])]
			option = f.readline().split(" = ")
			player_5 = [option[0], int(option[1])]
			option = f.readline().split(" = ")
			player_6 = [option[0], int(option[1])]
			option = f.readline().split(" = ")
			player_7 = [option[0], int(option[1])]
			option = f.readline().split(" = ")
			player_8 = [option[0], int(option[1])]
			option = f.readline().split(" = ")
			player_9 = [option[0], int(option[1])]
			option = f.readline().split(" = ")
			player_10 = [option[0], int(option[1])]
		return [player_1,player_2,player_3,player_4,player_5,player_6,player_7,player_8,player_9,player_10]

	def handle_highscore(self):
		scores = self.load_score_board()
		new_score = [self.player_name,self.level.score]
		scores.append(new_score)
		scores = sorted(scores, key=lambda x: x[1],reverse=True)

		f = open(HIGHSCORE_FILE, "w")
		for score in scores:
			f.write("{} = {}\n".format(score[0],score[1]))
		
		# highscores export
		f = open(HIGHSCORE_FILE_2, "w")
		i = 0
		f.write('{"scores":[')
		for score in scores:
			f.write('{"name":"')
			f.write(score[0])
			f.write('","score":')
			f.write(str(score[1]))
			f.write('}')
			# f.write('{"name":"","score":}')
			i += 1
			if i<10:
				f.write(',')
			else:
				break
		f.write('}]}')
			
		
	def run(self,player_name=""):
		if self.level.state == 'end':
			self.handle_highscore()
			self.status = "end"
			if(not self.level_bg_music==""):
				self.level_bg_music.stop()
		else:
			self.level.run()
			self.check_game_over()