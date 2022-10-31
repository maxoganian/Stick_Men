import pygame
from stick_men import *

#init pygame
pygame.init()


def drawAllText(screen, font, WIDTH, HEIGHT, numPlayers, levelNum, gameMode):
	screen.blit(font.render(str(numPlayers), True, (255,255,255)),(WIDTH/3, HEIGHT/2))#print num players

	screen.blit(font.render(str(levelNum), True, (255,255,255)),(WIDTH/3, HEIGHT/2))#print level num

	screen.blit(font.render(str(gameMode), True, (255,255,255)),(WIDTH/3, HEIGHT/2))#print gamemode