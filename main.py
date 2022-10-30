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
players.append(Player(400, 100, 2))
players.append(Player(600, 100, 3))

for player in players:
    hats.append(Hat(player))

platforms = pygame.sprite.Group()

makePlatforms(platforms)

#group to hold bullets
bullets = pygame.sprite.Group()

#group to hold explosionPieces
explosionPieces = pygame.sprite.Group()

state = "start"

running = True
while running:
    #controls is a two layer array, one for player1 one for player2. These layers are 5 long, holding boolean values
    #for jumping moving ect
    #reset controls to false
    allControls = [False]*4
    for player in players:
        allControls[player.id] = getControls(player, joys, useJoys) 


    for event in pygame.event.get():
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False
        if useJoys: #this feels wrog here but how do i exit the game otherwise?
            if allControls[0]['coin'] and allControls[0]['player']:
                running = False

    if state == "start":
        screen.blit(pygame.image.load("images/start_background.png"), (0,0))
        if allControls[0]['coin']: #on the coin press for now start to our deathmatch
            state = "deathmatch"

    if state == "deathmatch":
        screen.fill((0,0,0))

        updateAll(bullets, hats, players, platforms, explosionPieces, allControls, WIDTH, HEIGHT)

        drawAll(screen, bullets, players, hats, platforms, explosionPieces)

    # Update the display
    pygame.display.flip()

    clock.tick(30)