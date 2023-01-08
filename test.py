import pygame

pygame.init()

running = True

sound = pygame.mixer.Sound("sounds/im_back.wav")

sound.set_volume(1)

while running:

	pygame.mixer.Sound.play(sound)