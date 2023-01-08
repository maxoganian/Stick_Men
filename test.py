import pygame

pygame.init()

running = True

while running:

	pygame.mixer.Sound.play(pygame.mixer.Sound("sounds/Death.wav"))