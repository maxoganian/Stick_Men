import pygame

vect = pygame.math.Vector2 #2 for two dimensional

#Constants will be from config in game
JUMP = 15
GRAVITY = .5
ACC = 2
FRIC = -.15

MAXVEL = 30

WIDTH = 1000
HEIGHT = 600


class Sprite(pygame.sprite.Sprite):
    def __init__ (self, image, x, y, xVel = 0, yVel = 0, xAcc = 0, yAcc = 0):
        super(Sprite, self).__init__()
        self.surf = pygame.image.load(image)
        self.rect = self.surf.get_rect()
        
        #stores our position, velocity, acceleration        
        self.rect.center = (x,y)

        self.vel = vect(xVel, yVel)
        self.acc = vect(xAcc, yAcc)

    def move_x(self):
        x,y = self.rect.center


        if self.vel.x > MAXVEL:
            self.vel.x = MAXVEL

        x+= self.vel.x
        
        self.rect.center = (x,y)
   
    def move_y(self):
        x,y = self.rect.center

        if self.vel.y > MAXVEL:
            self.vel.y = MAXVEL
       
        y+= self.vel.y
        
        self.rect.center = (x,y)
    
    def move(self):
        self.move_x()
        self.move_y()

    def draw(self, screen):
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT       
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        
        screen.blit(self.surf, self.rect)
         
class Player(Sprite):
    def __init__ (self, x, y):
        super(Player, self).__init__("images/stick_man_running0.png", x, y, 0, 0, 0, GRAVITY)

        #make image background transperent
        #self.surf.convert()
        #self.surf.set_colorkey((0, 0, 0))

    def move_x(self, pressed_keys, platforms):
        self.acc.x = 0
        
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = ACC
            
        self.acc.x += self.vel.x * FRIC
        
        self.vel.x += self.acc.x
        
        if self.vel.x > MAXVEL:
            self.vel.x = MAXVEL

        x,y = self.rect.center
        
        x += int(self.vel.x + 0.5 * self.acc.x) #take integer b/c had some trouble with stopping
                
        self.rect.center = (x,y)


        hits = pygame.sprite.spritecollide(self,platforms, False)
        
        if hits:
            hit_plat = hits[-1] #this way we take the last hit plat
            
            #now decide what side of the platform were on and adjust
            #this method fails if the player moves to quickly into a skinny platform
            #this is rare, but is why we have to run at 30fps

            if (self.rect.left + self.rect.width/2) > (hit_plat.rect.left + hit_plat.rect.width/2):#we are on the right
                self.rect.left = hit_plat.rect.right
            else:
                self.rect.right = hit_plat.rect.left  

            self.vel.x = hit_plat.vel.x  

    def move_y(self, pressed_keys, platforms):

        hits = pygame.sprite.spritecollide(self,platforms, False)
        
        if not hits:
            self.acc.y = GRAVITY

        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0,11)
            if pygame.sprite.spritecollide(self,platforms, False): 
                self.vel.y = -JUMP
            self.rect.move_ip(0,-11)
        
        self.vel.y += self.acc.y
        
        if self.vel.y > MAXVEL:
            self.vel.y = MAXVEL
       
        x,y = self.rect.center

        y += self.vel.y + 0.5 * self.acc.y**2
       
        self.rect.center = (x,y)

        hits = pygame.sprite.spritecollide(self,platforms, False)
        
        if hits:
            hit_plat = hits[-1] #this way we take the last hit plat
            
            #same system as horizontal movement
            if (self.rect.top + self.rect.h/2) < (hit_plat.rect.top + hit_plat.rect.h/2):#we are on the bottom
                self.rect.bottom = hit_plat.rect.top
            else:
                self.rect.top = hit_plat.rect.bottom

            self.vel.y = hit_plat.vel.y
        
class Platform(Sprite):
    def __init__ (self, x, y, w, h, xVel = 0, yVel = 0):
        super(Platform, self).__init__("images/platform.png", x, y, xVel, yVel)
        self.rect.w = w
        self.rect.h = h

        self.surf = pygame.transform.scale(self.surf, (self.rect.width, self.rect.height))

def moveAll(players, platforms):
    "Move all sprites"
    
    pressed_keys = pygame.key.get_pressed()
    # have to deal with one dimension at a time b/c
    # collision detection consequences are easier that way

    #move x first to simplify detection
    for p in platforms:
        p.move_x() 
    
    for player in players:
        player.move_x(pressed_keys, platforms)

    #move y second
    for p in platforms:
        p.move_y()

    for player in players:
        player.move_y(pressed_keys, platforms)
   