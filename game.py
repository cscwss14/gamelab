from lib.bootstrap import *
import boot.readConfig as init 
import pygame
import os
import time, threadClass as tc
import Display_Buffer as dbuff

ENV_LED = 0
ENV_DESKTOP = 1

class CGame:
	def __init__(self):

		self.Joystick = None
		self.jump = None
		self.fail = None
		self.led = None
		self.joystick_names = []
		self.direction_of_pacman = None
		self.data  = init.config()
		self.posPacMan = 1
		self.index = str(self.posPacMan)
		self.direction_of_pacman = "up"	
		
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

		
		#Initialize LED
		self.led = LEDStrip(159)
		self.led.setMasterBrightness(0.5)
		
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
		self.dbuffer = dbuff.Display_Buffer(ENV_LED)




	def main(self):
		#Initilialize position
		self.posPacMan = 1
		self.index = str(self.posPacMan)
		self.direction_of_pacman = "right"	
		self.nextIndexPacman = "2"
		'''
		led.fillOff()
		led.fillRGB(255,0,0, self.posPacMan, self.posPacMan)
		led.update()
		'''

		prev_pos = self.posPacMan
		#Here fill all the LEDs with Yellow
		'''
		for i in range(159):
                        led.fillRGB(255, 255,0, i, i)
                        led.update()
		'''
		#Load the array of LEDs to be used for first boot for displaying coins
		#To implement, right now initializing everything		
                led.fillRGB(255, 255,0, 0, 0)
                led.update()
                led.fillRGB(255, 0,0, self.posPacMan, self.posPacMan)
                led.update()
		quit = False

		clock = pygame.time.Clock()

		while (quit != True):
		   	    
			'''
			We should create a thread and copy this function in that, since only pygame.event.wait could be handled from here
			time.sleep(1)
			self.index_of_led = self.data[self.nextIndexPacman][self.direction_of_pacman]
			print "self.index of led", self.index_of_led
		    	self.nextIndexPacman = self.data[self.index_of_led][self.direction_of_pacman]
		    	print "next pos", self.nextIndexPacman
			'''
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
						#led.setOff(posPacMan)
						dictn ={self.posPacMan:(255,0,0),prev_pos:(0,0,0)}
						led.fillIndexes(dictn)				
                        			led.update()
						#self.jump.play()
				        elif(jy_pos_horizontal > 0 and int(self.data[self.index]["right"]) != -1 ):
						prev_pos = self.posPacMan
						self.posPacMan = int(self.data[self.index]["right"])
						self.direction_of_pacman = "right"
						#self.fail.play()
						#led.setOff(self.posPacMan)
						dictn ={self.posPacMan:(255,0,0),prev_pos:(0,0,0)}
						led.fillIndexes(dictn)				
                        			led.update()
					if(jy_pos_vertical > 0 and int(self.data[self.index]["down"]) != -1):
						prev_pos = self.posPacMan
						self.posPacMan = int(self.data[self.index]["down"])
						self.direction_of_pacman = "down"
						#self.jump.play()
						#led.setOff(self.pos)
						dictn ={self.posPacMan:(255,0,0),prev_pos:(0,0,0)}
						led.fillIndexes(dictn)				
                        			led.update()
					elif(jy_pos_vertical < 0 and int(self.data[self.index]["up"]) != -1):
						prev_pos = self.posPacMan
						self.posPacMan = int(self.data[self.index]["up"])
						self.direction_of_pacman = "up"
						#led.setOff(self.posPacMan)
						dictn ={self.posPacMan:(255,0,0),prev_pos:(0,0,0)}
						led.fillIndexes(dictn)				
                        			led.update()
						#self.fail.play()
					
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
		'''
		self.posPacMan = 1
		self.index = str(self.posPacMan)
		
	
		
		prev_pos = self.posPacMan
	
		#Load the array of LEDs to be used for first boot for displaying coins
		#To implement, right now initializing everything		
                
		led.fillRGB(255, 255,0, 0, 0)
                led.update()
                led.fillRGB(255, 0,0, self.posPacMan, self.posPacMan)
                led.update()
		'''
		print "direction",self.direction_of_pacman
		print "self.posPacMan", self.posPacMan
		while 1:
			#print "prev_pos,posPacMan",prev_pos, self.posPacMan
			#put a lock here
			prev_pos = self.posPacMan
			if (int(self.data[self.index][self.direction_of_pacman]) != -1):
				self.posPacMan = int(self.data[self.index][self.direction_of_pacman])
				self.index = str(self.posPacMan)

			dictn ={self.posPacMan:(255,0,0),prev_pos:(0,0,0)}
			led.fillIndexes(dictn)				
                    	led.update()
			#release here
			time.sleep(2)
			
		



app = CGame()
refreshWin = tc.FuncThread(app.ledRunningFunc)
threadMain = tc.FuncThread(app.main)
refreshWin.start()
threadMain.start()
threadMain.join()
refreshWin.join()
#app.main()
#app.ledRunningFunc()
