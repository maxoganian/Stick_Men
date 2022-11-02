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

def updateState(allControls, mode):
	#press the low thumb joy to return to the start
    if allControls[0]['back']:
        return "start"
    else:
    	return mode
    	
def drawBlackRects(screen, state):
	"Draws black squares over the pieces we dont want, gives the appearence of the white encircling squares"
	yPos = 270

	player_rect = pygame.Rect(100, yPos, 200, 70)
	mode_rect = pygame.Rect(400, yPos, 200, 70)
	level_rect = pygame.Rect(700, yPos, 200, 70)

	if state != "player":
		pygame.draw.rect(screen, (0,0,0), player_rect)

	if state != "mode":
		pygame.draw.rect(screen, (0,0,0), mode_rect)

	if state != "level":
		pygame.draw.rect(screen, (0,0,0), level_rect)

def drawAllText(screen, font, WIDTH, HEIGHT, numPlayers, gameMode, levelNum):

	#print num players
	text = font.render(str(numPlayers), True, (255,255,255))
	text_rect = text.get_rect(center=(200, HEIGHT/2))
	screen.blit(text,text_rect)

	#print game mode
	text = font.render(str(gameMode), True, (255,255,255))
	text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
	screen.blit(text,text_rect)

	#print level num
	text = font.render(str(levelNum), True, (255,255,255))
	text_rect = text.get_rect(center=(WIDTH-200, HEIGHT/2))
	screen.blit(text,text_rect)
	