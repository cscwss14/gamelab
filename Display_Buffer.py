from lib.bootstrap import *
import boot.readConfig as init 
import pygame
import thread
import time
import multiprocessing 

ENV_LED = 0
ENV_DESKTOP = 1

#Pixel Class - For Storing information about each pixel
class Pixel:
	def __init__(self, x, y, color, state):
		self.x = x
		self.y = y
		self.color = color
                self.state = state
		self.LED = 0

class Display_Buffer:
	def __init__(self, environment):
		
		self.environment = environment	

		#default color - green
		color = (0,255,0)
			
                #default state
                state = 0               
 
		#Initialize all the Pixels
		self.Pixels = []
		for x in xrange(10):
			for y in xrange(10):
				self.Pixels.append(Pixel(x, y, color, state))


		#Get the Mapping of LED -to - Pixels
		self.Pixels_info = init.read_pixel_info()

		#Initialize the LEDs
		keys = self.Pixels_info.keys()
		for key in keys:
			for index in xrange(len(self.Pixels)):
				if((self.Pixels[index].x  == int(self.Pixels_info[key]["x"])) and (self.Pixels[index].y  == int(self.Pixels_info[key]["y"]))):
					self.Pixels[index].LED = int(key)  

		#Initialize LED
                self.led = LEDStrip(159)
                self.led.setMasterBrightness(0.5)

	
	def Start_Flushing(self):
		print "In Flusher" + str(self.environment)		
		if(self.environment == ENV_DESKTOP):
			#Initialize the Screen
			pygame.init()		

			# Set the height and width of the screen
			size = [600, 600]
			screen = pygame.display.set_mode(size)
 
			pygame.display.set_caption("PacMan - Desktop")
 
			#Loop until the user clicks the close button.
			done = False
			clock = pygame.time.Clock()
 
			while not done:
 
    				# This limits the while loop to a max of 10 times per second.
    				# Leave this out and we will use all CPU we can.
    				clock.tick(50)
     
    				for event in pygame.event.get(): # User did something
        				if event.type == pygame.QUIT: # If user clicked close
            					done=True # Flag that we are done so we exit this loop
                        	#White background
    				screen.fill([255, 255, 255])
                        
                        	#Draw the Pixels
                        	for item in self.Pixels:
    					pygame.draw.circle(screen, item.color, [(item.x + 1) * 50, (item.y + 1) * 50], 10, 0)
    
    				# Go ahead and update the screen with what we've drawn.
    				# This MUST happen after all the other drawing commands.
    				pygame.display.flip()
 
			# Be IDLE friendly
			pygame.quit()
		else:	
			done = False
                        clock = pygame.time.Clock()
			
			self.led.fillOff()
			self.led.update()

			while not done:
				print "Flushing"
				self.led.fillOff()
				self.led.update()
				clock.tick(50)
				#Flush the data to the LED Strips
				for item in self.Pixels:
					if(item.state == 1):
						self.led.fillRGB(item.color[0], item.color[1], item.color[2], item.LED, item.LED)
						self.led.update()
	def Flush_Once(self):
		self.led.fillOff()
                self.led.update()
		print "Flushing once"
               
                #Flush the data to the LED Strips
                for item in self.Pixels:
                	if(item.state == 1):
                        	self.led.fillRGB(item.color[0], item.color[1], item.color[2], item.LED, item.LED)
                                self.led.update()

	def Set_Pixel_State(self, pixel, state):
		#Find the Pixel corresponding to the LED
		for item in xrange(len(self.Pixels)):
			if(self.Pixels[item].LED == pixel):
				self.Pixels[item].state = state

	def Set_Pixel_Color(self, pixel, color):
		#Find the Pixel corresponding to the LED
		for item in xrange(len(self.Pixels)):
                        if(self.Pixels[item].LED == pixel):
                                self.Pixels[item].color = color
