from lib.bootstrap import *
import boot.readConfig as init 
import pygame
import os
import time, threadClass as tc
import Display_Buffer as dbuff
import sys, getopt

ENV_LED = 0
ENV_DESKTOP = 1

class CGame:
	def __init__(self, environment):

		self.Joystick = None
		self.jump = None
		self.fail = None
		self.led = None
		self.joystick_names = []
		self.direction_of_pacman = None
		self.data  = init.config()
		self.posPacMan = 1
		self.posGhost = 1
		self.index = str(self.posPacMan)
		self.direction_of_pacman = "up"	
		self.environment = environment
		self.colorPacMan = (0, 255, 0)
		self.colorGhost = (255, 0, 0)
		self.colorCoins = (255,255,255)

		#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
		pygame.init()                              #initialize pygame

		# look for sound & music files in subfolder 'data'
		#pygame.mixer.music.load(os.path.join('data', 'an-turr.ogg'))#load music
		#self.jump = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
		#self.fail = pygame.mixer.Sound(os.path.join('data','fail.wav'))  #load sound

		# play music non-stop
		#pygame.mixer.music.play(-1)

		#Initialize the Joysticks
		pygame.joystick.init()


		#Get count of joysticks
		joystick_count = pygame.joystick.get_count()

		#We need to setup the display. Otherwise, pygame events will not work
		screen_size = [500, 500]
		pygame.display.set_mode(screen_size)


		#Initialize joysticks
		for i in range(joystick_count):
		    #We need to initialize the individual joystick instances to receive the events
		    pygame.joystick.Joystick(i).init()


		#Capturing Joystick Events
		print("Press buttons on the Joystick and see if they are captured by this program")

		#Get the first joystick
		self.Joystick = pygame.joystick.Joystick(0)


		#Initialize the display buffer
		self.dbuffer = dbuff.Display_Buffer(self.environment)

		#Get the Mapping of LED -to - Pixels
		self.Pixels_info = init.read_pixel_info()


	def load_layout(self):

		keys = self.Pixels_info.keys()
		for key in keys:
			if(self.Pixels_info[key]["type"] == "P"):
				self.dbuffer.Set_Pixel(int(key), self.colorPacMan , 1)
				self.posPacMan = int(key)
			elif(self.Pixels_info[key]["type"] == "G"):
				self.dbuffer.Set_Pixel(int(key), self.colorGhost , 1)
				self.posGhost = int(key)
			elif(self.Pixels_info[key]["type"] == "C"):
				self.dbuffer.Set_Pixel(int(key), self.colorCoins , 1)		


	def main(self):
		#Load the array of LEDs to be used for first boot for displaying coins
		#To implement, right now initializing everything
		#It will read all LEDs from JSON file. Depending upon their type, they will have different colors
		self.load_layout()		
                
	
		self.index = str(self.posPacMan)
		self.direction_of_pacman = "up"	
		self.nextIndexPacman = "2"
		
		prev_pos = self.posPacMan
		
		quit = False

		clock = pygame.time.Clock()

		while (quit != True):
		    	'''
			if pygame.mixer.music.get_busy():
		        	print " music is playing"
		    	else:
		        	print " music is not playing"
			'''
			time.sleep(0.005)			

		        for event in pygame.event.get():
			    	if event.type == pygame.QUIT:
			        	quit = True
			    	if event.type == pygame.JOYAXISMOTION:
			        	print("Axis Moved...")
			        	#Joystick position
				        jy_pos_horizontal = self.Joystick.get_axis(0)
					jy_pos_vertical = self.Joystick.get_axis(1)

			       		if(jy_pos_horizontal < 0 and int(self.data[self.index]["left"]) != -1 ):
						prev_pos = self.posPacMan
				        	self.posPacMan = int(self.data[self.index]["left"])
						self.direction_of_pacman = "left"
						
						#Set Off Pac-man's old position
						self.dbuffer.Set_Pixel(prev_pos, self.colorPacMan, 0)

						#Set Pac-man's new position
						self.dbuffer.Set_Pixel(self.posPacMan, self.colorPacMan, 1)

						#self.jump.play()
				        elif(jy_pos_horizontal > 0 and int(self.data[self.index]["right"]) != -1 ):
						prev_pos = self.posPacMan
						self.posPacMan = int(self.data[self.index]["right"])
						self.direction_of_pacman = "right"

						#Set Off Pac-man's old position
						self.dbuffer.Set_Pixel(prev_pos, self.colorPacMan, 0)

						#Set Pac-man's new position
						self.dbuffer.Set_Pixel(self.posPacMan, self.colorPacMan, 1)

						#self.jump.play()
					if(jy_pos_vertical > 0 and int(self.data[self.index]["down"]) != -1):
						prev_pos = self.posPacMan
						self.posPacMan = int(self.data[self.index]["down"])
						self.direction_of_pacman = "down"

						#Set Off Pac-man's old position
						self.dbuffer.Set_Pixel(prev_pos, self.colorPacMan, 0)

						#Set Pac-man's new position
						self.dbuffer.Set_Pixel(self.posPacMan, self.colorPacMan, 1)

						#self.jump.play()
					elif(jy_pos_vertical < 0 and int(self.data[self.index]["up"]) != -1):
						prev_pos = self.posPacMan
						self.posPacMan = int(self.data[self.index]["up"])
						self.direction_of_pacman = "up"

						#Set Off Pac-man's old position
						self.dbuffer.Set_Pixel(prev_pos, self.colorPacMan, 0)

						#Set Pac-man's new position
						self.dbuffer.Set_Pixel(self.posPacMan, self.colorPacMan, 1)

						#self.jump.play()

			self.index = str(self.posPacMan)


			'''
			To stop the music :D :D 
			if pygame.mixer.music.get_busy():
		            pygame.mixer.music.stop()
		        else:
		            pygame.mixer.music.play()
			'''


		pygame.quit()

	#This function will be called in another thread which will increment the PACMAN with each clocktick
	def ledRunningFunc(self):
		
		print "direction",self.direction_of_pacman
		print "self.posPacMan", self.posPacMan
		while 1:
			#print "prev_pos,posPacMan",prev_pos, self.posPacMan
			#put a lock here
			prev_pos = self.posPacMan
			if (int(self.data[self.index][self.direction_of_pacman]) != -1):
				self.posPacMan = int(self.data[self.index][self.direction_of_pacman])
				self.index = str(self.posPacMan)
				
				print "prev_pos,posPacMan",prev_pos, self.posPacMan
				
				#Set Off Pac-man's old position
				self.dbuffer.Set_Pixel(prev_pos, self.colorPacMan, 0)

				#Set Pac-man's new position
				self.dbuffer.Set_Pixel(self.posPacMan, self.colorPacMan, 1)

			#release here
			time.sleep(1)


#Default Environment
environment = ENV_LED

#Command Line Arguments
if(len(sys.argv) > 1):
	if(str(sys.argv[1]) == '-h'):
		print "Game running on LED"
		environment = ENV_LED
	elif(str(sys.argv[1]) == '-d'):
		print "Game running on DESKTOP"
		environment = ENV_DESKTOP

app = CGame(environment)


refreshWin = tc.FuncThread(app.ledRunningFunc)
if(app.environment == ENV_DESKTOP):
	refreshDesktop = tc.FuncThread(app.dbuffer.Start_Flushing)
threadMain = tc.FuncThread(app.main)

#Start threads
refreshWin.start()
if(app.environment == ENV_DESKTOP):
	refreshDesktop.start()
threadMain.start()

#Join
threadMain.join()
if(app.environment == ENV_DESKTOP):
	refreshDesktop.join()
refreshWin.join()
#app.main()
#app.ledRunningFunc()
