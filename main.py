import pygame

numPlayers = 2
class Player(pygame.sprite.Sprite):

    def __init__(self, xStart, yStart):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/stick_man1.png")
        self.rect = self.surf.get_rect(center=(xStart, yStart))

        self.yVel = 0
        self.xVel = 0
        self.isAlive = True

        self.jumpHeight = 20
        self.gravPower = 2
        self.isJumping = False

        self.speed = 10
        self.dir = "right"

        self.shotCounter = 0
        self.kills = 0

    # Move the sprite based on user keypresses
    def update(self, pressedKeys, keys):

        leftKey = keys[0]
        rightKey = keys[1]
        upKey = keys[2]

        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)

        self.xVel = 0
        self.calc_grav()

        #if keydown:
        if pressedKeys[leftKey]:
            self.xVel = -self.speed
        if pressedKeys[rightKey]:
            self.xVel = self.speed

        if pressedKeys[upKey]:
            # move down a bit and see if there is a platform below us.
            self.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(
                self, platforms, False)
            self.rect.y -= 2

            # If it is ok to jump, set our speed upwards
            if platform_hit_list != []:
                self.yVel = -self.jumpHeight
 
        # Move left/right
        self.rect.move_ip(self.xVel, 0)

        # See if we hit anything
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)

        for platform in platform_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.xVel > 0:
                self.rect.right = platform.rect.left
            elif self.xVel < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = platform.rect.right

        #what direction are we moving?
        if self.xVel < 0:
            self.dir = "left"
        elif self.xVel > 0:
            self.dir = "right"

        #move up/down
        self.rect.move_ip(0, self.yVel)

        # Check and see if we hit anything
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)

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
            self.rect.left = WIDTH - 2
            #add a little height so we can move smoothly from platforms on either side
            self.rect.y -= 5
        if self.rect.left > WIDTH:
            self.rect.right = 2
            self.rect.y -= 5
        #for now fall to top, maybe die later
        if self.rect.top > HEIGHT:
            self.rect.bottom = 2
        #also let jump through ceiling, w/ current map not really aplicable
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT - 2
    
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.yVel == 0:
            self.yVel = 1
        else:
            self.yVel += self.gravPower


bullets = pygame.sprite.Group()


class Bullet(pygame.sprite.Sprite):

    def __init__(self, center, dir, playerNumber):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load("images/bullet" + str(playerNum+1) + ".png")
        self.rect = self.surf.get_rect(center=center)
        self.shotCounter = 0
        self.dir = dir
        self.speed = 20
        self.playerId = playerNumber

    def shoot(self):
        if self.dir == "left":
            self.rect.move_ip(-self.speed, 0)
        elif self.dir == "right":
            self.rect.move_ip(self.speed, 0)
        if self.rect.left > WIDTH:
            self.rect.right = 2
        if self.rect.right < 0:
            self.rect.left = WIDTH - 2

def collision_check(sprite1, sprite2):
    """Return True if sprites are colliding, unless it's the same sprite."""
    if sprite1 is not sprite2:
        return sprite1.rect.colliderect(sprite2.rect)
    else:  # Both sprites are the same object, so return False.
        return False


numPlatforms = 8
class Platform(pygame.sprite.Sprite):

    def __init__(self, xPos, yPos):
        super(Platform, self).__init__()
        self.surf = pygame.image.load("images/platform.png")
        self.rect = self.surf.get_rect(center=(xPos, yPos))


#game window width and height
WIDTH = 1000
HEIGHT = 600

# Create the screen object
# The size is determined by the constant WIDTH and HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#create players
players = []

for i in range(numPlayers):
    players.append(Player((i * 400) + 100, 400))

platforms = []
for i in range(numPlatforms):
    if i < 3:
        platforms.append(Platform((i * 400) + 100, 500))
    elif i < 5:
        platforms.append(Platform(((i - 3) * 400) + 300, 400))
    elif i < 9:
        platforms.append(Platform(((i - 5) * 400) + 100, 300))

# Setup the clock
clock = pygame.time.Clock()

#set up the font
pygame.font.init()

font = pygame.font.SysFont(None, 25)

running = True
while running:

    # for loop through the event queue
    for event in pygame.event.get():
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False
        # Check for KEYDOWN event
        if event.type == pygame.KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == pygame.K_ESCAPE:
                running = False
            #Restart if r key is pressed
            if event.key == pygame.K_r:
                for player in players:
                    player.isAlive = True

    # Get all the keys currently pressed
    pressedKeys = pygame.key.get_pressed()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    #deal with bullets, i know player movement should be here (tbf)
    for playerNum, player in enumerate(players):
        keys = []
        if player.isAlive:
            if playerNum == 0:
                keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_SPACE]
            else:
                keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_g]

            #make the image the right way, this is all our animation rn
            if player.dir == "right" and player.xVel != 0:
                player.surf = pygame.image.load("images/stick_man_right" + str(playerNum+1) + ".png")
            elif player.dir == "left" and player.xVel != 0:
                player.surf = pygame.image.load("images/stick_man_left" + str(playerNum+1) + ".png")
            else:
                player.surf = pygame.image.load("images/stick_man" + str(playerNum+1) + ".png")

            if pressedKeys[keys[3]] and player.shotCounter > 20:
                if player.dir == "left":
                    bullets.add(
                        Bullet((player.rect.x, player.rect.y + (player.rect.height / 2)), player.dir, playerNum))
                else:
                    bullets.add(
                        Bullet((player.rect.right, player.rect.y + (player.rect.height / 2)), player.dir, playerNum))

                player.shotCounter = 0

            player.shotCounter += 1

            #deal with bullet collisions
            for i, bullet in enumerate(bullets):
                #kill player, I cant decide if I want people to be able to kill themselves, will take gameplay testing
                if pygame.sprite.collide_rect(player, bullet) and playerNum != bullet.playerId:
                    player.isAlive = False
                    players[bullet.playerId].kills+=1
                    bullet.kill()

            #if bullets hit remove them tbh this is copied code probably could do other collison checks
            #with this, platforms?
            pygame.sprite.groupcollide(bullets, bullets, True, True, collided=collision_check)

            #update players
            player.update(pressedKeys, keys)

            #use this block to write kills above the players
            text_surf = font.render(str(player.kills), True, (255,255,255))
            text_rect = text_surf.get_rect(center=((player.rect.x + (player.rect.width/2)), player.rect.y-15))
            
            #write the kills to the screen
            screen.blit(text_surf, text_rect)

        #print kills
        #use this to print kills at top of screen
        # text = str(player.kills)
        # if playerNum == 0:
        #     color = (255,0,0)
        #     text += " :"
        # else:
        #     color = (0,0,255)

        # text_surf = font.render((text), True, color)
        # text_rect = text_surf.get_rect(center=(((WIDTH/2)+((playerNum+1)*20)), 20))
        ##write the kills to the screen
        #screen.blit(text_surf, text_rect)
        

    # Draw all sprites
    for platform in platforms:
        screen.blit(platform.surf, platform.rect)

    for player in players:
        if player.isAlive:
            screen.blit(player.surf, player.rect)

    for bullet in bullets:
        bullet.shoot()
        #keep bullets on screen and out of platforms
        if pygame.sprite.spritecollide(bullet, platforms, False) or bullet.shotCounter > 40:
            bullet.kill()
        bullet.shotCounter+=1
        screen.blit(bullet.surf, bullet.rect)

    # Update the display
    pygame.display.flip()

    clock.tick(20)
