import pygame
import math
import configparser
import random

# load config info
config = configparser.ConfigParser()
config.read("levels.conf")

numPlayers = 2
class Player(pygame.sprite.Sprite):

    def __init__(self, xStart, yStart):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/stick_man.png")
        self.rect = self.surf.get_rect(center=(xStart, yStart))

        self.yVel = 0
        self.xVel = 0
        self.isAlive = True

        self.jumpHeight = int(config['DEFAULTS']['player_jump_velocity'])
        self.gravPower = int(config['DEFAULTS']['gravity_acceleration'])
        self.isJumping = False


        self.speed = int(config['DEFAULTS']['player_speed'])
        self.dir = "right"

        self.running_imgs = []
        for i in range(2):
            self.running_imgs.append(pygame.image.load("images/stick_man_running"+str(i)+".png"))
        self.runningCounter = 0
        
        #self.running_imgs[0] = pygame.image.load("images/stick_man_running4.png")


        self.shotCounter = 0
        self.shotTime = 20
        self.kills = 0


    # Move the sprite based on user keypresses
    def update(self, pressedKeys, keys, joys):

        leftKey = keys[0]
        rightKey = keys[1]
        upKey = keys[2]

        leftJoy = False
        rightJoy = False
        upJoy = False

        if useJoysticks:   
            if joys[0] > .8:
                leftJoy = True
            elif joys[0] < -.8:
                rightJoy = True
            if joys[1] > .8:
                upJoy = True

        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)

        self.xVel = 0
        self.calc_grav()

        if pressedKeys[leftKey] or leftJoy:
            self.xVel = -self.speed
        if pressedKeys[rightKey] or rightJoy:
            self.xVel = self.speed

        if pressedKeys[upKey] or upJoy:
            # move down a bit and see if there is a platform below us.
            self.rect.y += 6
            platform_hit_list = pygame.sprite.spritecollide(
                self, platforms, False)
            self.rect.y -= 6

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

        #make the image the right way, this is all our animation rn
        if self.xVel != 0:
            if self.dir == "right":
                self.surf = pygame.transform.flip(self.running_imgs[self.runningCounter], True, False)
            elif self.dir == "left":
                self.surf = self.running_imgs[self.runningCounter]
            self.runningCounter+=1
            if self.runningCounter >= len(self.running_imgs):
                self.runningCounter = 0
        else:
            self.surf = pygame.image.load("images/stick_man.png")

        #keep the falling speed in check so we dont break the game
        if self.yVel > int(config['DEFAULTS']['maxFallSpeed']):
            self.yVel = int(config['DEFAULTS']['maxFallSpeed'])

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
    
        shot_rect = pygame.Rect(self.rect.x, self.rect.y - 5, self.shotTime - self.shotCounter, 2)
        shot_rect.center = (self.rect.x + self.rect.width/2, self.rect.y - 5)

        pygame.draw.rect(screen, (255,255,255), shot_rect)


    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.yVel == 0:
            self.yVel = 1
        else:
            self.yVel += self.gravPower


class Hat(pygame.sprite.Sprite):
    def __init__(self, player, playerNum):
        super(Hat, self).__init__()
        self.surf = pygame.image.load("images/hat" + str(playerNum+1) + ".png")
        self.rect = self.surf.get_rect(center=(player.rect.x + player.rect.width/2, player.rect.y-20))
        self.isAlive = player.isAlive

    def update(self, player):
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.isAlive = player.isAlive
  
bullets = pygame.sprite.Group()
 
class Bullet(pygame.sprite.Sprite):

    def __init__(self, center, dir, playerNum):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load("images/hat" + str(playerNum+1) + ".png")
        self.rect = self.surf.get_rect(center=center)
        self.shotCounter = 0
        self.dir = dir
        self.speed = 20
        self.playerId = playerNum

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



#numPlatforms = 8
class Platform(pygame.sprite.Sprite):
    def __init__(self, platform_input, type):
        super(Platform, self).__init__()
        
        #spilt our output from the cofig into usable pieces
        if type == "norm":
            start, rect, image = platform_input
        elif type == "moving":
            start, rect, image, end, speed = platform_input
            endX, endY = end 
        
        if image is None:
            image = "platform"

        self.surf = pygame.image.load("images/" + image + ".png")
        self.rect = self.surf.get_rect()
        self.type = type
      
        startX, startY = start
        width, height = rect

        self.startX = startX*10
        self.startY = startY*10
        # self.isGoingToEnd = True
        
        self.rect.width = width*10
        self.rect.height = height*10
        self.rect.center = (startX*10, startY*10)

        self.surf = pygame.transform.scale(self.surf, (self.rect.width, self.rect.height))
        
        if type == "moving":   
            self.endX = endX*10
            self.endY = endY*10

            #do math for moving plats 
            deltaX = (self.endX - self.startX)
            deltaY = (self.endY - self.startY)
            
            radians = math.atan2(deltaY, deltaX)

            #decide if we use the x or y delta to check for arrival at distance
            #use the larger of the two
            useXforDist = abs(deltaX) > abs(deltaY)
            #print("stepInX: ", stepInX)
            travelDist = deltaX if useXforDist else deltaY

            self.stepsTillEnd = int(travelDist/speed)
            self.origStepsTillEnd = self.stepsTillEnd

            self.yVel = speed * math.sin(radians)
            self.xVel = speed * math.cos(radians)
      
    def update(self):
        
        if(self.type == "moving"):
            if self.stepsTillEnd > 0:
                self.rect.move_ip(self.xVel, self.yVel)
            else:
                self.rect.move_ip(-self.xVel, -self.yVel)

            if self.stepsTillEnd < (-self.origStepsTillEnd):
                self.stepsTillEnd = self.origStepsTillEnd
            self.stepsTillEnd-=1
#game window width and height
WIDTH = 1000
HEIGHT = 600

# Create the screen object
# The size is determined by the constant WIDTH and HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#create and hats
players = []
hats = []

#for i in range(numPlayers):
players.append(Player(300, 50))
players.append(Player(700, 50))

    
for i, player in enumerate(players):
    hats.append(Hat(player, i))

platforms = pygame.sprite.Group()
def makePlatforms():
    #levelNum = random.randint(0,(int(config['DEFAULTS']['num_levels'])-1))
    levelNum = 0
    level = 'LEVEL_' + str(levelNum)
    
    print(level)
    for platform in platforms:
        platform.kill()
    
    #first add statonary platforms then moving ones
    for i in range(int(config[level]['num_normal'])):
       norm_platform = eval(config[level + '.norm_platforms']['p'+str(i)])
       platforms.add(Platform(norm_platform, "norm"))
    
    #create moving platforms
    for i in range(int(config[level]['num_moving'])):
        platform = eval(config[level + '.moving_platforms']['p'+str(i)])
        platforms.add(Platform(platform, "moving"))

    print("platforms: " + str(platforms))

print("platforms: " + str(platforms))
makePlatforms()

print("platformsFINAL: " + str(platforms))

def drawSprites():
    # Draw all sprites
    for bullet in bullets:
        bullet.shoot()
        #keep bullets on screen and out of platforms
        if pygame.sprite.spritecollide(bullet, platforms, False) or bullet.shotCounter > 40:
            bullet.kill()
        bullet.shotCounter+=1
        screen.blit(bullet.surf, bullet.rect)

    for platform in platforms:
        platform.update()
        screen.blit(platform.surf, platform.rect)

    for player in players:
        if player.isAlive:
            screen.blit(player.surf, player.rect)
    
    for i, hat in enumerate(hats):
        hat.update(players[i])
        if hat.isAlive:
            screen.blit(hat.surf, hat.rect)

def updateSprites():
    #deal with bullets, i know player movement should be here (tbf)
    for playerNum, player in enumerate(players):
        keys = []
        joys = []
        
        if useJoysticks:
            j = joysticks[playerNum]
            joys = [j.get_axis(0), j.get_axis(1), j.get_button(JOY_BTN_CENTER)]
            #respawn player
            if j.get_button(JOY_BTN_PLAYER):
                player.isAlive = True

        if player.isAlive:
            if playerNum == 0:
                keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_SPACE]
            else:
                keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_g]

            if pressedKeys[keys[3]] and player.shotCounter > player.shotTime:
                bullets.add(Bullet((player.rect.x, player.rect.y + (player.rect.height / 2)), player.dir, playerNum))
                player.shotCounter = 0
            if useJoysticks:
                if joys[2] and player.shotCounter > player.shotTime:
                    bullets.add(Bullet((player.rect.x, player.rect.y + (player.rect.height / 2)), player.dir, playerNum))
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
            player.update(pressedKeys, keys, joys)

            #use this block to write kills above the players
            text_surf = font.render(str(player.kills), True, (255,255,255))
            text_rect = text_surf.get_rect(center=((player.rect.x + (player.rect.width/2)), player.rect.y-15))
            
            #write the kills to the screen
            screen.blit(text_surf, text_rect)
        

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

#init pygame, needed for joysticks
pygame.init()

# Setup the clock
clock = pygame.time.Clock()

#set up the font
pygame.font.init()

font = pygame.font.SysFont(None, 25)

# look for joysticks
numJoysticks = pygame.joystick.get_count()
print("Detected num Joysticks: ", numJoysticks)
useJoysticks = numJoysticks >= numPlayers
# init all the joysticks we have
joysticks = []
for i in range(numJoysticks):
    j = pygame.joystick.Joystick(i)
    j.init()
    joysticks.append(j)

# Joystick constants
JOY_BTN_NORTH = 3
JOY_BTN_SOUTH = 6    
JOY_BTN_EAST = 5     
JOY_BTN_WEST = 2    
JOY_BTN_CENTER = 4
JOY_BTN_COIN = 0
JOY_BTN_PLAYER = 1

state = "start"

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
            if event.key == pygame.K_t:
                makePlatforms()
            if event.key == pygame.K_c:
                state = "playing"
            if event.key == pygame.K_s:
                state = "start"
            
    if useJoysticks: 
        if joysticks[0].get_button(JOY_BTN_COIN) and joysticks[0].get_button(JOY_BTN_PLAYER):
            running = False

    # Get all the keys currently pressed
    pressedKeys = pygame.key.get_pressed()
    if state == "start":
        image = pygame.image.load("images/start_background.png")
        image_rect = image.get_rect()
        screen.blit(image, image_rect)

    elif state == "playing":
        # Fill the screen with black
        screen.fill((0, 0, 0))
        updateSprites() 
        drawSprites()
    
    # Update the display
    pygame.display.flip()

    clock.tick(20)