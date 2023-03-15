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

useJoys = numJoysticks > 3

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

#set mouse to transparent
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

state = "start"

#used to store the winnign players
winning_players = []

#these two are used for the select screen
select_states = ["player", "mode", "numToWin", "level"]
selectIndex = 0

press_count = 0

#these globals will be chosen in the select menu
numPlayers = 2

modes = ["Deathmatch", "Team Deathmatch", "KDR", "Timed KDR"]
modeIndex = 0

numToWin = 20

levelNum = 1

#store sounds, so all sounds can be easily passed
sounds  = {'death': pygame.mixer.Sound("sounds/Death.wav"), 'woosh': pygame.mixer.Sound("sounds/woosh.wav"), 
            'im_back': pygame.mixer.Sound("sounds/im_back.wav"), 'win0': pygame.mixer.Sound("sounds/win0.wav"),
            'win1': pygame.mixer.Sound("sounds/win1.wav"), 'win2': pygame.mixer.Sound("sounds/win2.wav"), 
            'win3': pygame.mixer.Sound("sounds/win3.wav")}

sounds['woosh'].set_volume(10.0)

for sound in sounds.values():
    sound.set_volume(4.0)

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

    #always be able to exit
    if allControls[0]['coin'] and allControls[0]['player']: 
        running = False
    
    if state == "start":
        screen.blit(pygame.image.load("images/start_background.png"), (0,0))
        
        #remove the explosions left over from the win screen
        for piece in explosionPieces:
            piece.kill()

        if allControls[0]['coin']: #on the coin press move to slection
            state = "selection"

    if state == "selection":

        screen.blit(pygame.image.load("images/selection_background.png"), (0,0))

        if select_states[selectIndex] == "player":
            press_count, selectIndex, numPlayers, state = updateSelectState(allControls, press_count, 
                                                                        numPlayers, 2, 4, selectIndex, state)

        if select_states[selectIndex] == "mode":
            press_count, selectIndex, modeIndex, state = updateSelectState(allControls, press_count, 
                                                                        modeIndex, 0, len(modes)-1, selectIndex, state)
        if select_states[selectIndex] == "numToWin":
            press_count, selectIndex, numToWin, state = updateSelectState(allControls, press_count, numToWin,
                                                                                5, 100, selectIndex, state, select_states,
                                                                                modes[modeIndex])
            
        if select_states[selectIndex] == "level":
            press_count, selectIndex, levelNum, state = updateSelectState(allControls, press_count, 
                                                                        levelNum, 0, NUM_LEVELS-1, selectIndex, state) 

        press_count+=1

        drawBlackRects(screen, select_states[selectIndex])

        drawAllText(screen, font, WIDTH, HEIGHT, numPlayers, modes[modeIndex], numToWin, levelNum)

    if state == "init":
        #all of this runs once to init sprites

        makePlatforms(platforms, levelNum)

        makePlayers(players, hats, numPlayers)

        state = modes[modeIndex]

    if state == "Deathmatch" or state == "Team Deathmatch" or state == "KDR" or state == "Timed KDR":
        screen.fill((0,0,0))

        checkForBulletPlayer(players, bullets, explosionPieces, state, sounds)

        updateAll(bullets, hats, players, platforms, explosionPieces, allControls, sounds, WIDTH, HEIGHT)

        drawAll(screen, font, bullets, players, hats, platforms, explosionPieces, state, numToWin)

        state = updateState(allControls, modes[modeIndex])

        tempState, winning_players, numToWin  = handleWinner(players, explosionPieces, numToWin, screen, font, 
                                                    state, allControls, sounds)
        if tempState == "winner":
            state = "winner"

    if state == "winner":
        state = updateState(allControls, state)

        drawWinScreen(screen, winning_players, explosionPieces, font, modes[modeIndex])

    # Update the display
    pygame.display.flip()

    clock.tick(30)