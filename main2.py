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
GRAVITY = .5
ACC = 5
FRIC = -.15

class Sprite(pygame.sprite.Sprite):
    def __init__ (self, image, x, y, xVel = 0, yVel = 0, xAcc = 0, yAcc = 0):
        super(Sprite, self).__init__()
        self.surf = pygame.image.load(image)
        self.rect = self.surf.get_rect()
        
        #stores our position, velocity, acceleration        
        self.pos = vec((10, 360))
        self.rect.midbottom = self.pos

        self.vel = vect(xVel, yVel)
        self.acc = vect(xAcc, yAcc)

    def draw(self):
        if self.rect.top > HEIGHT:
            self.rect.bottom = 2

              
        screen.blit(self.surf, self.rect)
         
class Player(Sprite):
    def __init__ (self, x, y):
        super(Player, self).__init__("images/stick_man_running0.png", x, y, 0, 0, 0, GRAVITY)

    def move(self):
        self.acc = vect(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.rect.topleft += self.vel + 0.5 * self.acc

        self.draw()


class Platform(Sprite):
    def __init__ (self, x, y, w, h):
        super(Platform, self).__init__("images/platform.png", x, y)
        self.rect.w = w
        self.rect.h = h

        self.surf = pygame.transform.scale(self.surf, (self.rect.width, self.rect.height))

player = Player(500, 100)

platforms = pygame.sprite.Group()
platforms.add(Platform(200, 500, 500, 10))

running = True
while running:
    for event in pygame.event.get():
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False


    screen.fill((0,0,100))



    player.move()
    
    for platform in platforms:
        platform.draw()

    # Update the display
    pygame.display.flip()

    clock.tick(20)