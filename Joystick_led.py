from lib.bootstrap import *
import boot.readConfig as init 
import pygame
import os


#This function initializes sound, joystick, LED strips and returns the descriptor to Joystick

class CGame:
	def __init__(self):

		self.Joystick = None
		self.jump = None
		self.fail = None
		self.led = None
		self.joystick_names = []


		pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
		pygame.init()                              #initialize pygame
	
		# look for sound & music files in subfolder 'data'
		pygame.mixer.music.load(os.path.join('data', 'an-turr.ogg'))#load music
		jump = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
		fail = pygame.mixer.Sound(os.path.join('data','fail.wav'))  #load sound
	
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
	
	
	

	def main(self):
		#Initilialize position
		pos = 1
		index = str(pos)
		data = init.config()
		
		led.fillOff()
		led.fillRGB(255, 0,0, pos, pos)
		led.update()
		
		quit = False

		while (quit != True):
		    
		    if pygame.mixer.music.get_busy():
		        print " music is playing"
		    else:
		        print " music is not playing"
		
		    event = pygame.event.wait()
		    if event.type == pygame.QUIT:
		        quit = True
		    if event.type == pygame.JOYAXISMOTION:
		        print("Axis Moved...")
		        #Joystick position
		        jy_pos_horizontal = Joystick.get_axis(0)
			jy_pos_vertical = Joystick.get_axis(1)
		
		        if(jy_pos_horizontal < 0 and int(data[index]["left"]) != -1 ):
		        	pos = int(data[index]["left"])
				jump.play()
		
		
		        elif(jy_pos_horizontal > 0 and int(data[index]["right"]) != -1 ):
				pos = int(data[index]["right"])
				fail.play() 
		
			if(jy_pos_vertical > 0 and int(data[index]["down"]) != -1):
				pos = int(data[index]["down"])
		
			elif(jy_pos_vertical < 0 and int(data[index]["up"]) != -1):
				pos = int(data[index]["up"])
		
			index = str(pos)
		
		
			'''
			To stop the music :D :D 
			if pygame.mixer.music.get_busy():
		            pygame.mixer.music.stop()
		        else:
		            pygame.mixer.music.play()
			'''
		
			led.fillOff()
		        led.fillRGB(255, 0,0, pos, pos)
	       		led.update()
	        
	    
		pygame.quit()




app = CGame()
app.main()
