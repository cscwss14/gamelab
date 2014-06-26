import boot.readConfig as init 
from lib import threadClass as tc, displayBuffer as dbuff,pathFinding as pf
import pygame, os,time
import sys, getopt, threading

class Environment:
	ENV_LED, ENV_DESKTOP = range(0,2)

class GameState:
	RUNNING, PAUSED, RESETTED, STOPPED = range(0, 4)
	
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

		self.pacManJoystick = None
		self.ghostJoystick = None
		self.joystickCount = 1
		self.jump = None
		self.fail = None
		self.led = None
		self.joystick_names = []
		self.direction_of_pacman = None
		self.data  = init.config()
		
		#initial positions	
		self.posPacMan = 1
		self.posGhost = 1
		self.posAIGhost1 = "72"
		self.posAIGhost2 = "80"
		self.indexPacMan = str(self.posPacMan)
		self.indexGhost = str(self.posGhost)
		
		#initial direction
		self.direction_of_pacman = "up"	
		self.direction_of_ghost = "down"	
		
		#initial colors
		self.colorAIGhost1 = (0,0,255)
		self.colorAIGhost2 = (0,0,255)
		self.colorPacMan = (255, 255, 0)
		self.colorGhost = (255, 0, 0)
		self.colorCoins = (255,255,255)
		self.colorCollectedCoins = (12,223,223)
		
		#Initial State of the game
		self.gameState = GameState.STOPPED

	
		self.environment = environment
		self.secondPlayerActive= False
		
		#Intensities
		
		self.intensityPacMan = 1.0
		self.intensityGhost = 1.0
		self.intensityAIGhost = 1.0
		self.intensityCoins = 0.2
		self.intensityCollectedCoins = 0.3
		self.twoJSPresent = False
		self.lock = threading.Lock()
		
		#Initialize the display buffer
		self.dbuffer = dbuff.Display_Buffer(self.environment, self.data)
		self.aiPath = pf.CFindPath(self.data)	
	
		#call this function again to reset this dictionary
		self.scoreDict = self.aiPath.getNewScoreDict()
		

		pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
		pygame.init()                              #initialize pygame

		#We need to setup the display. Otherwise, pygame events will not work
		screen_size = [800, 800]
		pygame.display.set_mode(screen_size)
               

		# look for sound & music files in subfolder 'data'
		self.chomp = pygame.mixer.Sound(os.path.join('data','pacman_chomp.wav'))  #load sound
		               

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


		if self.joystickCount > 1:
			#self.Joystick2 = pygame.joystick.Joystick(1)
			self.twoJSPresent = True

	
	#this function loads the game layout
	def load_layout(self):

		keys = self.data.keys()
		for key in keys:
			if(self.data[key]["type"] == "P"):
				self.dbuffer.setPixel(int(key), self.colorPacMan , 1, self.intensityPacMan)
				self.posPacMan = int(key)
				self.indexPacMan = str(self.posPacMan)
			elif(self.data[key]["type"] == "G"):
				#if second joystick is active treat this as a coin, dont confuse with, if 2nd joystick present
				#it should be active, raj will set the variable,self.secondPlayerActive
				if  self.secondPlayerActive == True:
				    self.dbuffer.setPixel(int(key), self.colorGhost , 1, self.intensityGhost)
				    self.posGhost = int(key)
				    self.indexGhost = str(self.posGhost)
				else:
				    self.dbuffer.setPixel(int(key), self.colorCoins , 1, self.intensityCoins)
					
			elif(self.data[key]["type"] == "AI1"):
				self.dbuffer.setPixel(int(key), self.colorAIGhost1 , 1, self.intensityAIGhost)
				self.posAIGhost1 = int(key)
				self.indexAIGhost = str(self.posAIGhost1)
			elif(self.data[key]["type"] == "AI2"):
				#if second joystick is inactive use this
				if  self.secondPlayerActive == False:
				    self.dbuffer.setPixel(int(key), self.colorAIGhost2 , 1, self.intensityAIGhost)
				    self.posAIGhost2 = int(key)
				    self.indexAIGhost = str(self.posAIGhost2)
				else:
				    self.dbuffer.setPixel(int(key), self.colorCoins , 1, self.intensityCoins)
			elif(self.data[key]["type"] == "C"):
				self.dbuffer.setPixel(int(key), self.colorCoins , 1, self.intensityCoins)		

	#this function resets the variables
	def reset_game(self):
		#Reset all the variables
		self.posPacMan = 1
		self.posGhost = 1
		self.posAIGhost1 = "72"
		self.posAIGhost2 = "80"
                self.indexPacMan = str(self.posPacMan)
                self.indexGhost = str(self.posGhost)
	
                self.direction_of_pacman = "up" 
                self.direction_of_ghost = "down"
   
	#main game loop
	def main(self):		
		prev_posPacman = self.posPacMan
		prev_posGhost  = self.posGhost
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
					if self.gameState == GameState.STOPPED:
						if event.button == 1:
							print "First Player started the game"
							#Start the PacMan Sound
							pygame.mixer.music.load(os.path.join('data', 'pacman_beginning.wav'))
							pygame.mixer.music.play(-1)

							
							#Set the joystick instance of PacMan
							self.pacManJoystick = pygame.joystick.Joystick(event.joy)

							#if second joystick is present, then wait for the second player (ghost) to start the game
							if self.twoJSPresent == True:
								attempt = 1
								max_no_of_attempts = 3 
								found = False

								while attempt <= max_no_of_attempts and found == False:
									print "Inside While", attempt
					
									for inner_event in pygame.event.get():

										print "Inner Event Attempt", attempt
										if inner_event.type == pygame.JOYBUTTONDOWN and inner_event.button == 1 and inner_event.joy != event.joy:
											print "Second Player also started"
											#Set the joystick instance of Ghost
											self.ghostJoystick = pygame.joystick.Joystick(inner_event.joy)
					
											#Set the second player active to True
											self.secondPlayerActive = True
										
											found = True

											break

									attempt = attempt + 1

									time.sleep(1)
							
							#Load the array of LEDs to be used for first boot for displaying coins
                                                        #It will read all LEDs from JSON file. Depending upon their type, they will have different colors
                                                        app.load_layout()

															
							#Wait for 2 seconds
							time.sleep(2)

							#Flash the Pac Man and Ghost 3 times
							for i in range(0,3):
								self.dbuffer.setPixel(self.indexPacMan, (255, 255, 255), 1, self.intensityPacMan)
								self.dbuffer.setPixel(self.posAIGhost1, (255, 255, 255), 1, self.intensityAIGhost)
								if self.secondPlayerActive == False: 
									self.dbuffer.setPixel(self.posAIGhost2, (255, 255, 255), 1, self.intensityAIGhost)
								else:
									self.dbuffer.setPixel(self.indexGhost, (255, 255, 255), 1, self.intensityGhost)
								time.sleep(1)
								self.dbuffer.setPixel(self.indexPacMan, self.colorPacMan, 1, self.intensityPacMan)
								self.dbuffer.setPixel(self.posAIGhost1, self.colorAIGhost1, 1, self.intensityAIGhost)
								if self.secondPlayerActive == False:
									self.dbuffer.setPixel(self.posAIGhost2, self.colorAIGhost2, 1, self.intensityAIGhost)
								else:
									self.dbuffer.setPixel(self.indexGhost, self.colorGhost, 1, self.intensityGhost)
								time.sleep(1)
						
							#Change the game state to RUNNING
							self.gameState = GameState.RUNNING
							
							#Stop the intro sound
							pygame.mixer.music.stop()

							print "Game is running now.."
					
					elif self.gameState == GameState.RUNNING:
						#If the pause button is pressed and game is running, pause the game
						if event.button == 2:
							#Pause the game sound
							pygame.mixer.music.pause()
			
							#Change the game state to PAUSED
							self.gameState = GameState.PAUSED
						
						#If the stop button is pressed and game is running, stop the game
						if event.button == 4:
							print "Game Stopped"
							#Switch off all the LEDs
							self.reset_game()
							keys = self.data.keys()
                					for key in keys: 
								self.dbuffer.setPixel(int(key), (255, 0, 0) , 0)
			
							#Change the game state to STOPPED
							self.gameState = GameState.STOPPED
						
						#If the reset button is pressed and game is running, reset the game
						if event.button == 3:
							#Change the game state to RESETTED		
							self.gameState = GameState.RESETTED

							#Stop the game sound
							pygame.mixer.music.stop()

							#Reset the layout	
							self.reset_game()
							keys = self.data.keys()
                					for key in keys: 
								self.dbuffer.setPixel(int(key), (255, 0, 0) , 0)

							#Sleep for 2 seconds
							time.sleep(2)
			
							#Load the layout again
							self.load_layout()

			
							#Start the PacMan Sound
							pygame.mixer.music.load(os.path.join('data', 'pacman_beginning.wav'))
							pygame.mixer.music.play(-1)

							#Flash the Pac Man and Ghost 3 times
                                                        for i in range(0,3):
                                                                self.dbuffer.setPixel(self.indexPacMan, (255, 255, 255), 1, self.intensityPacMan)
                                                                self.dbuffer.setPixel(self.posAIGhost1, (255, 255, 255), 1, self.intensityAIGhost)
                                                                if self.secondPlayerActive == False:
                                                                        self.dbuffer.setPixel(self.posAIGhost2, (255, 255, 255), 1, self.intensityAIGhost)
                                                                else:
                                                                        self.dbuffer.setPixel(self.indexGhost, (255, 255, 255), 1, self.intensityGhost)
                                                                time.sleep(1)
                                                                self.dbuffer.setPixel(self.indexPacMan, self.colorPacMan, 1, self.intensityPacMan)
                                                                self.dbuffer.setPixel(self.posAIGhost1, self.colorAIGhost1, 1, self.intensityAIGhost)
                                                                if self.secondPlayerActive == False:
                                                                        self.dbuffer.setPixel(self.posAIGhost2, self.colorAIGhost2, 1, self.intensityAIGhost)
                                                                else:
                                                                        self.dbuffer.setPixel(self.indexGhost, self.colorGhost, 1, self.intensityGhost)
                                                                time.sleep(1)

		
							#Stop the intro sound
							pygame.mixer.music.stop()							

							#Change the game state to RUNNING
							self.gameState = GameState.RUNNING
					
					#If the start button is pressed and game is paused, resume the game
					elif self.gameState == GameState.PAUSED:
						if event.button == 1:
							#Start the game sound
							pygame.mixer.music.unpause()

							#Change the game state to RUNNING
							self.gameState = GameState.RUNNING

					
								
					
				#Track the PacMan and Ghost only if the game is RUNNING
				if self.gameState == GameState.RUNNING:
					if event.type == pygame.JOYAXISMOTION:
						print("Axis Moved...")
						#Joystick1 position
						jy_pos1_horizontal = self.pacManJoystick.get_axis(0)
						jy_pos1_vertical = self.pacManJoystick.get_axis(1)
					
						#Raj will check this
						if (self.twoJSPresent == True and self.secondPlayerActive == True):
							#Joystick2 position
							jy_pos2_horizontal = self.ghostJoystick.get_axis(0)
							jy_pos2_vertical = self.ghostJoystick.get_axis(1)
					
							self.handleJoystickTwo(jy_pos2_horizontal,jy_pos2_vertical)		 

						if(jy_pos1_horizontal < 0 and int(self.data[self.indexPacMan]["left"]) != -1 ):
							prev_pos = self.posPacMan
							self.direction_of_pacman = "left"

						elif(jy_pos1_horizontal > 0 and int(self.data[self.indexPacMan]["right"]) != -1 ):
							prev_pos = self.posPacMan
							self.direction_of_pacman = "right"

						if(jy_pos1_vertical > 0 and int(self.data[self.indexPacMan]["down"]) != -1):
							prev_pos = self.posPacMan
							self.direction_of_pacman = "down"

						elif(jy_pos1_vertical < 0 and int(self.data[self.indexPacMan]["up"]) != -1):
							prev_pos = self.posPacMan
							self.direction_of_pacman = "up"

							#self.indexPacMan = str(self.posPacMan)


		pygame.quit()



	def handleJoystickTwo(self,jy_pos2_horizontal,jy_pos2_vertical):					
			 
  		if(jy_pos2_horizontal < 0 and int(self.data[self.indexGhost]["left"]) != -1 ):
			print "left pressed"
			print "self.posGhost",self.posGhost					
			prev_posGhost = self.posGhost
			
			self.direction_of_ghost = "left"
				
		
		elif(jy_pos2_horizontal > 0 and int(self.data[self.indexGhost]["right"]) != -1 ):
			print "right pressed"
			print "self.posGhost",self.posGhost					
			prev_posGhost = self.posGhost
			self.direction_of_ghost = "right"

						
		if(jy_pos2_vertical > 0 and int(self.data[self.indexGhost]["down"]) != -1):
			print "down pressed"
			print "self.posGhost",self.posGhost					
			prev_posGhost = self.posGhost
			self.direction_of_ghost = "down"

						
		elif(jy_pos2_vertical < 0 and int(self.data[self.indexGhost]["up"]) != -1):
			print "up pressed"
			print "self.posGhost",self.posGhost					
			prev_posGhost = self.posGhost
			self.direction_of_ghost = "up"
	



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
					self.dbuffer.setPixel(prev_pos, (255, 255, 255), 1, self.intensityPacMan)

					#Set Pac-man's new position
					self.dbuffer.setPixel(self.posPacMan, self.colorPacMan, 1, self.intensityPacMan)

					#Play the sound
					self.chomp.play()
				#Raj will check this also
				if (self.twoJSPresent == True and self.secondPlayerActive == True):
					prev_pos = self.posGhost
					if (int(self.data[self.indexGhost][self.direction_of_ghost]) != -1):
						self.posGhost = int(self.data[self.indexGhost][self.direction_of_ghost])
						self.indexGhost = str(self.posGhost)
					
					
						#Set Off Ghost's old position
						self.dbuffer.setPixel(prev_pos, (255, 255, 255), 1, self.intensityGhost)

						#Set Ghost's new position
						self.dbuffer.setPixel(self.posGhost, self.colorGhost, 1, self.intensityGhost)

						#Play the sound
						self.chomp.play()
				
				#self.aiGhost()		
				self.lock.release()
				
			time.sleep(0.5)

	
	#this function will deal with the Artificial Ghost 
	def aiGhost1(self):
		while 1:
			#Do only when game is RUNNING
			if self.gameState == GameState.RUNNING:
				self.lock.acquire()
				
				destination = str(self.posPacMan)
				source_aighost1 = str(self.posAIGhost1)
				source_aighost2 = str(self.posAIGhost2)
				
				#Calculate only if the source and destination are different
				if source_aighost1 != destination and source_aighost2 !=destination:
				
					#This takes only string, so converted to string
					
					path1 = self.aiPath.findPathAstar1(source_aighost1, destination)
					#assign index 1 to the nextPosition of ghost as path[0] is the source iteself
					nextPosGhost1 = path1[1]
				
					#Set Off ghost's old position
					self.dbuffer.setPixel(self.posAIGhost1, (255, 255, 255), 1, self.intensityAIGhost)
				
					#Set ghost's new position
					self.posAIGhost1 = int(nextPosGhost1)
					self.dbuffer.setPixel(self.posAIGhost1, self.colorAIGhost1, 1, self.intensityAIGhost)
					 #Raj will check this
                                        #if secondplayer is not active then use this
                                        if self.secondPlayerActive == False:
                                            path2 = self.aiPath.findPathAstar2(source_aighost2,destination)
                                            nextPosGhost2 = path2[1]
                                            #Set Off ghost's old position
                                            self.dbuffer.setPixel(self.posAIGhost2, (255, 255, 255), 1, self.intensityAIGhost)

                                            #Set ghost's new position
                                            self.posAIGhost2 = int(nextPosGhost2)
                                            self.dbuffer.setPixel(self.posAIGhost2, self.colorAIGhost2, 1, self.intensityAIGhost)
					 
					#Play the sound
					self.chomp.play()

					
				#release a lock here
				self.lock.release()
				
			#This delay should be similar to ledRunning function so as to keep the speed constant
			time.sleep(0.5)

	#this function will deal with the Artificial Ghost 2
	def aiGhost2(self):
		while 1:
			#Do only when game is RUNNING
			if self.gameState == GameState.RUNNING:
				self.lock.acquire()
				
				destination = str(self.posPacMan)
				source_aighost2 = str(self.posAIGhost2)
				
				#Calculate only if the source and destination are different
				if  source_aighost2 !=destination:
				
					#This takes only string, so converted to string
					
					#Raj will check this
					#if secondplayer is not active then use this
					if self.secondPlayerActive == False:	
					    print "source, destinatiion",source_aighost2, destination 
					    #path2 = self.aiPath.findPathAstar2(source_aighost2,destination)
					    path2 = self.aiPath.findPathAstar2(source_aighost2,destination)
					    print "path2",path2
					    nextPosGhost2 = path2[1]
					    
						#Set Off ghost's old position
					    self.dbuffer.setPixel(self.posAIGhost2, (255, 255, 255), 1, self.intensityAIGhost)
				
					    #Set ghost's new position
					    self.posAIGhost2 = int(nextPosGhost2)
					    self.dbuffer.setPixel(self.posAIGhost2, self.colorAIGhost2, 1, self.intensityAIGhost)

				#release a lock here
				self.lock.release()
				
			#This delay should be similar to ledRunning function so as to keep the speed constant

if __name__ == '__main__':
	app = CGame(environment)
	#print app.scoreDict	
	#Create threads
	refreshWin = threading.Thread(target = app.ledRunningFunc, args = [])
	threadMain = threading.Thread(target = app.main, args = [])
	threadAIGhost1 = threading.Thread(target=app.aiGhost1 , args=[])
	#threadAIGhost2 = threading.Thread(target=app.aiGhost2,args=[])	
	#Start threads
	threadMain.start()
	threadAIGhost1.start()
	#threadAIGhost2.start()
	refreshWin.start()
	
	if(app.environment == Environment.ENV_DESKTOP):
		app.dbuffer.startFlushing()
	else:
		threadMain.join()
