import boot.readConfig as init 
from lib import threadClass as tc, displayBuffer as dbuff,pathFinding as pf
import pygame, os,time
import sys, getopt, threading
from threading import Timer

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
		self.posAIGhost3 = "80"
		self.posSpecialBeans = []
		self.indexPacMan = str(self.posPacMan)
		self.indexGhost = str(self.posGhost)
		
		
		#initial direction
		self.direction_of_pacman = "up"	
		self.direction_of_ghost = "down"

		#Pacman Speed
		self.pacmanSpeed = 1.0	
		
		#Sleep Time
		self.sleepTime = 0.5

		#initial colors
		self.colorAIGhost1 = (174,13,155) 
		self.colorAIGhost2 = (221,118,2) 
		self.colorAIGhost3 = (174,13,155)

		self.colorPacMan = (255, 255, 0)
		self.colorGhost = (255, 0, 0)
		self.colorCoins = (255,255,255)
		self.colorCollectedCoins = (12,223,223)
		self.colorSpecialBean = (0, 255, 0)
		
		#Initial State of the game
		self.gameState = GameState.STOPPED

	
		self.environment = environment
		self.secondPlayerActive= False
		
		#Intensities
		self.intensityPacMan = 1.0
		self.intensityGhost = 1.0
		self.intensityAIGhost = 1.0
		self.intensityCoins = 0.5
		self.intensityCollectedCoins = 0.15
		self.intensitySpecialBean = 1.0

		self.twoJSPresent = False
		self.lock = threading.Lock()

		#Timer
		self.timer = Timer(5, self.reset_speed)
		
		#Initialize the display buffer
		self.dbuffer = dbuff.Display_Buffer(self.environment, self.data)
		self.aiPath = pf.CFindPath(self.data)	
		#after every 3 seconds the aggressive ghost will scatter
		self.scatterTime = 0
	
		#call this function again to reset this dictionary
		self.scoreDict = self.aiPath.getNewScoreDict()
		#print "score dict", self.scoreDict
		self.numOfCoins = len(self.scoreDict)

		#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
		pygame.init()                              #initialize pygame

		#We need to setup the display. Otherwise, pygame events will not work
		#screen_size = [800, 800]
		#pygame.display.set_mode(screen_size)
               

		# look for sound & music files in subfolder 'data'
		#self.chomp = pygame.mixer.Sound(os.path.join('data','pacman_chomp.wav'))  #load sound
		#self.eat_fruit = pygame.mixer.Sound(os.path.join('data','pacman_eatfruit.wav'))  #load sound
		#self.pacman_death = pygame.mixer.Sound(os.path.join('data','pacman_death.wav'))  #load sound 	               
               
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
        
	#this function is the callback function to reset the speed of the pacman
	def reset_speed(self):
		self.pacmanSpeed = 1.0
		  
	
	#this function loads the game layout
	def load_layout(self):
		
		#reinitialize the scoring dictionary here based on the entries given in the json file
		#and then correspondingly modify the coins based on the second player
		self.scoreDict = self.aiPath.getNewScoreDict()
	
		keys = self.data.keys()
		for key in keys:
			if(self.data[key]["type"] == "P"):
				self.dbuffer.setPixel(int(key), self.colorPacMan , 1, self.intensityPacMan)
				self.posPacMan = int(key)
				self.indexPacMan = str(self.posPacMan)
				#since this is player, remove this entry from score calculation dictionary
				#TODO:
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
			
			elif(self.data[key]["type"] == "AI3"):
				    self.dbuffer.setPixel(int(key), self.colorAIGhost3 , 1, self.intensityAIGhost)
				    self.posAIGhost3 = int(key)
				    self.indexAIGhost = str(self.posAIGhost3)

			elif(self.data[key]["type"] == "C"):
				self.dbuffer.setPixel(int(key), self.colorCoins , 1, self.intensityCoins)

			elif(self.data[key]["type"] == "SB"):
				self.dbuffer.setPixel(int(key), self.colorSpecialBean, 1, self.intensitySpecialBean)
				self.posSpecialBeans.append(int(key))
						
		
		#this is the number of coins the pacman should collect to win
		self.numOfCoins = len(self.scoreDict)


	#this function resets the variables
	def reset_game(self):
		self.dbuffer.fillOff()
		#Reset all the variables
		self.posPacMan = 1
		self.posGhost = 1
		self.posAIGhost1 = "72"
		self.posAIGhost2 = "80"
		self.posAIGhost3 = "80"
		self.posSpecialBeans = []
                self.indexPacMan = str(self.posPacMan)
                self.indexGhost = str(self.posGhost)
	
                self.direction_of_pacman = "up" 
                self.direction_of_ghost = "down"
		self.numOfCoins = None
		self.scoreDict = None
		self.secondPlayerActive = False  
		 
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
							#pygame.mixer.music.load(os.path.join('data', 'pacman_beginning.wav'))
							#pygame.mixer.music.play(-1)

							
							#Set the joystick instance of PacMan
							self.pacManJoystick = pygame.joystick.Joystick(event.joy)

							#if second joystick is present, then wait for the second player (ghost) to start the game
							if self.twoJSPresent == True:
								attempt = 1
								max_no_of_attempts = 5 
								found = False
								self.secondPlayerActive = False
								while attempt <= max_no_of_attempts and found == False:
									#print "---------------Inside While-----------", attempt
					
									for inner_event in pygame.event.get():

										#print "-----Inner Event Attempt-----", attempt
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
                                                        self.load_layout()

															
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
								self.dbuffer.setPixel(self.posAIGhost3, (255, 255, 255), 1, self.intensityAIGhost)
								time.sleep(0.5)
								self.dbuffer.setPixel(self.indexPacMan, self.colorPacMan, 1, self.intensityPacMan)
								self.dbuffer.setPixel(self.posAIGhost1, self.colorAIGhost1, 1, self.intensityAIGhost)
								if self.secondPlayerActive == False:
									self.dbuffer.setPixel(self.posAIGhost2, self.colorAIGhost2, 1, self.intensityAIGhost)
								else:
									self.dbuffer.setPixel(self.indexGhost, self.colorGhost, 1, self.intensityGhost)
								self.dbuffer.setPixel(self.posAIGhost3, (255, 255, 255), 1, self.intensityAIGhost)
								time.sleep(1)
						
							#Change the game state to RUNNING
							self.gameState = GameState.RUNNING
							
							#Stop the intro sound
							#pygame.mixer.music.stop()

							#print "Game is running now.."
					
					elif self.gameState == GameState.RUNNING:
						#If the pause button is pressed and game is running, pause the game
						if event.button == 2:
							#play the intermission sound
							#pygame.mixer.music.load(os.path.join('data', 'pacman_intermission.wav'))
                                                        #pygame.mixer.music.play(-1)

			
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
							#pygame.mixer.music.stop()

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
							#pygame.mixer.music.load(os.path.join('data', 'pacman_beginning.wav'))
							#pygame.mixer.music.play(-1)

							#Flash the Pac Man and Ghost 3 times
                                                        for i in range(0,3):
                                                                self.dbuffer.setPixel(self.indexPacMan, (255, 255, 255), 1, self.intensityPacMan)
                                                                self.dbuffer.setPixel(self.posAIGhost1, (255, 255, 255), 1, self.intensityAIGhost)
                                                                if self.secondPlayerActive == False:
                                                                        self.dbuffer.setPixel(self.posAIGhost2, (255, 255, 255), 1, self.intensityAIGhost)
                                                                else:
                                                                        self.dbuffer.setPixel(self.indexGhost, (255, 255, 255), 1, self.intensityGhost)
								self.dbuffer.setPixel(self.posAIGhost3, (255, 255, 255), 1, self.intensityAIGhost)
                                                                time.sleep(1)
                                                                self.dbuffer.setPixel(self.indexPacMan, self.colorPacMan, 1, self.intensityPacMan)
                                                                self.dbuffer.setPixel(self.posAIGhost1, self.colorAIGhost1, 1, self.intensityAIGhost)
                                                                if self.secondPlayerActive == False:
                                                                        self.dbuffer.setPixel(self.posAIGhost2, self.colorAIGhost2, 1, self.intensityAIGhost)
                                                                else:
                                                                        self.dbuffer.setPixel(self.indexGhost, self.colorGhost, 1, self.intensityGhost)
								self.dbuffer.setPixel(self.posAIGhost3, (255, 255, 255), 1, self.intensityAIGhost)
                                                                time.sleep(1)

		
							#Stop the intro sound
							#pygame.mixer.music.stop()							

							#Change the game state to RUNNING
							self.gameState = GameState.RUNNING
					
					#If the start button is pressed and game is paused, resume the game
					elif self.gameState == GameState.PAUSED:
						if event.button == 1:
							#Stop the intermission game sound
							#pygame.mixer.music.stop()

							#Change the game state to RUNNING
							self.gameState = GameState.RUNNING

					
								
					
				#Track the PacMan and Ghost only if the game is RUNNING
				if self.gameState == GameState.RUNNING:
					if event.type == pygame.JOYAXISMOTION:
						#print("Axis Moved...")
						#Joystick1 position
						jy_pos1_horizontal = self.pacManJoystick.get_axis(4)
						jy_pos1_vertical = self.pacManJoystick.get_axis(5)
					
						#Raj will check this
						if (self.twoJSPresent == True and self.secondPlayerActive == True):
							#Joystick2 position
							jy_pos2_horizontal = self.ghostJoystick.get_axis(4)
							jy_pos2_vertical = self.ghostJoystick.get_axis(5)
					
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
			self.direction_of_ghost = "left"
				
		
		elif(jy_pos2_horizontal > 0 and int(self.data[self.indexGhost]["right"]) != -1 ):
			self.direction_of_ghost = "right"

						
		if(jy_pos2_vertical > 0 and int(self.data[self.indexGhost]["down"]) != -1):
			self.direction_of_ghost = "down"

						
		elif(jy_pos2_vertical < 0 and int(self.data[self.indexGhost]["up"]) != -1):
			self.direction_of_ghost = "up"
	



	#This function will be called in another thread which will increment the PACMAN with each clocktick
	def pacmanRunningFunc(self):
		
		while 1:
			#print "LED Running Function"		
			self.lock.acquire()
			#Do only when game is RUNNING
			if self.gameState == GameState.RUNNING:
				
				prev_pos = self.posPacMan
				if (int(self.data[self.indexPacMan][self.direction_of_pacman]) != -1):
					#Mark this position visited, if not already visited and decrease the number of counts
                                        index = str(prev_pos)	
					#print "index------------", index
					#print "dict", self.scoreDict
					if(self.scoreDict[index] == False):
                                        	self.scoreDict[index] = True
                                               	self.numOfCoins = self.numOfCoins - 1
			
						#If not already visited, then consume the coin and change the color of the coin
						self.dbuffer.setPixel(prev_pos, self.colorCollectedCoins, 1, self.intensityCollectedCoins)
			
						#If the coin is one of the special bean
						if prev_pos in self.posSpecialBeans:
							#Play the sound
							#self.eat_fruit.play()
							
							#If already in fast mode, then stop the timer and start over timer
							if (self.pacmanSpeed > 1.0 ):
								#Stop the timer
								self.timer.cancel()

								#Start the new timer
								self.timer = Timer(10, self.reset_speed)
								self.timer.start()
							else:
								#Start the new timer
								self.timer = Timer(10, self.reset_speed)
								self.timer.start()
								
							#Increase the speed of the pacman
							self.pacmanSpeed = self.pacmanSpeed + 1
							

						#Play the sound
						#self.chomp.play()
					else:
						#If already visited, then set the color to the color of the coin
						self.dbuffer.setPixel(prev_pos, self.colorCollectedCoins, 1, self.intensityCollectedCoins)

	

					self.posPacMan = int(self.data[self.indexPacMan][self.direction_of_pacman])
					self.indexPacMan = str(self.posPacMan)
					

					#Set Pac-man's new position
					self.dbuffer.setPixel(self.posPacMan, self.colorPacMan, 1, self.intensityPacMan)


				if(self.pacmanWon() == True):
                                        print "------------Pacman Won------------"
                                        #Make all leds yellow from down to top
					keys = self.data.keys()
					for key in keys:
						self.dbuffer.setPixel(int(key), (255, 255, 0), 1, 0.5)                                       
 
					time.sleep(1)
                                        
					#Turn off all leds
                                        self.reset_game()
                                        for key in keys:
                                        	self.dbuffer.setPixel(int(key), (255, 0, 0) , 0)
					
					#Change the game state to STOPPED
					self.gameState = GameState.STOPPED	

				self.afterLosing()

			#if the numOfCoins decreases to lesser than 100 activate the aggressive chase 	
			if(self.numOfCoins > 35):	
				if(self.scatterTime < 5 ):
					self.scatterTime +=1
				else:	
					self.scatterTime = 0
					self.aiPath.scatterMode = not self.aiPath.scatterMode
			else:
				self.aiPath.scatterMode = False

			self.lock.release()
				
			time.sleep(self.sleepTime / self.pacmanSpeed)
	
	#This function will be called in another thread which will increment the GHOST with each clocktick
        def ghostRunningFunc(self):
		while 1:
                        #print "Ghost Running Function"
                        self.lock.acquire()
                        #Do only when game is RUNNING
                        if self.gameState == GameState.RUNNING:
				if (self.twoJSPresent == True and self.secondPlayerActive == True):
                                        prev_posGhost = self.posGhost
                                        if (int(self.data[self.indexGhost][self.direction_of_ghost]) != -1):
                                                self.posGhost = int(self.data[self.indexGhost][self.direction_of_ghost])
                                                self.indexGhost = str(self.posGhost)

                                                #Set Off Ghost's old position
                                                #If that position is not visited by pacman, then set the color to coins
                                                #Otherwise, set the color to collected coins
                                                index = str(prev_posGhost)
                                                if(self.scoreDict[index] == False):
							if prev_posGhost in self.posSpecialBeans:
								 self.dbuffer.setPixel(prev_posGhost, self.colorSpecialBean, 1, self.intensitySpecialBean)
							else:
                                                        	self.dbuffer.setPixel(prev_posGhost, self.colorCoins, 1, self.intensityCoins)
                                                else:
                                                         self.dbuffer.setPixel(prev_posGhost, self.colorCollectedCoins, 1, self.intensityCollectedCoins)


                                                #Set Ghost's new position
                                                self.dbuffer.setPixel(self.posGhost, self.colorGhost, 1, self.intensityGhost)
					self.afterLosing()
			self.lock.release()
			
			#TBD - TEmp Fix
			time.sleep(self.sleepTime)



	
	def pacmanWon(self):
        #This function simply checks the current number of coins to collect as of now and decides the winner"""
		#print "------number of coins-----",self.numOfCoins
		if (self.numOfCoins == 1):
                	return True

        def pacmanLost(self):
	#This function checks if any of the ghosts caught the pacman or not"""
                if(self.posAIGhost1 == self.posPacMan):
                       return True
                #if second player is inactive then check if second player's
                if (self.secondPlayerActive == False and self.posAIGhost2 == self.posPacMan):
                       return True
		#if second player is active and player ghost caught the pacman
		if (self.secondPlayerActive == True and self.posGhost == self.posPacMan):
		       return True
                if(self.posAIGhost3 == self.posPacMan):
                       return True

	
	#this function will deal with the Artificial Ghost 
	def aiGhost1(self):
		while 1:
			self.lock.acquire()
			#Do only when game is RUNNING
			if self.gameState == GameState.RUNNING:

				
				destination = str(self.posPacMan)
				source_aighost1 = str(self.posAIGhost1)
				source_aighost2 = str(self.posAIGhost2)
				source_aighost3 = str(self.posAIGhost3)
				
				#Calculate only if the source and destination are different
				#TODO : This condition is really not needed here after implementing termination situation: DISCUSS
				if source_aighost1 != destination and source_aighost2 !=destination and source_aighost3 !=destination:
						
						
					nextPosGhost1 = self.aiPath.findPathAstar1(source_aighost1, destination)

					
					#Set Off ghost's old position
					#If the path is already visited by the pacman, then set the color to Collected coin color, otherwise set the color to Coin color
                                        if(self.scoreDict[source_aighost1] == False):
						if self.posAIGhost1 in self.posSpecialBeans:
							 self.dbuffer.setPixel(self.posAIGhost1, self.colorSpecialBean, 1, self.intensitySpecialBean)
						else:
                                                       	self.dbuffer.setPixel(self.posAIGhost1, self.colorCoins, 1, self.intensityCoins)
					else:
						self.dbuffer.setPixel(self.posAIGhost1, self.colorCollectedCoins, 1, self.intensityCollectedCoins)

						
				
					#Set ghost's new position
					self.posAIGhost1 = int(nextPosGhost1)
					self.dbuffer.setPixel(self.posAIGhost1, self.colorAIGhost1, 1, self.intensityAIGhost)

                                        #if secondplayer is not active then use this
                                        if self.secondPlayerActive == False:
					    nextPosGhost2 = self.aiPath.findPathAstar2(source_aighost2,destination)
  						
					    #Set Off ghost's old position
                                            #If the path is already visited by the pacman, then set the color to Collected coin color, otherwise set the color to Coin color
                                            if(self.scoreDict[source_aighost2] == False):
						if self.posAIGhost2 in self.posSpecialBeans:
							 self.dbuffer.setPixel(self.posAIGhost2, self.colorSpecialBean, 1, self.intensitySpecialBean)
						else:
                                                       	self.dbuffer.setPixel(self.posAIGhost2, self.colorCoins, 1, self.intensityCoins)
                                            else:
                                                self.dbuffer.setPixel(self.posAIGhost2, self.colorCollectedCoins, 1, self.intensityCollectedCoins)
                                          

                                            #Set ghost's new position
                                            self.posAIGhost2 = int(nextPosGhost2)
                                            self.dbuffer.setPixel(self.posAIGhost2, self.colorAIGhost2, 1, self.intensityAIGhost)
					

					nextPosGhost3 = self.aiPath.findPathScattered(source_aighost3, destination)
					
					#Set Off ghost's old position
                                        #If the path is already visited by the pacman, then set the color to Collected coin color, otherwise set the color to Coin color
                                        if(self.scoreDict[source_aighost3] == False):
						if self.posAIGhost3 in self.posSpecialBeans:
                                                	self.dbuffer.setPixel(self.posAIGhost3, self.colorSpecialBean, 1, self.intensitySpecialBean)
                                        	else:
                                               		self.dbuffer.setPixel(self.posAIGhost3, self.colorCoins, 1, self.intensityCoins)
					else:
						self.dbuffer.setPixel(self.posAIGhost3, self.colorCollectedCoins, 1, self.intensityCollectedCoins)

					#Set ghost's new position
					self.posAIGhost3 = int(nextPosGhost3)
					self.dbuffer.setPixel(self.posAIGhost3, self.colorAIGhost3, 1, self.intensityAIGhost)
					 

					#Play the sound
					#self.chomp.play()

				self.afterLosing()

		

			#release a lock here
			self.lock.release()
			#This delay should be similar to ledRunning function so as to keep the speed constant
			time.sleep(0.5)
	def afterLosing(self):
		if(self.pacmanLost() == True):
		#Play the sound
		#self.pacman_death.play()
	
                     	#Make all leds red from down to top
                	keys = self.data.keys()
                        for key in keys:
                        	self.dbuffer.setPixel(int(key), (255, 0, 0), 1, 0.5)                         

                        time.sleep(1)

                        #Turn off all leds
                        self.reset_game()
                        for key in keys:
                        	self.dbuffer.setPixel(int(key), (255, 0, 0) , 0)

                      	#Change the game state to STOPPED
                        self.gameState = GameState.STOPPED		
		
		
				

if __name__ == '__main__':
	app = CGame(environment)
	
	#Create threads
	refreshPacman = threading.Thread(target = app.pacmanRunningFunc, args = [])
	refreshGhost = threading.Thread(target = app.ghostRunningFunc, args = [])
	threadMain = threading.Thread(target = app.main, args = [])
	threadAIGhost1 = threading.Thread(target=app.aiGhost1 , args=[])

	#Start threads
	threadMain.start()
	threadAIGhost1.start()
	refreshPacman.start()
	refreshGhost.start()
	
	if(app.environment == Environment.ENV_DESKTOP):
		app.dbuffer.startFlushing()
	else:
		threadMain.join()
	
