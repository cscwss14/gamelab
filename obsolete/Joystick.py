import pygame

#Initialize the Joysticks
pygame.joystick.init()

#Get count of joysticks
joystick_count = pygame.joystick.get_count()

#We need to setup the display. Otherwise, pygame events will not work
screen_size = [500, 500]
pygame.display.set_mode(screen_size)

#Display the count of Joysticks
print("Number of Joysticks connected: "+ str(joystick_count))

#Display all the joysticks that are connected
for i in range(joystick_count):
    #We need to initialize the individual joystick instances to receive the events
    pygame.joystick.Joystick(i).init()
    print(pygame.joystick.Joystick(i).get_name())


#Capturing Joystick Events
print("Press buttons on the Joystick and see if they are captured by this program")

quit = False
while (quit != True):
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        quit = True
    #Button Pressed
    if event.type == pygame.JOYBUTTONDOWN:
        print("Button Pressed...")
    if event.type == pygame.JOYBUTTONUP:
        print("Button Released...")
    if event.type == pygame.JOYAXISMOTION:
        print("Axis Moved...")
    if event.type == pygame.JOYBALLMOTION:
        print("Ball Moved...")
    if event.type == pygame.JOYHATMOTION:
        print("Hat Moved...")


pygame.quit()
