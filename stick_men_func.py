import pygame
from stick_men import *

#init pygame
pygame.init()

# Joystick constants
JOY_BTN_NORTH = 3
JOY_BTN_SOUTH = 6    
JOY_BTN_EAST = 5     
JOY_BTN_WEST = 2    
JOY_BTN_CENTER = 4
JOY_BTN_COIN = 0
JOY_BTN_PLAYER = 1

def getControls(player, joys, useJoys):
    "Return the controls the player will use"
    #If joysticks are not detected use keyboard keys. 
    if not useJoys:
        pressed_keys = pygame.key.get_pressed()
        
        #we need to set different controls for the two players, these are just player movement values
        if player.id == 0:
            controls = [pressed_keys[pygame.K_UP], pressed_keys[pygame.K_LEFT], pressed_keys[pygame.K_RIGHT], pressed_keys[pygame.K_SPACE]]
            
        else:
            controls = [pressed_keys[pygame.K_w], pressed_keys[pygame.K_a], pressed_keys[pygame.K_d], pressed_keys[pygame.K_f]]
        
        #then after the different controls we add the two contros that are used regardess of what player.
        controls.append(pressed_keys[pygame.K_r])
        controls.append(pressed_keys[pygame.K_t])

    else:
        #use the correct joystick for player controls
        j = joys[player.id]

        #these greater than, less than statements will evaluate true or false, 
        #note the player 1 and two buttons are used to reset their respective players
        # the last one just uses a player 1 button as this is a general control
        controls = [j.get_axis(1) > .8, j.get_axis(0) > .8, j.get_axis(0) < -.8, j.get_button(JOY_BTN_CENTER), j.get_button(JOY_BTN_PLAYER), joys[0].get_button(JOY_BTN_COIN)]

    return controls

def getNumJoys():
    return pygame.joystick.get_count()

def initJoysticks(numJoysticks, joys):
    # look for joysticks
    print("Found " + str(numJoysticks) + " joysticks")
    # init all the joysticks we have and add them to joysticks

    for i in range(numJoysticks):
        j = pygame.joystick.Joystick(i)
        j.init()
        joys.append(j)

def makePlatforms(platforms):
    levelNum = random.randint(0,1)
    #levelNum = 1

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

def createBullets(player, bullets, controls):
    #ony fire after a certain amount of time has passed
    if controls[3] and player.shotCounter > SHOT_TIME:
        bullets.add(Bullet(player))
        player.shotCounter = 0
    
    player.shotCounter+=1

def checkForBulletPlayer(player, players, bullets, explosionPieces):
    "If bullet hits player kill player"
    #kill player:
    hits_player = player.hitGroup(bullets)
    
    if hits_player:
        hit_bullet = hits_player[0]
        if hit_bullet.playerId != player.id: #make sure the bullet isnt hitting its own player
            players[hit_bullet.playerId].kills += 1 #increase payer that shot the bullets kill count

            hit_bullet.kill() #remove bullet
            
            player.isAlive = False #kill player

            makeExplosion(explosionPieces, player)

def checkForBulletCollis(bullets, platforms):
    "If bullet hits platform or bullet hits bullet, kill bullet"
    pygame.sprite.groupcollide(bullets, platforms, True, False, collided=collision_check)

    pygame.sprite.groupcollide(bullets, bullets, True, True, collided=collision_check)

def collision_check(sprite1, sprite2):
    "Return True if sprites are colliding, unless it's the same sprite."
    #works with - pygame.sprite.groupcollide(explosionPieces, platforms, True, False, collided=collision_check) 
    if sprite1 is not sprite2:
        return sprite1.rect.colliderect(sprite2.rect)
    else:  # Both sprites are the same object, so return False.
        return False

def makeExplosion(explosionPieces, player):
    numPieces = random.randint(8, 14)

    for i in range(numPieces):
        explosionPieces.add(ExplosionPiece(player))


def updateAll(bullets, hats, players, platforms, explosionPieces, joys, useJoys, WIDTH, HEIGHT):
    "Update all sprites"    
    pressed_keys = pygame.key.get_pressed()

    #reset controls to false
    allControls = [False]*4
    
    # have to deal with one dimension at a time b/c
    # collision detection consequences are easier that way

    #move x first to simplify detection
    for p in platforms:
        p.move_plat_x() 
    
    for player in players:
        #controls is a two layer array, one for player1 one for player2. These layers are 5 long, holding boolean values
        #for jumping moving ect
        allControls[player.id] = getControls(player, joys, useJoys) #get the controls once here, then we know how to move for y too
        if player.isAlive:
            #print(controls)
            player.move_x(platforms, allControls[player.id])

    #move y second
    for p in players:#if we check if we can jump before the plat moves, the player can move down less.
        p.checkForJump(platforms)    

    for p in platforms:
        p.move_plat_y()

    for player in players:
        if player.isAlive:
            checkForBulletPlayer(player, players, bullets, explosionPieces)#pass players to increase kill counter im not a fan of this method

            hats[player.id].update(player) #putting hat movement here makes the hat follow the player, b/c the player moves
                                           #after the hat
            player.move_y(platforms, allControls[player.id])
            
            if player.vel.y < 0: #if the player is moving up we want the hat glued to their head
                hats[player.id].update(player)

            createBullets(player, bullets, allControls[player.id])#creates bullets on key presss

        if allControls[player.id][4]: #realive players
            player.isAlive = True

    #Move everything ----These updates actually just keep the item below the top velocity and on screen
    #theyre names need changed
    for bullet in bullets:
        bullet.move()
        bullet.updateBullet(WIDTH, HEIGHT)

    for piece in explosionPieces:
        piece.move()
        piece.updateExplos(WIDTH, HEIGHT, platforms, players)
    
    for player in players:
        player.update(WIDTH, HEIGHT)

    for platform in platforms:
        platform.update(WIDTH, HEIGHT)

    #if we press t choose a new random level, doesnt work amazing but this is a pretty temporary feature
    if allControls[0][5]: 
        makePlatforms(platforms)

    checkForBulletCollis(bullets, platforms)

def drawAll(screen, bullets, players, hats, platforms, explosionPieces):
    #draw all sprites
    for bullet in bullets:
        bullet.draw(screen)

    for player in players:
        player.draw(screen)
        
        hats[player.id].draw(screen)

        player.drawKillsAndShotRect(screen, hats[player.id])

    for platform in platforms:
        platform.draw(screen)

    for piece in explosionPieces:
        piece.draw(screen)
    