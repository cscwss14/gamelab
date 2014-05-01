from bootstrap import *
import pygame

#Initialize the Joysticks
pygame.joystick.init()

#Initialize LED
led = LEDStrip(159)
led.setMasterBrightness(0.5)

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
Joystick = pygame.joystick.Joystick(0)

#Initilialize position
pos = 1
quit = False
while (quit != True):
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        quit = True
    if event.type == pygame.JOYAXISMOTION:
        print("Axis Moved...")
        #Joystick position
        jy_pos = Joystick.get_axis(0)
        if(jy_pos < 0):
        	pos = pos - 1
        elif(jy_pos > 0):
		pos = pos + 1
	led.fillOff()
        led.fillRGB(255, 0,0, pos, pos)
        led.update()
        
    
pygame.quit()

