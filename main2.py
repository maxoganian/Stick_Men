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

players = pygame.sprite.Group()
players.add(Player(200, 100))
players.add(Player(800, 100))

platforms = pygame.sprite.Group()
platforms.add(Platform(250, 500, 500, 10, 0, 0))
platforms.add(Platform(200, 460, 100, 10, 4, -4))

running = True
while running:
    for event in pygame.event.get():
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,100))

    moveAll(players, platforms)

    for player in players:
        player.draw(screen)

    for platform in platforms:
        platform.draw(screen)
    
    # Update the display
    pygame.display.flip()

    clock.tick(30)