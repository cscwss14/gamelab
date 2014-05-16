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
		self.direction_of_led = None
		
		pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
		pygame.init()                              #initialize pygame
	
		# look for sound & music files in subfolder 'data'
		pygame.mixer.music.load(os.path.join('data', 'an-turr.ogg'))#load music
		self.jump = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
		self.fail = pygame.mixer.Sound(os.path.join('data','fail.wav'))  #load sound
	
		# play music non-stop
		pygame.mixer.music.play(-1)
		
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
		pos = 1
		index = str(pos)
		data = init.config()
	
		self.direction_of_led = "right"	
		next_pos_of_led = "2"
		'''
		led.fillOff()
		led.fillRGB(255,0,0, pos, pos)
		led.update()
		'''

		prev_pos = pos

		self.dbuffer.Set_Pixel_Color(pos, (255, 0,0))
		self.dbuffer.Set_Pixel_State(pos, 1)
		
		quit = False

		clock = pygame.time.Clock()

		while (quit != True):
		   	    
			'''
			We should create a thread and copy this function in that, since only pygame.event.wait could be handled from here
			time.sleep(1)
			index_of_led = data[next_pos_of_led][self.direction_of_led]
			print "index of led", index_of_led
		    	next_pos_of_led = data[index_of_led][self.direction_of_led]
		    	print "next pos", next_pos_of_led
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
			
			       		if(jy_pos_horizontal < 0 and int(data[index]["left"]) != -1 ):
						prev_pos = pos
				        	pos = int(data[index]["left"])
						self.direction_of_led = "left"
						self.jump.play()
						self.dbuffer.Set_Pixel_Color(pos, (255, 0,0))
						self.dbuffer.Set_Pixel_State(pos, 1)
						self.dbuffer.Set_Pixel_Color(prev_pos, (0, 0, 0))
                                                self.dbuffer.Set_Pixel_State(prev_pos, 0)
				        elif(jy_pos_horizontal > 0 and int(data[index]["right"]) != -1 ):
						prev_pos = pos
						pos = int(data[index]["right"])
						self.direction_of_led = "right"
						self.fail.play()
                                                self.dbuffer.Set_Pixel_Color(pos, (255, 0,0))
                                                self.dbuffer.Set_Pixel_State(pos, 1)
						self.dbuffer.Set_Pixel_Color(prev_pos, (0, 0, 0))
                                                self.dbuffer.Set_Pixel_State(prev_pos, 0)
					if(jy_pos_vertical > 0 and int(data[index]["down"]) != -1):
						prev_pos = pos
						pos = int(data[index]["down"])
						self.direction_of_led = "down"
						self.jump.play()
                                                self.dbuffer.Set_Pixel_Color(pos, (255, 0,0))
                                                self.dbuffer.Set_Pixel_State(pos, 1)
						self.dbuffer.Set_Pixel_Color(prev_pos, (0, 0, 0))
                                                self.dbuffer.Set_Pixel_State(prev_pos, 0)
					elif(jy_pos_vertical < 0 and int(data[index]["up"]) != -1):
						prev_pos = pos
						pos = int(data[index]["up"])
						self.direction_of_led = "up"
						self.fail.play()
                                                self.dbuffer.Set_Pixel_Color(pos, (255, 0,0))
                                                self.dbuffer.Set_Pixel_State(pos, 1)
						self.dbuffer.Set_Pixel_Color(prev_pos, (0, 0, 0))
                                                self.dbuffer.Set_Pixel_State(prev_pos, 0)
			index = str(pos)
		
		
			'''
			To stop the music :D :D 
			if pygame.mixer.music.get_busy():
		            pygame.mixer.music.stop()
		        else:
		            pygame.mixer.music.play()
			'''
			
			'''
			led.fillOff()
			print "position of led", int(next_pos_of_led)
			#led.fillRGB(0,255,0,int(next_pos_of_led), int(next_pos_of_led))
	      		led.fillRGB(255, 0,0, pos, pos)
	    		led.update() 
			self.dbuffer.Set_Pixel_Color(prev_pos, (0, 255, 0))
			self.dbuffer.Set_Pixel_Color(pos, (255, 0,0))
			'''
	    
		pygame.quit()




app = CGame()
refreshWin = tc.FuncThread(app.dbuffer.Start_Flushing)
threadMain = tc.FuncThread(app.main)
refreshWin.start()
threadMain.start()
threadMain.join()
refreshWin.join()

