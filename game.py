import boot.readConfig as init 
from lib import threadClass as tc, displayBuffer as dbuff,astarBBB as astar
import pygame, os,time
import sys, getopt, threading

class Environment:
	ENV_LED, ENV_DESKTOP = range(0,2)

class GameState:
	NOT_STARTED, RUNNING, PAUSED, RESETTED, STOPPED = range(0, 5)
	
#Default Environment
environment = Environment.ENV_LED

#Command Line Arguments
if(len(sys.argv) > 1):
        if(str(sys.argv[1]) == '-h'):
                print "Game running on LED"
                environment = Environment.ENV_LED
		from lib.bootstrap import *

        elif(str(sys.argv[1]) == '-d'):
                print "Game running on DESKTOP"
                environment = Environment.ENV_DESKTOP


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
		self.gameState = GameState.NOT_STARTED

		#change the default direction of ghost
		self.direction_of_ghost1 = "up"	
		self.environment = environment
		self.colorPacMan = (0, 255, 0)
		self.colorGhost = (255, 0, 0)
		self.colorCoins = (255,255,255)
		self.twoJSPresent = False
		self.lock = threading.Lock()
		#Initialize the display buffer
		self.dbuffer = dbuff.Display_Buffer(self.environment, self.data)
		self.aiPath = astar.CFindPath(self.data)	


		pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
		pygame.init()                              #initialize pygame

		#We need to setup the display. Otherwise, pygame events will not work
		screen_size = [500, 500]
		pygame.display.set_mode(screen_size)

		# look for sound & music files in subfolder 'data'
		pygame.mixer.music.load(os.path.join('data', 'an-turr.ogg'))#load music
		self.jump = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
		self.fail = pygame.mixer.Sound(os.path.join('data','fail.wav'))  #load sound

		# play music non-stop
		pygame.mixer.music.play(-1)

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

		keys = self.data.keys()
		for key in keys:
			if(self.data[key]["type"] == "P"):
				self.dbuffer.Set_Pixel(int(key), self.colorPacMan , 1)
				self.posPacMan = int(key)
				self.indexPacMan = str(self.posPacMan)
			elif(self.data[key]["type"] == "G"):
				self.dbuffer.Set_Pixel(int(key), self.colorGhost , 1)
				self.posGhost1 = int(key)
				self.indexGhost1 = str(self.posGhost1)
			elif(self.data[key]["type"] == "AI"):
				self.dbuffer.Set_Pixel(int(key), self.colorAIGhost , 1)
				self.posAIGhost = int(key)
				self.indexAIGhost = str(self.posAIGhost)
			elif(self.data[key]["type"] == "C"):
				self.dbuffer.Set_Pixel(int(key), self.colorCoins , 1)		


	def main(self):		
		prev_posPacman = self.posPacMan
		prev_posGhost1  = self.posGhost1
		quit = False

		clock = pygame.time.Clock()
		
		print "Press Start Button to start playing.."
		
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
				if event.type == pygame.JOYBUTTONDOWN:
					#If the start button is pressed and game is stopped, start the game
					if event.button == 1  and self.gameState == GameState.NOT_STARTED:
						#Load the array of LEDs to be used for first boot for displaying coins
						#It will read all LEDs from JSON file. Depending upon their type, they will have different colors
						app.load_layout()
						

						#Wait for 2 seconds
						time.sleep(2)

						#Flash the Pac Man and Ghost 5 times
						for i in range(0,5):
							self.dbuffer.Set_Pixel(self.indexPacMan, (255, 255, 255), 1)
							self.dbuffer.Set_Pixel(self.indexGhost1, (255, 255, 255), 1)
							self.dbuffer.Set_Pixel(self.posAIGhost, (255, 255, 255), 1) 
							time.sleep(1)
							self.dbuffer.Set_Pixel(self.indexPacMan, self.colorPacMan, 1)
							self.dbuffer.Set_Pixel(self.indexGhost1, self.colorGhost, 1)
							self.dbuffer.Set_Pixel(self.posAIGhost, self.colorAIGhost, 1)
							time.sleep(1)
						
						#Change the game state to RUNNING
						self.gameState = GameState.RUNNING

						#Start the PacMan Sound
						print "Game is running now.."

					#If the pause button is pressed and game is running, pause the game
					if event.button == 2 and self.gameState == GameState.RUNNING:
						#Stop the game sound
			
						#Change the game state to PAUSED
						self.gameState = GameState.PAUSED
					
					#If the start button is pressed and game is running, pause the game
					if event.button == 1 and self.gameState == GameState.PAUSED:
						#Start the game sound
			
						#Change the game state to RUNNING
						self.gameState = GameState.RUNNING

								
					
				#Track the PacMan and Ghost only if the game is RUNNING
				if self.gameState == GameState.RUNNING:
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
							self.direction_of_pacman = "left"

							self.jump.play()
						elif(jy_pos1_horizontal > 0 and int(self.data[self.indexPacMan]["right"]) != -1 ):
							prev_pos = self.posPacMan
							self.direction_of_pacman = "right"

							self.jump.play()
						if(jy_pos1_vertical > 0 and int(self.data[self.indexPacMan]["down"]) != -1):
							prev_pos = self.posPacMan
							self.direction_of_pacman = "down"

							self.jump.play()
						elif(jy_pos1_vertical < 0 and int(self.data[self.indexPacMan]["up"]) != -1):
							prev_pos = self.posPacMan
							self.direction_of_pacman = "up"
							self.jump.play()

							#self.indexPacMan = str(self.posPacMan)


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
				
			#Set Off Ghost's old position
			self.dbuffer.Set_Pixel(prev_posGhost1, (255, 255, 255), 1)
			#Set Ghost's new position
			self.dbuffer.Set_Pixel(self.posGhost1, self.colorGhost, 1)
		
		elif(jy_pos2_horizontal > 0 and int(self.data[self.indexGhost1]["right"]) != -1 ):
			print "right pressed"
			print "self.posGhost1",self.posGhost1					
			prev_posGhost1 = self.posGhost1
			self.posGhost1 = int(self.data[self.indexGhost1]["right"])
			self.direction_of_ghost = "right"
			#Set Ghost's old position
			self.dbuffer.Set_Pixel(prev_posGhost1, (255, 255, 255), 1)
			#Set Ghost's new position
			self.dbuffer.Set_Pixel(self.posGhost1, self.colorGhost, 1)

						
		if(jy_pos2_vertical > 0 and int(self.data[self.indexGhost1]["down"]) != -1):
			print "down pressed"
			print "self.posGhost1",self.posGhost1					
			prev_posGhost1 = self.posGhost1
			self.posGhost1 = int(self.data[self.indexGhost1]["down"])
			self.direction_of_ghost = "down"
			#Set Ghost's old position
			self.dbuffer.Set_Pixel(prev_posGhost1, (255, 255, 255), 1)
			#Set Ghost's new position
			self.dbuffer.Set_Pixel(self.posGhost1, self.colorGhost, 1)

						
		elif(jy_pos2_vertical < 0 and int(self.data[self.indexGhost1]["up"]) != -1):
			print "up pressed"
			print "self.posGhost1",self.posGhost1					
			prev_posGhost1 = self.posGhost1
			self.posGhost1 = int(self.data[self.indexGhost1]["up"])
			self.direction_of_ghost = "up"
			#Set Off Ghost's old position
			self.dbuffer.Set_Pixel(prev_posGhost1, (255, 255, 255), 1)
			#Set Ghost's new position
			self.dbuffer.Set_Pixel(self.posGhost1, self.colorGhost, 1)
	
		#self.indexGhost1 = str(self.posGhost1)



	#This function will be called in another thread which will increment the PACMAN with each clocktick
	def ledRunningFunc(self):
		
		while 1:
			print "LED Running Function"		
			#Do only when game is RUNNING
			if self.gameState == GameState.RUNNING:
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
				#self.aiGhost()		
				self.lock.release()
				
			time.sleep(0.5)

	
	#this function will deal with the Artificial Ghost 
	def aiGhost(self):
		while 1:
			#Do only when game is RUNNING
			if self.gameState == GameState.RUNNING:
				self.lock.acquire()
				
				destination = str(self.posPacMan)
				source = str(self.posAIGhost)
				
				#Calculate only if the source and destination are different
				if not (source == destination):
				
					#This takes only string, so converted to string
					path = self.aiPath.findPath(source, destination)
					#assign index 1 to the nextPosition of ghost as path[0] is the source iteself
					nextPosGhost = path[1]
				
					#Set Off ghost's old position
					self.dbuffer.Set_Pixel(self.posAIGhost, (255, 255, 255), 1)
				
					#Set ghost's new position
					self.posAIGhost = int(nextPosGhost)
					self.dbuffer.Set_Pixel(self.posAIGhost, self.colorAIGhost, 1)
				
				#release a lock here
				self.lock.release()
				
			#This delay should be similar to ledRunning function so as to keep the speed constant
			time.sleep(0.5)

if __name__ == '__main__':
	app = CGame(environment)
	
	#Create threads
	refreshWin = threading.Thread(target = app.ledRunningFunc, args = [])
	threadMain = threading.Thread(target = app.main, args = [])
	threadAIGhost = threading.Thread(target=app.aiGhost , args=[])
	
	#Start threads
	threadMain.start()
	threadAIGhost.start()
	refreshWin.start()
	
	if(app.environment == Environment.ENV_DESKTOP):
		app.dbuffer.Start_Flushing()
	else:
		threadMain.join()
		threadAIGhost.join()
		refreshWin.join()
		
