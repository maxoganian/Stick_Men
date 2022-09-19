# import pygame module in this program
import pygame

# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# create the display surface object
# of specific dimension..e(500, 500).
win = pygame.display.set_mode((500, 500))

# set the pygame window name
pygame.display.set_caption("Jump Game")

# object current co-ordinates
x = 200
y = 200

# dimensions of the object
width = 30
height = 40

# Stores if player is jumping or not
isjump = False

# Force (v) up and mass m.
velocity = 10
mass = .25

origVel = velocity
origMass = mass
# Indicates pygame is running
run = True

clock = pygame.time.Clock()
# infinite loop
while run:

	# completely fill the surface object
	# with black colour
	win.fill((0, 0, 0))

	# drawing object on screen which is rectangle here
	pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
	
	# iterate over the list of Event objects
	# that was returned by pygame.event.get() method.
	for event in pygame.event.get():
		
		# if event object type is QUIT
		# then quitting the pygame
		# and program both.
		if event.type == pygame.QUIT:
			
			# it will make exit the while loop
			run = False
	# stores keys pressed
	keys = pygame.key.get_pressed()
		
	if isjump == False:

		# if space bar is pressed
		if keys[pygame.K_SPACE]:
				
			# make isjump equal to True
			isjump = True
			
	if isjump :
		# calculate force (F). F = 1 / 2 * mass * velocity ^ 2.
		F =(1 / 2)*mass*(velocity**2)
		
		# change in the y co-ordinate
		y-= F
		
		# decreasing velocity while going up and become negative while coming down
		velocity = velocity-1
		
		# object reached its maximum height
		if velocity<0:
			
			# negative sign is added to counter negative velocity
			mass =-origMass

		# objected reaches its original state
		if velocity ==-11:

			# making isjump equal to false
			isjump = False

	
			# setting original values to v and m
			velocity = origVel
			mass = origMass
	

	# it refreshes the window
	pygame.display.update()

	clock.tick(20)
# closes the pygame window	
pygame.quit()
