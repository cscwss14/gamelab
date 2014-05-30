#from lib.bootstrap import *
import boot.readConfig as init 
import pygame
import os, threading
import time, threadClass as tc
import displayBuffer as dbuff
import sys, getopt, threading
import astarBBB as astar

ENV_LED = 0
ENV_DESKTOP = 1

#Default Environment
environment = ENV_LED

#Command Line Arguments
if(len(sys.argv) > 1):
        if(str(sys.argv[1]) == '-h'):
                print "Game running on LED"
                environment = ENV_LED
		from lib.bootstrap import *

        elif(str(sys.argv[1]) == '-d'):
                print "Game running on DESKTOP"
                environment = ENV_DESKTOP


class CGame:
	def __init__(self, environment):

		self.Joystick1 = None
		self.Joystick2 = None
		self.joystickCount = 1
		self.jump = None
		self.fail = None
		self.led = None
		self.joystick_names = []
		self.direction_of_pacman = None
		self.data  = init.config()
		self.posPacMan = 1
		self.posGhost1 = 1
		self.indexPacMan = str(self.posPacMan)
		self.indexGhost1 = str(self.posGhost1)
		self.direction_of_pacman = "up"	
		self.direction_of_ghost = "down"	
		self.posAIGhost = "72"
		self.direction_of_AIGhost = "up"
		self.colorAIGhost = (0,0,255)

		#change the default direction of ghost
		self.direction_of_ghost1 = "up"	
		self.environment = environment
		self.colorPacMan = (0, 255, 0)
		self.colorGhost = (255, 0, 0)
		self.colorCoins = (255,255,255)
		self.twoJSPresent = False
		self.lock = threading.Lock()
		#Initialize the display buffer
		self.dbuffer = dbuff.Display_Buffer(self.environment)
		self.aiPath = astar.CFindPath(self.data)	

		#Get the Mapping of LED -to - Pixels
		self.Pixels_info = init.read_pixel_info()

		#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
		pygame.init()                              #initialize pygame

		#We need to setup the display. Otherwise, pygame events will not work
		screen_size = [500, 500]
		pygame.display.set_mode(screen_size)

		# look for sound & music files in subfolder 'data'
		#pygame.mixer.music.load(os.path.join('data', 'an-turr.ogg'))#load music
		#self.jump = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
		#self.fail = pygame.mixer.Sound(os.path.join('data','fail.wav'))  #load sound

		# play music non-stop
		#pygame.mixer.music.play(-1)

		#Initialize the Joysticks
		pygame.joystick.init()

		#Get count of joysticks
		self.joystickCount = pygame.joystick.get_count()

		#Initialize joysticks
		for i in range(self.joystickCount):
		    #We need to initialize the individual joystick instances to receive the events
		    pygame.joystick.Joystick(i).init()


		#Capturing Joystick Events
		print("Press buttons on the Joystick and see if they are captured by this program")

		#Get the first joystick
		self.Joystick1 = pygame.joystick.Joystick(0)
	
		if self.joystickCount > 1:
			self.Joystick2 = pygame.joystick.Joystick(1)
			self.twoJSPresent = True


	def load_layout(self):

		keys = self.Pixels_info.keys()
		for key in keys:
			if(self.Pixels_info[key]["type"] == "P"):
				self.dbuffer.Set_Pixel(int(key), self.colorPacMan , 1)
				self.posPacMan = int(key)
				self.indexPacMan = str(self.posPacMan)
			elif(self.Pixels_info[key]["type"] == "G"):
				self.dbuffer.Set_Pixel(int(key), self.colorGhost , 1)
				self.posGhost1 = int(key)
				self.indexGhost1 = str(self.posGhost1)
			elif(self.Pixels_info[key]["type"] == "AI"):
				self.dbuffer.Set_Pixel(int(key), self.colorAIGhost , 1)
				self.posAIGhost = int(key)
				self.indexAIGhost = str(self.posGhost)
			elif(self.Pixels_info[key]["type"] == "C"):
				self.dbuffer.Set_Pixel(int(key), self.colorCoins , 1)		


	def main(self):		
		prev_posPacman = self.posPacMan
		prev_posGhost1  = self.posGhost1
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
			        	#Joystick1 position
				        jy_pos1_horizontal = self.Joystick1.get_axis(0)
					jy_pos1_vertical = self.Joystick1.get_axis(1)
					
					if (self.twoJSPresent == True):
			        		#Joystick2 position
				        	jy_pos2_horizontal = self.Joystick2.get_axis(0)
						jy_pos2_vertical = self.Joystick2.get_axis(1)
					
						self.handleJoystickTwo(jy_pos2_horizontal,jy_pos2_vertical)		 



					if(jy_pos1_horizontal < 0 and int(self.data[self.indexPacMan]["left"]) != -1 ):
						prev_pos = self.posPacMan
				        	self.posPacMan = int(self.data[self.indexPacMan]["left"])
						self.direction_of_pacman = "left"
						
						#Set Off Pac-man's old position
						self.dbuffer.Set_Pixel(prev_pos, (255, 255, 255), 1)

						#Set Pac-man's new position
						self.dbuffer.Set_Pixel(self.posPacMan, self.colorPacMan, 1)

						#self.jump.play()
				        elif(jy_pos1_horizontal > 0 and int(self.data[self.indexPacMan]["right"]) != -1 ):
						prev_pos = self.posPacMan
						self.posPacMan = int(self.data[self.indexPacMan]["right"])
						self.direction_of_pacman = "right"

						#Set Off Pac-man's old position
						self.dbuffer.Set_Pixel(prev_pos, (255, 255, 255), 1)

						#Set Pac-man's new position
						self.dbuffer.Set_Pixel(self.posPacMan, self.colorPacMan, 1)

						#self.jump.play()
					if(jy_pos1_vertical > 0 and int(self.data[self.indexPacMan]["down"]) != -1):
						prev_pos = self.posPacMan
						self.posPacMan = int(self.data[self.indexPacMan]["down"])
						self.direction_of_pacman = "down"

						#Set Off Pac-man's old position
						self.dbuffer.Set_Pixel(prev_pos, (255, 255, 255), 1)

						#Set Pac-man's new position
						self.dbuffer.Set_Pixel(self.posPacMan, self.colorPacMan, 1)

						#self.jump.play()
					elif(jy_pos1_vertical < 0 and int(self.data[self.indexPacMan]["up"]) != -1):
						prev_pos = self.posPacMan
						self.posPacMan = int(self.data[self.indexPacMan]["up"])
						self.direction_of_pacman = "up"

						#Set Off Pac-man's old position
						self.dbuffer.Set_Pixel(prev_pos, (255, 255, 255), 1)

						#Set Pac-man's new position
						self.dbuffer.Set_Pixel(self.posPacMan, self.colorPacMan, 1)

						#self.jump.play()

			self.indexPacMan = str(self.posPacMan)


			'''
			To stop the music :D :D 
			if pygame.mixer.music.get_busy():
		            pygame.mixer.music.stop()
		        else:
		            pygame.mixer.music.play()
			'''


		pygame.quit()



	def handleJoystickTwo(self,jy_pos2_horizontal,jy_pos2_vertical):					
			 
  		if(jy_pos2_horizontal < 0 and int(self.data[self.indexGhost1]["left"]) != -1 ):
			print "left pressed"
			print "self.posGhost1",self.posGhost1					
			prev_posGhost1 = self.posGhost1
	       		self.posGhost1 = int(self.data[self.indexGhost1]["left"])
			
			self.direction_of_ghost = "left"
				
			#Set Off Pac-man's old position
			self.dbuffer.Set_Pixel(prev_posGhost1, (255, 255, 255), 1)
			#Set Pac-man's new position
			self.dbuffer.Set_Pixel(self.posGhost1, self.colorGhost, 1)

	       	elif(jy_pos2_horizontal > 0 and int(self.data[self.indexGhost1]["right"]) != -1 ):
			print "right pressed"
			print "self.posGhost1",self.posGhost1					
			prev_posGhost1 = self.posGhost1
			self.posGhost1 = int(self.data[self.indexGhost1]["right"])
			self.direction_of_ghost = "right"
			#Set Off Pac-man's old position
			self.dbuffer.Set_Pixel(prev_posGhost1, (255, 255, 255), 1)
			#Set Pac-man's new position
			self.dbuffer.Set_Pixel(self.posGhost1, self.colorGhost, 1)

						
		if(jy_pos2_vertical > 0 and int(self.data[self.indexGhost1]["down"]) != -1):
			print "down pressed"
			print "self.posGhost1",self.posGhost1					
			prev_posGhost1 = self.posGhost1
			self.posGhost1 = int(self.data[self.indexGhost1]["down"])
			self.direction_of_ghost = "down"
			#Set Off Pac-man's old position
			self.dbuffer.Set_Pixel(prev_posGhost1, (255, 255, 255), 1)
			#Set Pac-man's new position
			self.dbuffer.Set_Pixel(self.posGhost1, self.colorGhost, 1)

						
		elif(jy_pos2_vertical < 0 and int(self.data[self.indexGhost1]["up"]) != -1):
			print "up pressed"
			print "self.posGhost1",self.posGhost1					
			prev_posGhost1 = self.posGhost1
			self.posGhost1 = int(self.data[self.indexGhost1]["up"])
			self.direction_of_ghost = "up"
			#Set Off Pac-man's old position
			self.dbuffer.Set_Pixel(prev_posGhost1, (255, 255, 255), 1)
	
			#Set Pac-man's new position
	
			self.dbuffer.Set_Pixel(self.posGhost1, self.colorGhost, 1)
	
		self.indexGhost1 = str(self.posGhost1)
		time.sleep(0.01)

	




	#This function will be called in another thread which will increment the PACMAN with each clocktick
	def ledRunningFunc(self):
		
		while 1:
			#print "prev_pos,posPacMan",prev_pos, self.posPacMan
			self.lock.acquire()
			prev_pos = self.posPacMan
			if (int(self.data[self.indexPacMan][self.direction_of_pacman]) != -1):
				self.posPacMan = int(self.data[self.indexPacMan][self.direction_of_pacman])
				self.indexPacMan = str(self.posPacMan)
				
				
				#Set Off Pac-man's old position
				self.dbuffer.Set_Pixel(prev_pos, (255, 255, 255), 1)

				#Set Pac-man's new position
				self.dbuffer.Set_Pixel(self.posPacMan, self.colorPacMan, 1)
			
			if (self.twoJSPresent == True):
				prev_pos = self.posGhost1
				if (int(self.data[self.indexGhost1][self.direction_of_ghost]) != -1):
					self.posGhost1 = int(self.data[self.indexGhost1][self.direction_of_ghost])
					self.indexGhost1 = str(self.posGhost1)
				
				
					#Set Off Ghost's old position
					self.dbuffer.Set_Pixel(prev_pos, (255, 255, 255), 1)

					#Set Ghost's new position
					self.dbuffer.Set_Pixel(self.posGhost1, self.colorGhost, 1)
			self.aiGhost()		
			self.lock.release()
			time.sleep(0.5)

	#this function will deal with the Artificial Ghost 
	def aiGhost(self):
		#put a lock here
		#while 1:
			
			#self.lock.acquire()
			index = 0 
			destination = str(self.posPacMan)
			source = str(self.posAIGhost)
			#This takes only string, so converted to string
			path = self.aiPath.findPath(source, destination)
			print "path",path
			nextPosGhost = path[index+1]
			print "nexPosGhost",nextPosGhost,self.posAIGhost	
			#Set Off ghost's old position
			self.dbuffer.Set_Pixel(self.posAIGhost, (255, 255, 255), 1)
			
			#Set ghost's new position
			self.posAIGhost = int(nextPosGhost)
			self.dbuffer.Set_Pixel(self.posAIGhost, self.colorAIGhost, 1)
			
			nextPosGhost = path[index+2]
			print "nexPosGhost2",nextPosGhost,self.posAIGhost	
					
			#Set Off ghost's old position
			self.dbuffer.Set_Pixel(self.posAIGhost, (255, 255, 255), 1)
			#Set ghost's new position
			self.posAIGhost = int(nextPosGhost)
			#this takes on integer , so typecasted it
			self.dbuffer.Set_Pixel(self.posAIGhost, self.colorAIGhost, 1)
			
			#release a lock here
			#self.lock.release()
			#time.sleep(0.5)



if __name__ == '__main__':
	app = CGame(environment)
	#Load the array of LEDs to be used for first boot for displaying coins
	#To implement, right now initializing everything
	#It will read all LEDs from JSON file. Depending upon their type, they will have different colors
	app.load_layout()

	print "Pacman position"+str(app.posPacMan)
	#app.main()
	refreshWin = threading.Thread(target=app.ledRunningFunc, args=[])
	if(app.environment == ENV_DESKTOP):
		refreshDesktop = threading.Thread(target=app.dbuffer.Start_Flushing, args=[])
	threadMain = threading.Thread(target=app.main, args=[])
	threadAIGhost = threading.Thread(target=app.aiGhost, args=[])
	'''
	refreshWin = tc.FuncThread(app.ledRunningFunc)
	if(app.environment == ENV_DESKTOP):
		refreshDesktop = tc.FuncThread(app.dbuffer.Start_Flushing)
	threadMain = tc.FuncThread(app.main)
	#threadAIGhost = tc.FuncThread(app.aiGhost)
	'''
	#Start threads
	threadMain.start()
	refreshWin.start()
	threadAIGhost.start()
	if(app.environment == ENV_DESKTOP):
		refreshDesktop.start()
	#Join
	#if(app.environment == ENV_DESKTOP):
	#	refreshDesktop.join()
	#refreshWin.join()
	#threadMain.join()
	#threadAIGhost.join()
