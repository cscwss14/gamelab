from lib.bootstrap import *
import boot.readConfig as init 
import pygame
import thread
import time
import multiprocessing 

class Environment:
	ENV_LED, ENV_DESKTOP = range(0,2)

#Pixel Class - For Storing information about each pixel
class Pixel:
	def __init__(self, led, x, y, color, state, intensity):
		self.x = x
		self.y = y
		self.color = color
		self.state = state
		self.LED = led
		self.intensity = intensity

class Display_Buffer:
	def __init__(self, environment, data):
		
		self.environment = environment	

		self.led = None
		#default color - white
		color = (255,255,255)

		#default state
		state = 0

		#default intensity
		intensity = 1.0
 
		#Get the Mapping of LED -to - Pixels
		self.Pixels_info = data

		#Initialize all the Pixels
		self.Pixels = {}
		keys = self.Pixels_info.keys()
		for key in keys:
			self.Pixels[key] = Pixel(int(key), int(self.Pixels_info[key]["x"]), int(self.Pixels_info[key]["y"]), color, state, intensity)
		
		if(self.environment == Environment.ENV_LED):
			#Initialize LED
			self.led = LEDStrip(320)
			self.led.setMasterBrightness(0.5)
			self.led.fillOff()
			self.led.update()
		else:
			#Initialize the Screen
			pygame.init()

			# Set the height and width of the screen
			size = [800, 800]
			self.screen = pygame.display.set_mode(size)
			pygame.display.set_caption("PacMan - Desktop")


	def fillOff(self):
		if(self.environment == Environment.ENV_LED):
			self.led.fillOff()
		else:
			keys = self.Pixels_info.keys()
                	for key in keys:
                        	self.Pixels[key] = Pixel(int(key), int(self.Pixels_info[key]["x"]), int(self.Pixels_info[key]["y"]), (255, 255, 255), 0, 1.0)
	

	#This Method is called only when the environment is Desktop
	#Incase of LEDs, periodic Flushing will result in blinking
	def startFlushing(self):
		print "In Flusher" + str(self.environment)		
		if(self.environment == Environment.ENV_DESKTOP):

			#Loop until the user clicks the close button.
			done = False
			clock = pygame.time.Clock()
 
			while not done:
				#print "In Flushing function"
 
    				# This limits the while loop to a max of 10 times per second.
    				# Leave this out and we will use all CPU we can.
    				#clock.tick(50)
				time.sleep(0.001)
     
    				for event in pygame.event.get(): # User did something
        				if event.type == pygame.QUIT: # If user clicked close
            					done=True # Flag that we are done so we exit this loop
                
				#Black background
    				self.screen.fill([0, 0, 0])
                        
                		#Draw the Pixels
				keys = self.Pixels.keys()
                		for key in keys:
					if(self.Pixels[key].state == 1):
    						pygame.draw.circle(self.screen, self.Pixels[key].color, [(self.Pixels[key].x + 1) * 20, (self.Pixels[key].y + 1) * 20], 5, 0)
					
		
    				# Go ahead and update the screen with what we've drawn.
    				# This MUST happen after all the other drawing commands.
    				pygame.display.flip()
 
			# Be IDLE friendly
			pygame.quit()


	#This function will push the update to the LED
	#when the environment is LED, each change in the pixel will be immediately flushed to the LEDs
	#This is for internal usage
	def pushToLed(self, pixel):
		if(pixel.state == 1):
			self.led.fillPixelWithIntensity(pixel.color[0], pixel.color[1], pixel.color[2], pixel.LED - 1, pixel.intensity)
		else:
			self.led.setOff(pixel.LED)

		self.led.update()

	def setPixelState(self, pixel, state):
		#Find the Pixel corresponding to the LED
		self.Pixels[str(pixel)].state = state
		
		#Push Immediately when environment is LED, otherwise for desktop need not do nothing
         	#Because it is refreshed periodically
         	if(self.environment == Environment.ENV_LED):
			self.pushToLed(self.Pixels[str(pixel)])

	def setPixelColor(self, pixel, color):
		#Find the Pixel corresponding to the LED
		self.Pixels[str(pixel)].color = color
		 
		
		#Push Immediately when environment is LED, otherwise for desktop need not do nothing
         	#Because it is refreshed periodically
         	if(self.environment == Environment.ENV_LED):
			self.pushToLed(self.Pixels[str(pixel)])

	def setPixel(self, pixel, color, state, intensity = 1.0):
		 #Find the Pixel corresponding to the LED
		 self.Pixels[str(pixel)].color = color
		 self.Pixels[str(pixel)].state = state
		 self.Pixels[str(pixel)].intensity = intensity
		
		 #Push Immediately when environment is LED, otherwise for desktop need not do nothing
         	 #Because it is refreshed periodically
         	 if(self.environment == Environment.ENV_LED):
		 	self.pushToLed(self.Pixels[str(pixel)])
