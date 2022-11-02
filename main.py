import pygame
import math
import configparser
import random
import time

from stick_men import * #import classes and functions
from stick_men_func import *
from selection_func import *

pygame.init()

PRESS_TIME = float(config['DEFAULTS']['PRESS_TIME'])

#have to init font for words
font = pygame.font.SysFont(None, 25)

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

#number of levels
NUM_LEVELS = float(config['DEFAULTS']['NUM_LEVELS'])

# Create the screen object
# The size is determined by the constant WIDTH and HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#hats and payers is a list because pg groups arent scriptable and players dont get popped
players = []
hats = []

platforms = pygame.sprite.Group()

#group to hold bullets
bullets = pygame.sprite.Group()

#group to hold explosionPieces
explosionPieces = pygame.sprite.Group()

state = "start"

#these two are used for the select screen
select_state = "player"
press_count = 0

#these globals will be chosen in the select menu
numPlayers = 2

modes = ["Deathmatch", "Team Deathmatch"]
modeIndex = 0

levelNum = 1

running = True
while running:
    #controls is a two layer array, one for player1 one for player2. These layers are 5 long, holding boolean values
    #for jumping moving ect
    #reset controls to false
    allControls = [False]*4

    for i in range(numPlayers):
        allControls[i] = getControls(i, joys, useJoys) 

    for event in pygame.event.get():
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False

    if state == "start":
        screen.blit(pygame.image.load("images/start_background.png"), (0,0))
        
        if allControls[0]['coin']: #on the coin press move to slection
            state = "selection"

        #if were at the start we can exit
        if allControls[0]['coin'] and allControls[0]['player']: 
            running = False

    if state == "selection":

        screen.blit(pygame.image.load("images/selection_background.png"), (0,0))

        if select_state == "player":
            if press_count > PRESS_TIME:
                #select between 2 or 4 players
                if allControls[0]['up'] and numPlayers < 4:
                    numPlayers+=1
                    press_count = 0
                
                elif allControls[0]['down'] and numPlayers > 2:
                    numPlayers-=1
                    press_count = 0

                if allControls[0]['shoot']: #on the shoot press move on
                    select_state = "mode"
                    press_count = 0

        if select_state == "mode":
            if press_count > PRESS_TIME:
                if allControls[0]['up'] and modeIndex < len(modes)-1:
                    modeIndex+=1
                    press_count = 0
                
                elif allControls[0]['down'] and modeIndex > 0:
                    modeIndex-=1
                    press_count = 0

                if allControls[0]['shoot']: #on the coin press move on
                    select_state = "level"
                    press_count = 0

        if select_state == "level":
            if press_count > PRESS_TIME:
                if allControls[0]['up'] and levelNum < NUM_LEVELS-1:
                    levelNum+=1
                    press_count = 0

                elif allControls[0]['down'] and levelNum > 0:
                    levelNum-=1
                    press_count = 0

                if allControls[0]['shoot']: #on the coin press move on
                    select_state = "player"
                    state = "init"
                    press_count = 0    

        press_count+=1

        drawBlackRects(screen, select_state)

        drawAllText(screen, font, WIDTH, HEIGHT, numPlayers, modes[modeIndex], levelNum)

    if state == "init":
        #all of this runs once to init sprites

        makePlatforms(platforms, levelNum)

        makePlayers(players, hats, numPlayers)

        state = modes[modeIndex]

    if state == "Deathmatch":
        screen.fill((0,0,0))

        checkForBulletPlayer(players, bullets, explosionPieces, False)

        updateAll(bullets, hats, players, platforms, explosionPieces, allControls, WIDTH, HEIGHT)

        drawAll(screen, font, bullets, players, hats, platforms, explosionPieces)

        state = updateState(allControls, modes[modeIndex])

    if state == "Team Deathmatch":
        screen.fill((0,0,0))
        
        checkForBulletPlayer(players, bullets, explosionPieces, True)

        updateAll(bullets, hats, players, platforms, explosionPieces, allControls, WIDTH, HEIGHT)

        drawAll(screen, font, bullets, players, hats, platforms, explosionPieces)

        state = updateState(allControls, modes[modeIndex])

    # Update the display
    pygame.display.flip()

    clock.tick(30)