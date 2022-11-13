from multiprocessing.connection import wait
from time import sleep
import settings

# if pygame and pygame_menu not installed:
import sys
import subprocess
import pkg_resources

required = {'pygame', 'pygame_menu'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
	# install via pip
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
	# if pip is not installed
		# view commands to install pygame and pygame_menu libs

import pygame, sys
import pygame_menu.controls as ctrl
from game import Game

ctrl.KEY_APPLY = pygame.K_k
ctrl.KEY_BACK = pygame.K_l
ctrl.KEY_CLOSE_MENU = pygame.K_ESCAPE
ctrl.KEY_LEFT = pygame.K_a
ctrl.KEY_MOVE_DOWN = pygame.K_w
ctrl.KEY_MOVE_UP = pygame.K_s  # Consider keys are "inverted"
ctrl.KEY_RIGHT = pygame.K_d
ctrl.KEY_TAB = pygame.K_TAB
import pygame_menu
# from lib.pygame_menu.pygame_menu import pygame_menu

LOCALE_PLAY = "HRÁT"
LOCALE_SCOREBOARD = "TABULKA VÍTĚZŮ"
LOCALE_INSTRUCTIONS = "INSTRUKCE"
LOCALE_CREDITS = "O HŘE"
LOCALE_QUIT = "KONEC"

def load_player_name():
	with open('../playername.txt', 'r') as f:
		return f.readline()

screen_width = settings.screen_width
screen_height = settings.screen_height
player_name = load_player_name()

class Program:
	# font = pygame_menu.font.FONT_NEVIS
	PROGRAM_NAME = "Vodník František"

	def __init__(self):
		# Pygame setup
		pygame.init()
		self.main_menu_music = pygame.mixer.Sound('../audio/vodevil-15550.mp3')
		font = pygame.font.Font('../kyrou_7_wide_bold.ttf', 6) # 40
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
			image_path="../graphics/menu.png"
		)
		background_image.draw(self.screen)
	def run(self):
		self.run_launch_screen()
		self.main_menu_music.play(loops = -1)
		self.main_menu.mainloop(self.screen,self.main_background)

	def run_game(self):
		self.main_menu_music.stop()
		self.game = Game(self.screen)
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
				self.main_menu_music.play(loops = -1)
				break
		
		self.scoreboard_menu.clear()

		scoreboard = self.load_score_board()

		self.scoreboard_menu.add.label("SCORE BOARD")
		table = self.scoreboard_menu.add.table("scoreboard")
		# table.set_border(4,"red")
		table.set_background_color((233,206,146))
		# ALIGN_RIGHT
		self.score1 = table.add_row([' 1.',' {0}'.format(scoreboard[0][1][:-1]), '    {0}'.format(scoreboard[0][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row([' 2.',' {0}'.format(scoreboard[1][1][:-1]), '    {0}'.format(scoreboard[1][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row([' 3.',' {0}'.format(scoreboard[2][1][:-1]), '    {0}'.format(scoreboard[2][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row([' 4.',' {0}'.format(scoreboard[3][1][:-1]), '    {0}'.format(scoreboard[3][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row([' 5.',' {0}'.format(scoreboard[4][1][:-1]), '    {0}'.format(scoreboard[4][0])],None,(233,206,146),None,None,None,"black")
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
		main_menu.add.button(LOCALE_PLAY, self.play_menu)
		#main_menu.add.menu_link(self.scoreboard_menu, 'Score Board')
		self.sc_b_button = main_menu.add.button(LOCALE_SCOREBOARD, self.scoreboard_menu)
		#main_menu.add.menu_link(self.instructions_menu, 'Instructions')
		main_menu.add.button(LOCALE_INSTRUCTIONS, self.instructions_menu)
		#main_menu.add.menu_link(self.credits_menu, 'Credits')
		main_menu.add.button(LOCALE_CREDITS, self.credits_menu)
		main_menu.add.button(LOCALE_QUIT, pygame_menu.events.EXIT)
		return main_menu

	def create_play_menu(self):
		def add_letter_to_name(self,selected_value):
			global player_name
			if len(player_name)<13:
				player_name += selected_value
				name_label.set_title("Jméno: {0}".format(player_name))
				name_label.render()
			
		def delete_character():
			global player_name
			player_name = player_name[:-1]
			name_label.set_title("Jméno: {0}".format(player_name))
			name_label.render()
		
		play_menu = pygame_menu.Menu('Play', screen_width, screen_height,
						theme=self.THEME_VODNIK)
		name_label = play_menu.add.label("Jméno: {0}".format(player_name))

		self.letter_input = play_menu.add.selector('Přidat písmeno :', [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z'), ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('_', '_')],onreturn=add_letter_to_name)
		play_menu.add.button('Umazat písmeno', delete_character)
		play_menu.add.button('Hrát', self.run_game)
		# play_menu.add.button('Play', pygame_menu.events.RESET)
		return play_menu

	def load_score_board(self):
		with open('../highscores.txt', 'r') as f:
			option = f.readline().split(" = ")
			player_1 = [option[0], option[1]]
			option = f.readline().split(" = ")
			player_2 = [option[0], option[1]]
			option = f.readline().split(" = ")
			player_3 = [option[0], option[1]]
			option = f.readline().split(" = ")
			player_4 = [option[0], option[1]]
			option = f.readline().split(" = ")
			player_5 = [option[0], option[1]]
		return [player_1,player_2,player_3,player_4,player_5]

	def create_scoreboard_menu(self):
		menu = pygame_menu.Menu(LOCALE_SCOREBOARD, screen_width, screen_height,
						theme=self.THEME_VODNIK)
		scoreboard = self.load_score_board()

		menu.add.label(LOCALE_SCOREBOARD)
		table = menu.add.table("scoreboard")
		# table.set_border(4,"red")
		table.set_background_color(((233,206,146)))
		# ALIGN_RIGHT
		self.score1 = table.add_row([' 1.',' {0}'.format(scoreboard[0][1][:-1]), '    {0}'.format(scoreboard[0][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row([' 2.',' {0}'.format(scoreboard[1][1][:-1]), '    {0}'.format(scoreboard[1][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row([' 3.',' {0}'.format(scoreboard[2][1][:-1]), '    {0}'.format(scoreboard[2][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row([' 4.',' {0}'.format(scoreboard[3][1][:-1]), '    {0}'.format(scoreboard[3][0])],None,(233,206,146),None,None,None,"black")
		self.score1 = table.add_row([' 5.',' {0}'.format(scoreboard[4][1][:-1]), '    {0}'.format(scoreboard[4][0])],None,(233,206,146),None,None,None,"black")
		# self.score2 = table.add.label("2) {0} by {1}".format(scoreboard[1][1],scoreboard[1][0]))
		# self.score3 = menu.add.label("3) {0} by {1}".format(scoreboard[2][1],scoreboard[2][0]))
		# self.score4 = menu.add.label("4) {0} by {1}".format(scoreboard[3][1],scoreboard[3][0]))
		# self.score5 = menu.add.label("5) {0} by {1}".format(scoreboard[4][1],scoreboard[4][0]))
		return menu

	def create_credits_menu(self):
		menu = pygame_menu.Menu(LOCALE_CREDITS, screen_width, screen_height,
						theme=self.THEME_VODNIK)
		menu.add.label("Programming: Samuel Machat")
		menu.add.label("Grafika: Lenka Holubcová")
		menu.add.label("")
		menu.add.label("S láskou k Hogo Frogo")
		menu.add.label("pro FIK Mat")
		return menu

	def create_instructions_menu(self):
		menu = pygame_menu.Menu('Instructions', screen_width, screen_height,
						theme=self.THEME_VODNIK)
		menu.add.label("Joystick - pohyb")
		menu.add.label("A - uchop")
		menu.add.label("B - polož")
		menu.add.label("Nahoru + A - chyť duši")
		menu.add.label("Nahoru + B - pověs")
		menu.add.label("Recykluj sklo a dostaneš body.")
		menu.add.label("Věš pneumatiky na pruty,")
		menu.add.label("abys chytil pytláky.")
		menu.add.label("S hrníčky z poličky sbírej jejich duše.")
		return menu

	def run_launch_screen(self):

		# window = (settings.screen_width,settings.screen_height)
		# background = pygame.Surface(window)

		# myimage = pygame.image.load('../graphics/hogo_frogo_teamo_logo.png')
		# picture = pygame.transform.scale(myimage, (settings.screen_width/2, settings.screen_height/2))
		
		# x1, y1 = background.get_width()//2, background.get_height()//2
		# background.blit(picture, (x1 - picture.get_width() // 2, y1 - picture.get_height() // 2))
		
		# x, y = self.screen.get_width()//2, self.screen.get_height()//2
		# self.screen.blit(background,(x - background.get_width() // 2, y - background.get_height() // 2))
		# pygame.display.flip()
		# sleep(1)


		window = (settings.screen_width,settings.screen_height)
		background = pygame.Surface(window)

		myimage = pygame.image.load('../graphics/pygame_logo.png')
		picture = pygame.transform.scale(myimage, (round(settings.screen_width/1.5), round(settings.screen_height/1.5)))
		
		x1, y1 = background.get_width()//2, background.get_height()//2
		background.blit(picture, (x1 - picture.get_width() // 2, y1 - picture.get_height() // 2))
		
		x, y = self.screen.get_width()//2, self.screen.get_height()//2
		self.screen.blit(background,(x - background.get_width() // 2, y - background.get_height() // 2))
		pygame.display.flip()
		sleep(1.2)
