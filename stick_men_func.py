import pygame
from stick_men import *

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

def createBullets(player, bullets, pressed_keys):
    #ony fire after a certain amount of time has passed
    if pressed_keys[player.keys[3]] and player.shotCounter > SHOT_TIME:
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


def updateAll(bullets, hats, players, platforms, explosionPieces):
    "Update all sprites"    
    pressed_keys = pygame.key.get_pressed()

    # have to deal with one dimension at a time b/c
    # collision detection consequences are easier that way

    #move x first to simplify detection
    for p in platforms:
        p.move_plat_x() 
    
    for player in players:
        if player.isAlive:
            player.move_x(pressed_keys, platforms)

    #move y second
    for p in platforms:
        p.move_plat_y()

    for player in players:
        if player.isAlive:
            checkForBulletPlayer(player, players, bullets, explosionPieces)#pass players to increase kill counter im not a fan of this method

            hats[player.id].update(player) #putting hat movement here makes the hat follow the player, b/c the payer moves
                                           #after the hat
            player.move_y(pressed_keys, platforms)
            
            if player.vel.y < 0: #if the player is moving up we want the hat glued to their head
                hats[player.id].update(player)

            createBullets(player, bullets, pressed_keys)#creates bullets on key presss

        if pressed_keys[pygame.K_r]: #realive players
            player.isAlive = True

    for bullet in bullets:
        bullet.move()

    for piece in explosionPieces:
        piece.move()
    #if we press t choose a new random level, doesnt work amazing but this is a pretty temporary feature
    if pressed_keys[pygame.K_t]: 
        makePlatforms(platforms)

    checkForBulletCollis(bullets, platforms)    