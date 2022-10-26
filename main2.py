import pygame
import math
import configparser
import random
import time

from stick_men import * #import classes and functions
from stick_men_func import *

pygame.init()

#create and init a list of joysticks
joys = []
numJoysticks = getNumJoys()
initJoysticks(numJoysticks, joys)

useJoys = numJoysticks > 1

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

makePlatforms(platforms)

#group to hold bullets
bullets = pygame.sprite.Group()

#group to hold explosionPieces
explosionPieces = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False
        if useJoys: #this feels wrog here but how do i exit the game otherwise?
            if joys[0].get_button(JOY_BTN_PLAYER) and joys[0].get_button(JOY_BTN_COIN):
                running = False

    screen.fill((0,0, 0))

    updateAll(bullets, hats, players, platforms, explosionPieces, joys, useJoys)

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

    for piece in explosionPieces:

        piece.updateExplos(WIDTH, HEIGHT, platforms, players)
        piece.draw(screen)
    
    # Update the display
    pygame.display.flip()

    clock.tick(30)