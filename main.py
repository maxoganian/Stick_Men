import pygame

numPlayers = 2

class Player(pygame.sprite.Sprite):
    
    def __init__(self, xStart, yStart):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/stick_man.png")
        self.rect = self.surf.get_rect(center = (xStart, yStart))
        self.yVel = 0
        self.xVel = 0
        self.jumpHeight = 20
        self.gravPower = 2
        self.speed = 10
        self.isJumping = False

    # Move the sprite based on user keypresses
    def update(self, pressedKeys, keydown, keyup, leftKey, rightKey, upKey):
        platform_hit_list = pygame.sprite.spritecollide(self, all_platforms, False)
        
        self.calc_grav()

        if keydown:
            if pressedKeys[leftKey]:
                self.xVel = -self.speed
            if pressedKeys[rightKey]:
                self.xVel = self.speed

            if pressedKeys[upKey]:
                # move down a bit and see if there is a platform below us.
                self.rect.y += 2
                platform_hit_list = pygame.sprite.spritecollide(self, all_platforms, False)
                self.rect.y -= 2
         
                # If it is ok to jump, set our speed upwards
                if platform_hit_list != []:
                    self.yVel = -self.jumpHeight
        elif keyup:
            if event.key == leftKey:
                self.xVel = 0
            if event.key == rightKey:
                self.xVel = 0

        # Move left/right
        self.rect.move_ip(self.xVel,0)

        # See if we hit anything
        platform_hit_list = pygame.sprite.spritecollide(self, all_platforms, False)
        for platform in platform_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.xVel > 0:
                self.rect.right = platform.rect.left
            elif self.xVel < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = platform.rect.right
 

        #move up/down
        self.rect.move_ip(0,self.yVel)

        # Check and see if we hit anything
        platform_hit_list = pygame.sprite.spritecollide(self, all_platforms, False)
        
        for platform in platform_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.yVel > 0:
                self.rect.bottom = platform.rect.top
            elif self.yVel < 0:
                self.rect.top = platform.rect.bottom
 
            # Stop our vertical movement
            self.yVel = 0
        
        # Keep player on the screen
        if self.rect.right < 0:
            self.rect.left = WIDTH-2
            #add a little height so we can move smoothly from platforms on either side
            self.rect.y-=5
        if self.rect.left > WIDTH:
            self.rect.right = 2
            self.rect.y-=5
        #for now fall to top, maybe die later
        if self.rect.top > HEIGHT:
            self.rect.bottom = 2
        #also let jump through ceiling, w/ current map not really aplicable
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT-2

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.yVel == 0:
            self.yVel = 1
        else:
            self.yVel += self.gravPower


numPlatforms = 8
class Platform(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos):
        super(Platform, self).__init__()
        self.surf = pygame.image.load("images/platform.png")
        self.rect = self.surf.get_rect(center = (xPos, yPos))

     
#game window width and height
WIDTH = 1000
HEIGHT = 600

# Create the screen object
# The size is determined by the constant WIDTH and HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#create players
players = []
for i in range(numPlayers):
    players.append(Player((i*400)+100, 400))

platforms = []
for i in range(numPlatforms):
    if i<3:
        platforms.append(Platform((i*400)+100, 500))
    elif i<5:
        platforms.append(Platform(((i-3)*400)+300, 400))
    elif i<9:
        platforms.append(Platform(((i-5)*400)+100, 300))

#deal with sprite groups
all_players = pygame.sprite.Group()
for player in players:
    print(player)
    all_players.add(player)
print("----------")

all_platforms = pygame.sprite.Group()
for platform in platforms:
    print(platform)
    all_platforms.add(platform)

all_sprites = pygame.sprite.Group()
all_sprites.add(all_players)
all_sprites.add(all_platforms)

# Setup the clock
clock = pygame.time.Clock()

running = True
while running:
    keydown = False
    keyup = False

    # for loop through the event queue
    for event in pygame.event.get():
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False
        # Check for KEYDOWN event
        if event.type == pygame.KEYDOWN:
            keydown = True
            # If the Esc key is pressed, then exit the main loop
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.KEYUP:
            keyup = True
    # Get all the keys currently pressed
    pressedKeys = pygame.key.get_pressed()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    #update players
    players[0].update(pressedKeys, keydown, keyup, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)
    players[1].update(pressedKeys, keydown, keyup, pygame.K_a, pygame.K_d, pygame.K_w)

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Update the display
    pygame.display.flip()
    clock.tick(20)