import pygame
import math
import configparser
import random
import time

pygame.init()

vect = pygame.math.Vector2 #2 for two dimensional

clock = pygame.time.Clock()

#game window width and height
WIDTH = 1000
HEIGHT = 600

# Create the screen object
# The size is determined by the constant WIDTH and HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Constants will be from config in game
JUMP = 10
GRAVITY = .5
ACC = 3
FRIC = -.15

class Sprite(pygame.sprite.Sprite):
    def __init__ (self, image, x, y, xVel = 0, yVel = 0, xAcc = 0, yAcc = 0):
        super(Sprite, self).__init__()
        self.surf = pygame.image.load(image)
        self.rect = self.surf.get_rect()
        
        #stores our position, velocity, acceleration        
        self.rect.center = (x,y)

        self.vel = vect(xVel, yVel)
        self.acc = vect(xAcc, yAcc)
    
    def move_x(self):
        self.vel.x += self.acc.x

        x,y = self.rect.center

        x+= self.vel.x
        
        self.rect.center = (x,y)
    def move_y(self):
        self.vel.y += self.acc.y

        x,y = self.rect.center

        y+= self.vel.y
        
        self.rect.center = (x,y)
    def draw(self):
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT       
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        
        screen.blit(self.surf, self.rect)
         
class Player(Sprite):
    def __init__ (self, x, y):
        super(Player, self).__init__("images/stick_man_running0.png", x, y, 0, 0, 0, GRAVITY)

        #make image background transperent
        #self.surf.convert()
        #self.surf.set_colorkey((0, 0, 0))

    def move_x(self):
        self.acc.x = 0

        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = ACC
            
        self.acc.x += self.vel.x * FRIC
        
        self.vel.x += self.acc.x
        
        x,y = self.rect.center
        
        x += int(self.vel.x + 0.5 * self.acc.x) #take integer b/c had some trouble with stopping
                
        self.rect.center = (x,y)
    
    def move_y(self):
        
        hits = pygame.sprite.spritecollide(player,platforms, False)
        
        if not hits:
            self.acc.y = GRAVITY

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0,2)
            if pygame.sprite.spritecollide(player,platforms, False): 
                self.vel.y = -JUMP
        
        self.vel.y += self.acc.y
        
        x,y = self.rect.center

        y += self.vel.y + 0.5 * self.acc.y

        self.rect.center = (x,y)

class Platform(Sprite):
    def __init__ (self, x, y, w, h, xVel = 0, yVel = 0):
        super(Platform, self).__init__("images/platform.png", x, y, xVel, yVel)
        self.rect.w = w
        self.rect.h = h

        self.surf = pygame.transform.scale(self.surf, (self.rect.width, self.rect.height))
def moveAll(player, platforms):
    "Deal with player hitting stuff"

    #move x first to simplify detection
    for p in platforms:
        p.move_x()
    player.move_x()


    hits = pygame.sprite.spritecollide(player,platforms, False)
    
    if hits:
        hit_plat = hits[len(hits)-1] #this way we take the last hit plat
        #all this keeps the player out of platforms
        #its complicated because platforms move too
        
        if player.vel.x > 0: #if player is moving right
            #if the platform is still or moving left, then we are aproaching from the left    
            if hit_plat.vel.x <= 0: 
                player.rect.right = hit_plat.rect.left
            else: #otherwise we are aproaching from the right
                player.rect.right = hit_plat.rect.left
        
        #else if the player is moving left
        elif player.vel.x < 0:
            if hit_plat.vel.x >= 0: #same thing but flipped (the plat is moving right or still)
                player.rect.left = hit_plat.rect.right
            else:
                player.rect.left = hit_plat.rect.right
       
        #otherwise player is still and plats hit the player
        else:
            if hit_plat.vel.x < 0:
                player.rect.right = hit_plat.rect.left
            elif hit_plat.vel.x > 0:
                player.rect.left = hit_plat.rect.right

        # #if the player lands ontop of a moving platform it moves with the plat
        # player.rect.x += hit_plat.vel.x
    
    #move y second
    for p in platforms:
        p.move_y()
    player.move_y()

    hits = pygame.sprite.spritecollide(player,platforms, False)
    
    if hits:
        hit_plat = hits[len(hits)-1] #this way we take the last hit plat
        
        if player.vel.y > 0:
            player.rect.bottom = hit_plat.rect.top
        elif player.vel.x < 0:
            player.rect.top = hit_plat.rect.bottom
        else:
            if hit_plat.vel.x < 0:
                player.rect.right = hit_plat.rect.left
            elif hit_plat.vel.x > 0:
                player.rect.left = hit_plat.rect.right
        player.vel.y = hit_plat.vel.y

player = Player(500, 100)

platforms = pygame.sprite.Group()
platforms.add(Platform(200, 500, 500, 10, 0, 0))
platforms.add(Platform(200, 470, 300, 10, -10, 0))

running = True
while running:
    for event in pygame.event.get():
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,100))

    moveAll(player, platforms)

    player.draw()

    for platform in platforms:
        platform.draw()
    
    # Update the display
    pygame.display.flip()

    clock.tick(20)