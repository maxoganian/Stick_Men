import pygame
import configparser

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

class Player(Sprite):
    def __init__ (self, x, y, id):
        super(Player, self).__init__("images/stick_man_running0.png", x, y, 0, 0, 0, GRAVITY)

        self.id = id #should be 0 through number of players

        self.shotCounter = 0 #used so bullets can only go so often

        self.kills = 0 #stores the amount of kills the player has

        #make image background transperent
        # self.surf.convert()
        # self.surf.set_colorkey((0, 0, 0))

    def drawKillsAndShotRect(self, screen, hat):
        "Draws a rectangle to show how long until the next shot, and the kills the player has"
        #we pass in hat so the kils move with the hat, and the hat doesn't cover them
        if self.isAlive:
            shot_rect = pygame.Rect(hat.rect.x, hat.rect.y - 5, SHOT_TIME - self.shotCounter, 2)
            shot_rect.center = (hat.rect.x + hat.rect.width/2, hat.rect.y - 5)

            pygame.draw.rect(screen, (255,255,255), shot_rect)

            #use this block to write kills above the players
            text_surf = font.render(str(self.kills), True, (255,255,255))
            text_rect = text_surf.get_rect(center=((hat.rect.x + (hat.rect.width/2)), hat.rect.y-15))
            
            #write the kills to the screen
            screen.blit(text_surf, text_rect)

    def move_x(self, pressed_keys, platforms):
        self.acc.x = 0 #make sure player stops with no keys
        
        #move off key pressed
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = ACC
            
        self.acc.x += self.vel.x * FRIC #slows player to imitate friction
        
        self.vel.x += self.acc.x  #basic motion
        
        x,y = self.rect.center #split center into usable pieces
        
        x += int(self.vel.x + 0.5 * self.acc.x**2) #equation for motion - take integer b/c had some trouble with stopping
                
        self.rect.center = (x,y) #set our position

        hits = hitGroup(self, platforms)
        
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

    def move_y(self, pressed_keys, platforms):

        hits = hitGroup(self, platforms)
        
        if not hits:
            self.acc.y = GRAVITY

        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0,11)
            if hitGroup(self, platforms): 
                self.vel.y = -JUMP
            self.rect.move_ip(0,-11)
        
        self.vel.y += self.acc.y
             
        x,y = self.rect.center

        y += self.vel.y + 0.5 * self.acc.y**2
       
        self.rect.center = (x,y)

        hits = hitGroup(self, platforms)
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
    def __init__ (self, x, y, w, h, xVel = 0, yVel = 0):
        super(Platform, self).__init__("images/platform.png", x, y, xVel, yVel)
        
        self.rect.w = w
        self.rect.h = h

        self.surf = pygame.transform.scale(self.surf, (self.rect.width, self.rect.height)) #make the image match the rect

        self.rect.center = (x,y) #the scaling seems to move the entire rect, this resets it

def hitGroup(sprite1, spriteGroup, removeGroup = False):
    "Returns a list of all the items in spriteGroup sprite1 hits"
    return pygame.sprite.spritecollide(sprite1, spriteGroup, removeGroup)

def createBullets(player, bullets, pressed_keys):
    #ony fire after a certain amount of time has passed
    if pressed_keys[pygame.K_SPACE] and player.shotCounter > SHOT_TIME:
        bullets.add(Bullet(player))
        player.shotCounter = 0
    
    player.shotCounter+=1

def checkForBulletPlayer(player, players, bullets):
    "If bullet hits player kill player"
    #kill player:
    hits_player = hitGroup(player, bullets)
    
    if hits_player:
        hit_bullet = hits_player[0]
        if hit_bullet.playerId != player.id: #make sure the bullet isnt hitting its own player
            players[hit_bullet.playerId].kills += 1 #increase payer that shot the bullets kill count

            hit_bullet.kill() #remove bullet
            
            player.isAlive = False #kill player

def checkForBulletCollis(bullets, platforms):
    "If bullet hits platform or bullet hits bullet, kill bullet"
    pygame.sprite.groupcollide(bullets, platforms, True, False, collided=collision_check)

    pygame.sprite.groupcollide(bullets, bullets, True, True, collided=collision_check)

def collision_check(sprite1, sprite2):
    "Return True if sprites are colliding, unless it's the same sprite."
    #works with - pygame.sprite.groupcollide(explosionPieces, platforms, True, False, collided=collision_check) 
    if sprite1 is not sprite2:
        return sprite1.rect.colliderect(sprite2.rect)
    else:  # Both sprites are the same object, so return False.
        return False

def updateAll(bullets, hats, players, platforms):
    "Update all sprites"    
    pressed_keys = pygame.key.get_pressed()

    # have to deal with one dimension at a time b/c
    # collision detection consequences are easier that way

    #move x first to simplify detection
    for p in platforms:
        p.move_x() 
    
    for player in players:
        if player.isAlive:
            player.move_x(pressed_keys, platforms)

    #move y second
    for p in platforms:
        p.move_y()

    for player in players:
        if player.isAlive:
            checkForBulletPlayer(player, players, bullets)#pass players to increase kill counter im not a fan of this method

            hats[player.id].update(player) #putting hat movement here makes the hat follow the player, b/c the payer moves
                                           #after the hat

            player.move_y(pressed_keys, platforms)
            
            if player.vel.y < 0: #if the player is moving up we want the hat glued to their head
                hats[player.id].update(player)

            createBullets(player, bullets, pressed_keys)#creates bullets on key presss

        if pressed_keys[pygame.K_r]: #realive players
            player.isAlive = True

    for bullet in bullets:
        bullet.move()

    checkForBulletCollis(bullets, platforms)


    