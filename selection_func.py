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


def updateSelectState(allControls, press_count, v1, low, high, selectIndex, state, select_state = None):
	if select_state == None:
		select_state = [""]*(selectIndex+1)

	if press_count < PRESS_TIME:
		return (press_count, selectIndex, v1, state)
	
	if select_state[selectIndex] == 'numToWin':
		changeBy = 5
	else:
		changeBy = 1

	if allControls[0]['up'] and v1 < high:
		v1+=changeBy
		press_count = 0
	
	elif allControls[0]['down'] and v1 > low:
		v1-=changeBy
		press_count = 0
	
	if allControls[0]['shoot']:
		if selectIndex < 3:
			selectIndex+=1
		else:
			selectIndex = 0
			state = "init"

		press_count = 0

	return (press_count, selectIndex, v1, state)

def drawBlackRects(screen, state):
	"Draws black squares over the pieces we dont want, gives the appearence of the white encircling squares"
	yPos = 270

	player_rect = pygame.Rect(60, yPos, 200, 70)
	mode_rect = pygame.Rect(260, yPos, 200, 70)
	num_rect = pygame.Rect(520, yPos, 200, 130)
	level_rect = pygame.Rect(720, yPos, 200, 70)

	if state != "player":
		pygame.draw.rect(screen, (0,0,0), player_rect)

	if state != "mode":
		pygame.draw.rect(screen, (0,0,0), mode_rect)

	if state != "level":
		pygame.draw.rect(screen, (0,0,0), level_rect)

	if state != "numToWin":
		pygame.draw.rect(screen, (0,0,0), num_rect)

def drawAllText(screen, font, WIDTH, HEIGHT, numPlayers, gameMode, numToWin, levelNum):

	#print num players
	text = font.render(str(numPlayers), True, (255,255,255))
	text_rect = text.get_rect(center=(140, HEIGHT/2))
	screen.blit(text,text_rect)

	#print game mode
	text = font.render(str(gameMode), True, (255,255,255))
	text_rect = text.get_rect(center=((WIDTH/2)-135, HEIGHT/2))
	screen.blit(text,text_rect)

	#print the amount to win by
	text = font.render(str(numToWin), True, (255,255,255))
	text_rect = text.get_rect(center=((WIDTH/2)+120, HEIGHT/2))
	screen.blit(text,text_rect)

	#print level num
	text = font.render(str(levelNum), True, (255,255,255))
	text_rect = text.get_rect(center=(WIDTH-150, HEIGHT/2))
	screen.blit(text,text_rect)
	