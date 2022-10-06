import pygame

pygame.init()

clock = pygame.time.Clock()

#game window width and height
WIDTH = 1000
HEIGHT = 600

# Create the screen object
# The size is determined by the constant WIDTH and HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Sprite(pygame.sprite.Sprite):
    def __init__ (self, image, x, y, xVel = 0, yVel = 0, xAcc = 0, yAcc = 0):
        super(Sprite, self).__init__()
        self.surf = pygame.image.load(image)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.xVel = xVel
        self.yVel = yVel

        self.xAcc = xAcc
        self.yAcc = yAcc

    def update(self):
        
        self.xVel += self.xAcc
        self.yVel += self.yAcc

        self.rect.move_ip(self.xVel, self.yVel)
    
        screen.blit(self.surf, self.rect)
         
class Player(Sprite):
    def __init__ (self, x, y):
        super(Player, self).__init__("images/stick_man_running0.png", x, y, 0, 0, 0, 2)

class Platform(Sprite):
    def __init__ (self, x, y, w, h):
        super(Platform, self).__init__("images/platform.png", x, y)
        self.rect.w = w
        self.rect.h = h

        self.surf = pygame.transform.scale(self.surf, (self.rect.width, self.rect.height))

player = Player(500, 0)

platform = Platform(200, 500, 500, 10)

running = True
while running:
    for event in pygame.event.get():
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False


    screen.fill((0,255,0))

    if pygame.Rect.colliderect(player.rect, platform.rect):
        player.yVel = platform.yVel


    player.update()
    
    platform.update()

    # Update the display
    pygame.display.flip()

    clock.tick(20)