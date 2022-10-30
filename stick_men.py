import pygame
import configparser
import random

#Vect only used to organize the x and y
vect = pygame.math.Vector2 #2 for two dimensional

#init config parser
config = configparser.ConfigParser()
config.read("levels.conf")

#Constants from config 
JUMP = float(config['DEFAULTS']['JUMP'])
GRAVITY = float(config['DEFAULTS']['GRAVITY'])
ACC = float(config['DEFAULTS']['ACC'])
FRIC = float(config['DEFAULTS']['FRIC'])

MAXVEL = float(config['DEFAULTS']['MAXVEL'])

BULLET_TIME = float(config['DEFAULTS']['BULLET_TIME'])
BULLET_SPEED = float(config['DEFAULTS']['BULLET_SPEED'])
SHOT_TIME = float(config['DEFAULTS']['SHOT_TIME'])
EXPLOSION_SIZE = float(config['DEFAULTS']['EXPLOSION_SIZE'])

#pygame init for joysticks and font
pygame.init()

#have to init font for words
font = pygame.font.SysFont(None, 25)

class Sprite(pygame.sprite.Sprite):
    def __init__ (self, image, x, y, xVel = 0, yVel = 0, xAcc = 0, yAcc = 0):
        super(Sprite, self).__init__()
        self.surf = pygame.image.load(image)
        self.rect = self.surf.get_rect()
        
        #stores our position, velocity, acceleration        
        self.rect.center = (x,y)#Rect gives a grat built in way to hold position

        self.vel = vect(xVel, yVel)
        self.acc = vect(xAcc, yAcc)

        self.isAlive = True

        #make image background transperent
        # self.surf.convert()
        # self.surf.set_colorkey((0, 0, 0))

    def move_x(self):
        x,y = self.rect.center
        
        x+= self.vel.x
        
        self.rect.center = (x,y)
   
    def move_y(self):
        x,y = self.rect.center

        y+= self.vel.y
        
        self.rect.center = (x,y)
    
    def move(self):
        self.move_x()
        self.move_y()
    
    def keepBelowVel(self):
        if self.vel.x > MAXVEL:
            self.vel.x = MAXVEL
        if self.vel.y > MAXVEL:
            self.vel.y = MAXVEL

    def update(self, width, height):
        if self.rect.top > height:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = height
        if self.rect.left > width:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = width
        
        self.keepBelowVel()
    
    def draw(self, screen):
        if self.isAlive:
            screen.blit(self.surf, self.rect)


    def hitGroup(self, spriteGroup, removeGroup = False):
        "Returns a list of all the items in spriteGroup sprite1 hits"
        return pygame.sprite.spritecollide(self, spriteGroup, removeGroup)

class Player(Sprite):
    def __init__ (self, x, y, id):
        super(Player, self).__init__("images/stick_man_running0.png", x, y, 0, 0, 0, GRAVITY)

        self.id = id #should be 0 through number of players

        self.shotCounter = 0 #used so bullets can only go so often

        self.kills = 0 #stores the amount of kills the player has

        self.controls = [None]*4 #init controls will use in move functions, this stores joystick or key controls

        self.canJump = False #if we are standing on something we can jump

    def drawKillsAndShotRect(self, screen, hat):
        "Draws a rectangle to show how long until the next shot, and the kills the player has"
        #we pass in hat so the kills move with the hat, and the hat doesn't cover them
        if self.isAlive:
            shot_rect = pygame.Rect(hat.rect.x, hat.rect.y - 5, SHOT_TIME - self.shotCounter, 2)
            shot_rect.center = (hat.rect.x + hat.rect.width/2, hat.rect.y - 5)

            if SHOT_TIME -self.shotCounter > 0: #in linux the rect will accept a - width but not in windows??
                pygame.draw.rect(screen, (255,255,255), shot_rect)

            #use this block to write kills above the players
            text_surf = font.render(str(self.kills), True, (255,255,255))
            text_rect = text_surf.get_rect(center=((hat.rect.x + (hat.rect.width/2)), hat.rect.y-15))
            
            #write the kills to the screen
            screen.blit(text_surf, text_rect)
    
    def move_x(self, platforms, controls):
        self.acc.x = 0 #make sure player stops with no controls

        #move off of key presses
        if controls[1]:
            self.acc.x = -ACC
        if controls[2]:
            self.acc.x = ACC
            
        self.acc.x += self.vel.x * FRIC #slows player to imitate friction
        
        self.vel.x += self.acc.x  #basic motion
        
        x,y = self.rect.center #split center into usable pieces
        
        x += int(self.vel.x + 0.5 * self.acc.x**2) #equation for motion - take integer b/c had some trouble with stopping
                
        self.rect.center = (x,y) #set our position

        hits = self.hitGroup(platforms)
        
        if hits:
            hit_plat = hits[0]
            
            #now decide what side of the platform were on and adjust
            #this method fails if the player moves to quickly into a skinny platform
            #this is rare, but is why we run at 30fps

            if (self.rect.left + self.rect.width/2) > (hit_plat.rect.left + hit_plat.rect.width/2):#we are on the right
                self.rect.left = hit_plat.rect.right
            else:
                self.rect.right = hit_plat.rect.left  

            self.vel.x = hit_plat.vel.x # make sure we move with the platforn
    def checkForJump(self, platforms):
        "This is used so we can test jumping before the plat moves"
        self.canJump = False
        
        self.rect.move_ip(0,1)
        
        if self.hitGroup(platforms):
            self.canJump = True
        
        self.rect.move_ip(0,-1)

    def move_y(self, platforms, controls):

        hits = self.hitGroup(platforms)
        
        if not hits:
            self.acc.y = GRAVITY

        if controls[0] and self.canJump:
            self.vel.y = -JUMP

        self.vel.y += self.acc.y
             
        x,y = self.rect.center

        y += self.vel.y + 0.5 * self.acc.y**2
       
        self.rect.center = (x,y)

        hits = self.hitGroup(platforms)
        if hits:

            hit_plat = hits[0] #take the plat we are on
            
            #same system as horizontal movement
            if (self.rect.top + self.rect.h/2) < (hit_plat.rect.top + hit_plat.rect.h/2):#we are on the bottom
                self.rect.bottom = hit_plat.rect.top
            else:
                self.rect.top = hit_plat.rect.bottom

            self.vel.y = hit_plat.vel.y

class Hat(Sprite):
    def __init__ (self, player):
        x,y = player.rect.midtop
        super(Hat, self).__init__("images/hat" + str(player.id+1) + ".png", x, y, player.vel.x, player.vel.y, player.acc.x, player.acc.y) 

    def update(self,player):
        self.rect.center = (player.rect.midtop) #keeps hat on player
        self.rect.y += 3 #move down the hat
        self.isAlive = player.isAlive #so hat vanishes when the player does

class Bullet(Sprite):
    def __init__ (self, player):
        x,y = player.rect.center
        #set bullet speed based of player direction
        if player.vel.x >= 0:
            self.speed = BULLET_SPEED
        else:
            self.speed = -BULLET_SPEED

        super(Bullet, self).__init__("images/hat" + str(player.id+1) + ".png", x, y, self.speed)

        self.counter = 0 #used so bullet will timeout

        self.playerId = player.id #used so bullets can only kill other players

    def updateBullet(self, w, h):
        self.update(w, h)
        self.counter+=1
        if self.counter > BULLET_TIME:
            self.kill()

class Platform(Sprite):
    def __init__ (self, platform):
        
        #split platform into pieces we need
        #first we split it to tuples then to usable variables that we need

        if len(platform) == 5:#used to see if the platform has the variables for moving
            start, rect, image, end, speed = platform
            
            endX, endY = end
            
            self.endX = endX*10
            self.endY = endY*10

            self.isMoving = True

        else:#otherwise dont split end and speed
            start, rect, image = platform
            speed = (0,0) #if not moving our speed is 0

            self.isMoving = False

        #then tuples into usable variables
        w, h = rect
        xVel, yVel = speed

        x,y = start
        
        self.startX = x*10
        self.startY = y*10

        super(Platform, self).__init__("images/platform.png", self.startX, self.startY, xVel, yVel)
        
        self.rect.w = w*10
        self.rect.h = h*10

        self.surf = pygame.transform.scale(self.surf, (self.rect.width, self.rect.height)) #make the image match the rect

        self.rect.center = (self.startX,self.startY) #the scaling seems to move the entire rect, this resets it

    def move_plat_x(self):
        self.move_x()
        if self.isMoving: #check if its moving so we dont try to call variables that dotn exist
            #these create the "bouncing" platforms
            if (self.rect.x + self.rect.w/2) > self.endX:
                self.vel.x = -self.vel.x

            if (self.rect.x + self.rect.w/2) < self.startX:
                self.vel.x = -self.vel.x

    def move_plat_y(self):
        self.move_y()
        if self.isMoving: #check if its moving so we dont try to call variables that dotn exist
            #these create the "bouncing" platforms
            if (self.rect.y + self.rect.height/2) > self.endY:
                self.vel.y = -self.vel.y

            if (self.rect.y + self.rect.height/2) < self.startY:
                self.vel.y = -self.vel.y

class ExplosionPiece(Sprite):
    def __init__(self, player):
        #our exposion is just a random number of these pieces sent out at random velocities for a set time
        #Rn we just use the hat images cause im lazy
        x,y = player.rect.center #split center so it can be input into super

        #random velocities for the piece
        xVel = random.randint(-6, 6)
        yVel = random.randint(-6, 6)

        super(ExplosionPiece, self).__init__("images/piece"+str(player.id)+".png", x, y, xVel, yVel)

        self.counter = 0

    def updateExplos(self, w, h, platforms, players):
        self.update(w, h)
        #kill piece if its time runs out or it hits a plat
        # i know it seems weird to let them go through players, but if the players are ontop of each other
        #we still want an explosion
        if self.counter > EXPLOSION_SIZE or self.hitGroup(platforms): 
            self.kill()
        self.counter+=1