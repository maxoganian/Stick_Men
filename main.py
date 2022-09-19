import pygame

numPlayers = 2

class Player(pygame.sprite.Sprite):
    
    def __init__(self, xStart, yStart):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/stick_man.png")
        self.rect = self.surf.get_rect(center = (xStart, yStart))
        self.yVel = 0
        self.xVel = 8
        self.acc = 0
        self.jumpCount = 40
        self.isJumping = False

    # Move the sprite based on user keypresses
    def update(self, pressedKeys, leftKey, rightKey, upKey):
        platform_hit_list = pygame.sprite.spritecollide(self, all_platforms, False)
        
        if pressedKeys[leftKey]:
            self.rect.move_ip(-self.xVel, 0)
        if pressedKeys[rightKey]:
            self.rect.move_ip(self.xVel, 0)
        if pressedKeys[upKey]:
            if self.isJumping == False and platform_hit_list != []:
                self.jumpCount = 0
                self.isJumping =True
        # Keep player on the screen
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0

        if platform_hit_list == []:
            self.acc = 2
        else:
            self.acc = -4
            self.yVel = 0

        if self.isJumping and self.jumpCount == 1:
            self.yVel = -20
        if self.jumpCount < 19:            
            self.jumpCount+=1
        else:
            self.isJumping = False

        self.yVel += self.acc
        self.rect.move_ip(0,self.yVel)

numPlatforms = 3
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
    platforms.append(Platform((i*400)+100, 500))

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
    
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == pygame.KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == pygame.K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == pygame.QUIT:
            running = False

    # Get all the keys currently pressed
    pressedKeys = pygame.key.get_pressed()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    #update players
    players[0].update(pressedKeys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)
    players[1].update(pressedKeys, pygame.K_a, pygame.K_d, pygame.K_w)

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Update the display
    pygame.display.flip()
    clock.tick(20)