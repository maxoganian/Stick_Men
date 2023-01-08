import pygame

pygame.init()

running = True

while running:

	pygame.mixer.Sound.play(pygame.mixer.Sound("sounds/im_back.wav").set_volume(0.5))