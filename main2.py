import pygame
import math
import configparser
import random
import time

from stick_men import * #import classes and functions

pygame.init()

vect = pygame.math.Vector2 #2 for two dimensional

clock = pygame.time.Clock()

#game window width and height
WIDTH = 1000
HEIGHT = 600

# Create the screen object
# The size is determined by the constant WIDTH and HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#hats and payers is a list because pg groups arent scriptable and players dont get popped
players = []
hats = []

players.append(Player(200, 100, 0))
players.append(Player(800, 100, 1))

for player in players:
    hats.append(Hat(player))

platforms = pygame.sprite.Group()
platforms.add(Platform(300, 500, 500, 10, 0, 0))
platforms.add(Platform(200, 470, 100, 10, 0, 0))
platforms.add(Platform(300, 300, 100, 10))

#group to hold bullets
bullets = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,100))

    updateAll(bullets, hats, players, platforms)


    for bullet in bullets:
        
        bullet.updateBullet(WIDTH, HEIGHT)
        bullet.draw(screen)

    for player in players:
        
        player.update(WIDTH, HEIGHT)
        player.draw(screen)
        
        hats[player.id].draw(screen)

        player.drawKillsAndShotRect(screen, hats[player.id])

    for platform in platforms:

        platform.update(WIDTH, HEIGHT)
        platform.draw(screen)
    
    # Update the display
    pygame.display.flip()

    clock.tick(30)