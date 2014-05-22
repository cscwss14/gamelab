from lib.bootstrap import *
import boot.readConfig as init 
import pygame
import os
import time


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

                #Connection Info
                self.connInfo =init.connectionInfo()

                #Orientation
                self.orient = init.orientation()
	
	
        def get_next_pos(self, current_pos):
		
		match_found = False
                next_pos = -1
                event = "none"
		
                #Joystick position
		jy_pos_horizontal = self.Joystick.get_axis(0)
		jy_pos_vertical = self.Joystick.get_axis(1)
		
                #get the event
                if(jy_pos_horizontal < 0): event = "left"
                elif(jy_pos_horizontal > 0): event = "right"
                
                if(jy_pos_vertical > 0): event = "down"
                elif(jy_pos_vertical < 0): event = "up"

                for i in xrange(len(self.orient)):
                	index = str(i+1)
                	start = int(self.orient[index]["start"])
        		end = int(self.orient[index]["end"])
        		if( current_pos >= start and current_pos <=end):
                		print "Non-Connection Point"
                		match_found = True
                                        
                                #if the orientation is Horizontal Left
                                if(int(self.orient[index]["orient"]) == 0):
					if( event == "right"): next_pos = current_pos - 1
                                        if( event == "left"): next_pos = current_pos + 1

                                #if the orientation is Horizontal Right
                                if(int(self.orient[index]["orient"]) == 1):
					if( event == "right"): next_pos = current_pos + 1
                                        if( event == "left"): next_pos = current_pos - 1

                                #if the orientation is Vertical Down
                                if(int(self.orient[index]["orient"]) == 2):
					if( event == "down"): next_pos = current_pos + 1
                                        if( event == "up"): next_pos = current_pos - 1
                               
                                #if the orientation is Vertical Up
                                if(int(self.orient[index]["orient"]) == 3):
					if( event == "up"): next_pos = current_pos + 1
                                        if( event == "down"): next_pos = current_pos - 1

		if(match_found == False and event!="none"):
        		print "Connection Point"
                        print "Current Pos:", current_pos
                        print "Event is :", event
                        next_pos = int(self.connInfo[str(current_pos)][event])

                return next_pos	

	def main(self):
		#Initilialize position
		pos = 1
	        next_pos = pos
		self.direction_of_led = "right"	
		next_pos_of_led = "2"
		led.fillOff()
		led.fillRGB(255,0,0, pos, pos)
		led.update()
		
		quit = False

		while (quit != True):
		   	    
			'''
			We should create a thread and copy this function in that, since only pygame.event.wait could be handled from here
			time.sleep(1)
			index_of_led = data[next_pos_of_led][self.direction_of_led]
			print "index of led", index_of_led
		    	next_pos_of_led = data[index_of_led][self.direction_of_led]
		    	print "next pos", next_pos_of_led
			'''
		    	if pygame.mixer.music.get_busy():
		        	print " music is playing"
		    	else:
		        	print " music is not playing"
		
		        event = pygame.event.wait()
		    	if event.type == pygame.QUIT:
		        	quit = True
		    	if event.type == pygame.JOYAXISMOTION:
		        	print("Axis Moved...")
                               
                                #Get the next pos             
		        	next_pos = self.get_next_pos(pos)
                               
                                #Music
                                if(next_pos == -1): self.fail.play() 
                                else: 
					self.jump.play()
                                        pos = next_pos
		
		
			'''
			To stop the music :D :D 
			if pygame.mixer.music.get_busy():
		            pygame.mixer.music.stop()
		        else:
		            pygame.mixer.music.play()
			'''
		
			led.fillOff()
			print "position of led", int(next_pos_of_led)
			#led.fillRGB(0,255,0,int(next_pos_of_led), int(next_pos_of_led))
	      		led.fillRGB(255, 0,0, pos, pos)
	    		led.update()
	    
		pygame.quit()




app = CGame()
app.main()
