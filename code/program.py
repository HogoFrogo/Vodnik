from multiprocessing.connection import wait
from time import sleep
from fikmat_api import display_score_on_led_display
import settings
from path_filler import ROOT_FOLDER,GRAPHICS_FOLDER,AUDIO_FOLDER

# check if pygame and pygame_menu not installed:
import sys
import subprocess
import pkg_resources

required = {'pygame', 'pygame_menu','requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
	# install via pip
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
	# if pip is not installed
		# view commands in readme.md to install pygame and pygame_menu libs

import pygame, sys
from game import Game
import pygame_fikmat_controls

import pygame_menu
# from lib.pygame_menu.pygame_menu import pygame_menu

LOCALE_PROGRAM_NAME = "Vodník František"
LOCALE_PLAY = "HRÁT"
LOCALE_PLAY_2 = "Hrát"
LOCALE_SAVE = "Uložit"
LOCALE_CONGRATULATIONS = "Dobrá práce!"
LOCALE_SCOREBOARD = "TABULKA VÍTĚZŮ"
LOCALE_INSTRUCTIONS = "INSTRUKCE"
LOCALE_CREDITS = "O HŘE"
LOCALE_QUIT = "KONEC"
LOCALE_NAME = "Jméno"
LOCALE_ADD_CHARACTER = "Přidat písmeno"
LOCALE_DELETE_CHARACTER = "Umazat písmeno"
LOCALE_CREDITS_LABEL_1 = "Programming: Samuel Machat"
LOCALE_CREDITS_LABEL_2 = "Grafika: Lenka Holubcová"
LOCALE_CREDITS_LABEL_3 = "S láskou k Hogo Frogo"
LOCALE_CREDITS_LABEL_4 = "pro FIKMAT"

PLAYERNAME_FILE = ROOT_FOLDER + 'playername.txt'
MAIN_MENU_MUSIC_FILE = AUDIO_FOLDER + 'vodevil-15550.mp3'
FONT_FILE = ROOT_FOLDER + 'kyrou_7_wide_bold.ttf'
MENU_IMAGE_FILE = GRAPHICS_FOLDER + "menu.png"
HIGHSCORE_FILE = ROOT_FOLDER + 'highscores.txt'
HIGHSCORE_FILE_2 = ROOT_FOLDER + "highscore.json"
PYGAME_LOGO_FILE = GRAPHICS_FOLDER + 'pygame_logo.png'

def load_player_name():
	with open(PLAYERNAME_FILE, 'r') as f:
		return f.readline()

screen_width = settings.screen_width
screen_height = settings.screen_height
player_name = load_player_name()

class Program:
	# font = pygame_menu.font.FONT_NEVIS
	PROGRAM_NAME = LOCALE_PROGRAM_NAME

	def __init__(self):
		# Pygame setup
		pygame.init()
		self.main_menu_music=""
		try:
			self.main_menu_music = pygame.mixer.Sound(MAIN_MENU_MUSIC_FILE)
		except:
			print("Music not loaded")

		self.scoreboard = self.load_score_board()
		font = pygame.font.Font(FONT_FILE, 6) # 40
		self.THEME_VODNIK = pygame_menu.Theme(
			background_color=(0, 0, 0, 0),
			cursor_color=(255, 255, 255),
			cursor_selection_color=(80, 80, 80, 120),
			scrollbar_color=(39, 41, 42),
			scrollbar_slider_color=(65, 66, 67),
			scrollbar_slider_hover_color=(90, 89, 88),
			selection_color=(255, 255, 255),
			title_background_color=(47, 88, 51),
			title_font_color=(215, 215, 215),
			widget_font_color=(0, 20, 0),
			title_font=font,
			widget_font=font,
			widget_font_size=10, # 40
			widget_font_shadow=False, # True
			widget_font_shadow_offset=1,
			title=False,
			widget_font_shadow_color=(80, 120, 80),
			widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(
			# arrow_right_margin=50,
		)
		)
		pygame.display.set_caption(self.PROGRAM_NAME)
		self.screen = pygame.display.set_mode((screen_width,screen_height), pygame.SCALED + pygame.NOFRAME + pygame.FULLSCREEN)
		# self.screen. # background image
		self.clock = pygame.time.Clock()

		self.play_menu = self.create_play_menu()
		self.scoreboard_menu = self.create_scoreboard_menu()
		self.instructions_menu = self.create_instructions_menu()
		self.credits_menu = self.create_credits_menu()
		self.main_menu = self.create_main_menu()
		pygame_menu.widgets.MENUBAR_STYLE_NONE

	def main_background(self) -> None:
		background_image = pygame_menu.BaseImage(
			image_path=MENU_IMAGE_FILE
		)
		background_image.draw(self.screen)
	def run(self):
		self.run_launch_screen()
		if(not self.main_menu_music==""):
			self.main_menu_music.play(loops = -1)
		try:
			display_score_on_led_display(0)
		except:
			print("Could not send curl.")
		self.main_menu.mainloop(self.screen,self.main_background)

	def run_game(self):
		if(not self.main_menu_music==""):
			self.main_menu_music.stop()
		self.game = Game(self.screen,self.create_play_menu,self.scoreboard[9][1])
		global player_name
		self.game.player_name = player_name
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.screen.fill('grey')
			self.game.run()

			pygame.display.update()
			self.clock.tick(30)
			if self.game.status=='end':
				if not self.main_menu_music=="":
					self.main_menu_music.play(loops = -1)
				break
		
		self.handle_highscore()
		
		self.scoreboard_menu.clear()
		try:
			display_score_on_led_display(0)
		except:
			print("Could not send curl.")

		self.scoreboard = self.load_score_board()

		self.scoreboard_menu.add.label(LOCALE_SCOREBOARD)
		table = self.scoreboard_menu.add.table("scoreboard")
		# table.set_border(4,"red")
		table.set_background_color((233,206,146))
		# ALIGN_RIGHT
		self.score1 = table.add_row(['  1.',' {0}'.format(self.scoreboard[0][1]), '    {0}'.format(self.scoreboard[0][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  2.',' {0}'.format(self.scoreboard[1][1]), '    {0}'.format(self.scoreboard[1][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  3.',' {0}'.format(self.scoreboard[2][1]), '    {0}'.format(self.scoreboard[2][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  4.',' {0}'.format(self.scoreboard[3][1]), '    {0}'.format(self.scoreboard[3][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  5.',' {0}'.format(self.scoreboard[4][1]), '    {0}'.format(self.scoreboard[4][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  6.',' {0}'.format(self.scoreboard[5][1]), '    {0}'.format(self.scoreboard[5][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  7.',' {0}'.format(self.scoreboard[6][1]), '    {0}'.format(self.scoreboard[6][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  8.',' {0}'.format(self.scoreboard[7][1]), '    {0}'.format(self.scoreboard[7][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  9.',' {0}'.format(self.scoreboard[8][1]), '    {0}'.format(self.scoreboard[8][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row([' 10.',' {0}'.format(self.scoreboard[9][1]), '    {0}'.format(self.scoreboard[9][0])],None,(233,206,146),None,None,None,"black")
		self.scoreboard_menu.render()
		self.main_menu.full_reset()
		# self.play_menu = self.create_play_menu()
		# self.play_menu.render()
		# self.scoreboard_menu = self.create_scoreboard_menu()
		# self.scoreboard_menu.render()
		# self.credits_menu = self.create_credits_menu()
		# self.credits_menu.render()
		# self.main_menu = self.create_main_menu()
		# self.main_menu.render()
		
	def create_main_menu(self):
		main_menu = pygame_menu.Menu(self.PROGRAM_NAME, screen_width, screen_height,
						theme=self.THEME_VODNIK)
		# main_menu.add.label("Vodník František")
		# main_menu.add.image("../graphics/foreground.png")
		#main_menu.add.menu_link(self.play_menu, 'Play')
		main_menu.add.button(LOCALE_PLAY, self.run_game)
		#main_menu.add.menu_link(self.scoreboard_menu, 'Score Board')
		self.sc_b_button = main_menu.add.button(LOCALE_SCOREBOARD, self.scoreboard_menu)
		#main_menu.add.menu_link(self.instructions_menu, 'Instructions')
		main_menu.add.button(LOCALE_INSTRUCTIONS, self.instructions_menu)
		#main_menu.add.menu_link(self.credits_menu, 'Credits')
		main_menu.add.button(LOCALE_CREDITS, self.credits_menu)
		# main_menu.add.button(LOCALE_QUIT, pygame_menu.events.EXIT)
		return main_menu

	def handle_highscore(self):
		scores = self.load_score_board()
		print("score")
		print(self.game.level.score)
		global player_name
		print(player_name)
		new_score = [player_name,self.game.level.score]
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
		f.write(']}')
	def create_play_menu(self):
		def add_letter_to_name(self,selected_value):
			global player_name
			if len(player_name)<13:
				player_name += selected_value
				name_label.set_title(LOCALE_NAME+": {0}".format(player_name))
				name_label.render()
			
		def delete_character():
			global player_name
			player_name = player_name[:-1]
			name_label.set_title(LOCALE_NAME+": {0}".format(player_name))
			name_label.render()
		
		play_menu = pygame_menu.Menu(LOCALE_CONGRATULATIONS, screen_width, screen_height,
						theme=self.THEME_VODNIK)
		name_label = play_menu.add.label(LOCALE_CONGRATULATIONS)
		name_label = play_menu.add.label(LOCALE_NAME+": {0}".format(player_name))

		self.letter_input = play_menu.add.selector(LOCALE_ADD_CHARACTER + ':', [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z'), ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('_', '_')],onreturn=add_letter_to_name)
		play_menu.add.button(LOCALE_DELETE_CHARACTER, delete_character)
		# play_menu.add.button(LOCALE_PLAY_2, self.run_game)
		play_menu.add.button(LOCALE_SAVE, play_menu.disable)
		# play_menu.add.button('Play', pygame_menu.events.RESET)
		return play_menu

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

	def create_scoreboard_menu(self):
		menu = pygame_menu.Menu(LOCALE_SCOREBOARD, screen_width, screen_height,
						theme=self.THEME_VODNIK)

		menu.add.label(LOCALE_SCOREBOARD)
		table = menu.add.table("scoreboard")
		# table.set_border(4,"red")
		table.set_background_color(((233,206,146)))
		# ALIGN_RIGHT
		self.score1 = table.add_row(['  1.',' {0}'.format(self.scoreboard[0][1]), '    {0}'.format(self.scoreboard[0][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  2.',' {0}'.format(self.scoreboard[1][1]), '    {0}'.format(self.scoreboard[1][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  3.',' {0}'.format(self.scoreboard[2][1]), '    {0}'.format(self.scoreboard[2][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  4.',' {0}'.format(self.scoreboard[3][1]), '    {0}'.format(self.scoreboard[3][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  5.',' {0}'.format(self.scoreboard[4][1]), '    {0}'.format(self.scoreboard[4][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  6.',' {0}'.format(self.scoreboard[5][1]), '    {0}'.format(self.scoreboard[5][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  7.',' {0}'.format(self.scoreboard[6][1]), '    {0}'.format(self.scoreboard[6][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  8.',' {0}'.format(self.scoreboard[7][1]), '    {0}'.format(self.scoreboard[7][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row(['  9.',' {0}'.format(self.scoreboard[8][1]), '    {0}'.format(self.scoreboard[8][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row([' 10.',' {0}'.format(self.scoreboard[9][1]), '    {0}'.format(self.scoreboard[9][0])],None,(233,206,146),None,None,None,"black")
		# self.score2 = table.add.label("2) {0} by {1}".format(self.scoreboard[1][1],self.scoreboard[1][0]))
		# self.score3 = menu.add.label("3) {0} by {1}".format(self.scoreboard[2][1],self.scoreboard[2][0]))
		# self.score4 = menu.add.label("4) {0} by {1}".format(self.scoreboard[3][1],self.scoreboard[3][0]))
		# self.score5 = menu.add.label("5) {0} by {1}".format(self.scoreboard[4][1],self.scoreboard[4][0]))
		return menu

	def create_credits_menu(self):
		menu = pygame_menu.Menu(LOCALE_CREDITS, screen_width, screen_height,
						theme=self.THEME_VODNIK)
		menu.add.label(LOCALE_CREDITS_LABEL_1)
		menu.add.label(LOCALE_CREDITS_LABEL_2)
		menu.add.label("")
		menu.add.label(LOCALE_CREDITS_LABEL_3)
		menu.add.label(LOCALE_CREDITS_LABEL_4)
		return menu

	def create_instructions_menu(self):
		menu = pygame_menu.Menu('Instructions', screen_width, screen_height,
						theme=self.THEME_VODNIK)
		menu.add.label("Joystick - pohyb")
		menu.add.label("žluté tlačítko - uchop")
		menu.add.label("červené tlačítko - polož")
		menu.add.label("Nahoru + žluté - chyť duši")
		menu.add.label("Nahoru + červené - pověs")
		menu.add.label("Recykluj sklo a dostaneš body.")
		menu.add.label("Věš pneumatiky na pruty,")
		menu.add.label("abys chytil pytláky.")
		menu.add.label("S hrníčky z poličky sbírej jejich duše.")
		return menu

	def run_launch_screen(self):
		self.display_pygame_screen()

	def display_pygame_screen(self):
		window = (settings.screen_width,settings.screen_height)
		background = pygame.Surface(window)

		myimage = pygame.image.load(PYGAME_LOGO_FILE)
		picture = pygame.transform.scale(myimage, (round(settings.screen_width/1.5), round(settings.screen_height/1.5)))
		
		x1, y1 = background.get_width()//2, background.get_height()//2
		background.blit(picture, (x1 - picture.get_width() // 2, y1 - picture.get_height() // 2))
		
		x, y = self.screen.get_width()//2, self.screen.get_height()//2
		self.screen.blit(background,(x - background.get_width() // 2, y - background.get_height() // 2))
		pygame.display.flip()
		sleep(1.2)
	
