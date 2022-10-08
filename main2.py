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
JUMP = 15
GRAVITY = 1
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
    
    def move(self):
        self.vel += self.acc

        x,y = self.rect.center

        x+= self.vel.x
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

    def move(self):
        self.acc.x = 0

        hits = pygame.sprite.spritecollide(player,platforms, False)
        
        if not hits:
            self.acc.y = GRAVITY
        
        pressed_keys = pygame.key.get_pressed()

        if hits and pressed_keys[pygame.K_UP]:
            self.vel.y = -JUMP
        
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = ACC
            

        self.acc.x += self.vel.x * FRIC
        
        self.vel += self.acc
        
        x,y = self.rect.center
        
        x += int(self.vel.x + 0.5 * self.acc.x) #take integer b/c had some trouble with stopping
        y += self.vel.y + 0.5 * self.acc.y
        
        self.rect.center = (x,y)

class Platform(Sprite):
    def __init__ (self, x, y, w, h, xVel = 0, yVel = 0):
        super(Platform, self).__init__("images/platform.png", x, y, xVel, yVel)
        self.rect.w = w
        self.rect.h = h

        self.surf = pygame.transform.scale(self.surf, (self.rect.width, self.rect.height))
def checkCollision(player, platforms):
    "Deal with player hitting stuff"

    hits = pygame.sprite.spritecollide(player,platforms, False)

    if hits:

        hit_plat = hits[len(hits)-1] #this way we take the last hit plat

        if player.vel.y > 0:
            player.rect.bottom = hit_plat.rect.top+1
        if player.vel.y < 0:
            player.rect.top = hit_plat.rect.bottom
        

        player.vel.y = hit_plat.vel.y
        player.acc.y = hit_plat.acc.y

        player.rect.x += hit_plat.vel.x
          
player = Player(500, 100)

platforms = pygame.sprite.Group()
platforms.add(Platform(200, 500, 500, 10, 0, 0))
platforms.add(Platform(200, 470, 300, 10, 10, 0))

running = True
while running:
    for event in pygame.event.get():
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,100))

    player.move()

    for platform in platforms:
        platform.move()

    checkCollision(player, platforms)

    player.draw()

    for platform in platforms:
        platform.draw()
    
    # Update the display
    pygame.display.flip()

    clock.tick(20)