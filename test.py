import pygame

pygame.init()

running = True

sound = pygame.mixer.Sound("sounds/im_back.wav")

sound.set_volume(2)

while running:

	pygame.mixer.Sound.play(sound)