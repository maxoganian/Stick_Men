import pygame
from stick_men import *
import configparser

#init pygame
pygame.init()

PRESS_TIME = float(config['DEFAULTS']['PRESS_TIME'])

def makePlayers(players, hats, numPlayers):
    #clear old players and hats.
    players.clear()
    hats.clear()

    for i in range(numPlayers):
        players.append(Player((i+1)*200, 100, i))#create players spaced 200 apart

    for player in players:
        hats.append(Hat(player))

def makePlatforms(platforms, levelNum):
    level = 'LEVEL_' + str(levelNum)
    
    print(level)
    for platform in platforms:
        platform.kill()
    
    numPlatforms = int(config[level]['num_platforms'])

    #first add statonary platforms then moving ones
    for i in range(numPlatforms):
       platform = eval(config[level]['p'+str(i)])
       platforms.add(Platform(platform))
    
    print("platforms: " + str(platforms))

def select(allControls, press_count):
	if allControls[0]['shoot'] and press_count > PRESS_TIME:
		return True
	else:
		return False

def drawAllText(screen, font, WIDTH, HEIGHT, numPlayers, gameMode, levelNum):
	screen.blit(font.render(str(numPlayers), True, (255,255,255)),(200, HEIGHT/2))#print num players

	screen.blit(font.render(str(gameMode), True, (255,255,255)),(WIDTH/2, HEIGHT/2))#print gamemode

	screen.blit(font.render(str(levelNum), True, (255,255,255)),(WIDTH-200, HEIGHT/2))#print level num