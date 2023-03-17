import pygame
import time
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
JOY_BTN_THUMB = 7

def drawBackground(screen, image):
    screen.blit(image, (0,0))

def getControls(i, joys, useJoys):
    "Return the controls the player will use"
    #If joysticks are not detected use keyboard keys. 
    if not useJoys:
        pressed_keys = pygame.key.get_pressed()
        
        #we need to set different controls for the players, these are just player movement values
        if i == 0:
            controls = {'up': pressed_keys[pygame.K_UP], 'down': pressed_keys[pygame.K_DOWN], 
                            'left': pressed_keys[pygame.K_LEFT], 'right': pressed_keys[pygame.K_RIGHT],
                             'shoot': pressed_keys[pygame.K_SPACE]}
        elif i == 1:
            controls = {'up': pressed_keys[pygame.K_w], 'down': pressed_keys[pygame.K_s],
                            'left': pressed_keys[pygame.K_a], 'right': pressed_keys[pygame.K_d], 
                            'shoot': pressed_keys[pygame.K_e]}
        elif i == 2:
            controls = {'up': pressed_keys[pygame.K_t], 'down': pressed_keys[pygame.K_g],
                            'left': pressed_keys[pygame.K_f], 'right': pressed_keys[pygame.K_h], 
                            'shoot': pressed_keys[pygame.K_y]}
        else:
            controls = {'up': pressed_keys[pygame.K_i], 'down': pressed_keys[pygame.K_k],
                            'left': pressed_keys[pygame.K_j], 'right': pressed_keys[pygame.K_l],
                            'shoot': pressed_keys[pygame.K_o]}
        
        #then after the different controls we add the controls that are used regardless of what player.
        controls['player'] = pressed_keys[pygame.K_p]
        controls['coin'] = pressed_keys[pygame.K_c]
        controls['back'] = pressed_keys[pygame.K_b]

    else:
    #use the correct joystick for player controls
        j = joys[i]

        #these greater than, less than statements will evaluate true or false, 
        #note the player 1 and two buttons are used to reset their respective players
        controls = {'up': j.get_axis(1) > .8, 'down': j.get_axis(1) < -.8, 'left': j.get_axis(0) > .8, 
                        'right': j.get_axis(0) < -.8, 'shoot': j.get_button(JOY_BTN_CENTER), 
                        'player': j.get_button(JOY_BTN_PLAYER), 'coin': j.get_button(JOY_BTN_COIN), 
                        'back': j.get_button(JOY_BTN_THUMB)}

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

def createBullets(player, bullets, controls, sounds):
    #ony fire after a certain amount of time has passed
    if controls['shoot'] and player.shotCounter > SHOT_TIME:
        
        playSound(sounds['woosh'])
        bullets.add(Bullet(player))
        player.shotCounter = 0
    
    player.shotCounter+=1

def playSound(sound):
    pygame.mixer.Sound.play(sound)

def updateState(allControls, state):
    #press the low thumb joy to return to the start
    oldState = state

    if allControls[0]['back']:
        return "start"
    else:
        return oldState

def handleWinner(players, explosionPieces, amount, kdrTimer, screen, font, state, allControls, sounds, hasNotPlayed = True):
    winning_players = []

    if state == "Deathmatch": 
        for player in players:
            if checkForWinKills(player, amount):
                winning_players = [player]
                
                playSound(sounds['win' + str(player.id)])

                state = "winner"

    elif state == "Team Deathmatch":
        #none of this is the prettiest but its finals week and i want the game done
        if returnWinKillsTeam(players, amount) == 1:
            #figure out the number of players, so there is no out of bounds error
            
            if len(players) <= 2:
                winning_players = [players[0]]
            else:
                winning_players = [players[0], players[2]]
            
            playSound(sounds['win0'])

            state = "winner"

        elif returnWinKillsTeam(players, amount) == 2:
            #figure out the number of players, so there is no out of bounds error
            
            if len(players) <= 3:
                winning_players = [players[1]]
            else:
                winning_players = [players[1], players[3]]

            playSound(sounds['win1'])
            
            state = "winner"
    
    elif state == "KDR":
        for player in players:
            if player.kdr >= amount:
                winning_players = [player]

                playSound(sounds['win' + str(player.id)])

                state = "winner"
    
    elif state == "Timed KDR":
        #since we run at 30 fps this counts in minutes
        kdrTimer -= (1/30)/60
        #kdrTimer -= (1/30)
        
        if kdrTimer <= 0:
            max = 0
            for player in players:
                if player.kdr >= max:
                    max = player.kdr
                    winning_players.append(player)

            if len(winning_players) == 1: #only play a sound if there is one winner
                playSound(sounds['win' + str(winning_players[0].id)])

            state = "winner"

        #print(kdrTimer)

    return state, winning_players, kdrTimer

def checkForWinKills(player, amount):
    if player.kills >= amount:
        return True
    else:
        return False

def returnWinKillsTeam(players, amount):
    team1 = 0
    team2 = 0

    for player in players:
        if player.id % 2 == 0:
            team1 += player.kills
        else:
            team2 += player.kills

    if team1 >= amount:
        return 1
    elif team2 >= amount:
        return 2
    else:
        return 0

def drawWinScreen(screen, winning_players, explosionPieces, font, gamemode):
    screen.fill((0,0,0))
    #print the winner players
    for player in winning_players:
        makeExplosion(explosionPieces, player)

    for piece in explosionPieces:
        piece.move()
        piece.draw(screen)


    if gamemode == "Deathmatch" or gamemode == "KDR":
        text = font.render("Player " + str(winning_players[0].id +1) + " wins", True, (255,255,255))
    elif gamemode == "Team Deathmatch":
        text = font.render("Team " + str((winning_players[0].id%2) +1) + " wins", True, (255,255,255))
    
    elif gamemode == "Timed KDR":
        if len(winning_players) == 1:
            text = font.render("Player " + str(winning_players[0].id +1) + " wins", True, (255,255,255))
        else:
            
            #if kdrs are exactly equal this is used to show a tie 
            playerNums = ""

            for player in winning_players:
                playerNums += str(player.id +1) + ", "
            
            text = font.render("Players " + playerNums + "tie", True, (255,255,255))

    text_rect = text.get_rect(center=(500, 250))
    screen.blit(text, text_rect)
    
    text = font.render("Press Player 1 lower thumb button to return", True, (255,255,255))
    text_rect = text.get_rect(center=(500, 350))
    screen.blit(text, text_rect)

def printTopVals(state, numToWin, kdrTimer, players, screen, font):
    "Prints out the values at the top of the in game screen"
 
    if state == "Team Deathmatch":
        tempText = ""
        team1 = 0
        team2 = 0

        for player in players:
            if player.id%2 == 0:
                team1 += player.kills
            else:
                team2 += player.kills        

        text = font.render("Team 1 has " + str(team1) + " kills     |      Team 2 has " + str(team2) + " kills", 
                                True, (255,255,255))
    
        text_rect = text.get_rect(center=(500, 20))
        screen.blit(text, text_rect)

    if state != "Timed KDR":
        text = font.render("Needs " + str(numToWin) + " to win", True, (255, 255, 255))
    else:
        text = font.render(str(round(kdrTimer, 3)) + " minutes left", True, (255, 255, 255))
    
    text_rect = text.get_rect(center=(500, 40))
    screen.blit(text, text_rect)

def checkForBulletPlayer(players, bullets, explosionPieces, gamemode, sounds):
    "If bullet hits player kill player"
    isTeam = gamemode == "Team Deathmatch"

    #kill player:

    for bullet in bullets:
        hit_players = bullet.hitGroup(players)
    
        if hit_players:
            
            for hit_player  in hit_players: #loop through all players so when the player hit is stacked onto
                                            #the player shooting the player being shot will stil die
                if hit_player.isAlive: 
                    player_shooting = players[bullet.playerId]

                    #this handles finding teams based off player id
                    if isTeam:
                        #if there is a remainder when dividing, then we are team 1, and vice versa, 
                        #this checks they arent on the same team
                        if hit_player.id%2 != player_shooting.id%2: 
                            teamCheck = True
                        else:
                            teamCheck = False
                    else:
                        teamCheck = True

                    if hit_player.id != player_shooting.id and teamCheck: #make sure the bullet isnt hitting its own player
                        player_shooting.kills += 1 #increase payer that shot the bullets kill count
                        
                        hit_player.isAlive = False #kill player
                        hit_player.deaths += 1

                        playSound(sounds['death'])

                        makeExplosion(explosionPieces, hit_player)

                        bullet.kill() #remove bullet

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


def updateAll(bullets, hats, players, platforms, explosionPieces, allControls, sounds, WIDTH, HEIGHT):
    "Update all sprites"    
    pressed_keys = pygame.key.get_pressed()
    
    # have to deal with one dimension at a time b/c
    # collision detection consequences are easier that way

    #move x first to simplify detection
    for p in platforms:
        p.move_plat_x() 
    
    for player in players:
        if player.isAlive:
            #print(controls)
            player.move_x(platforms, allControls[player.id])

    #move y second
    for p in players:#if we check if we can jump before the plat moves, the player can move down less.
        p.checkForJump(platforms)    

    for p in platforms:
        p.move_plat_y()

    for player in players:
        hats[player.id].update(player) #putting hat movement here makes the hat follow the player, b/c the player moves
                                           #after the hat; the hat updatehas to be outside of the isAlive so the hat 
                                           #unalive with the player
        if player.isAlive:
            player.move_y(platforms, allControls[player.id])
            
            player.animate(allControls)# update player frame

            if player.vel.y < 0: #if the player is moving up we want the hat glued to their head
                hats[player.id].update(player)

            createBullets(player, bullets, allControls[player.id], sounds)#creates bullets on key presss

        if allControls[player.id]['player']: #realive players
            
            if not player.isAlive:
                playSound(sounds['im_back'])
            
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

    checkForBulletCollis(bullets, platforms)

def drawAll(screen, font, bullets, players, hats, platforms, explosionPieces, state, numToWin, kdrTimer):
    
    printTopVals(state, numToWin, kdrTimer, players, screen, font)
    
    #draw all sprites
    for bullet in bullets:
        bullet.draw(screen)

    for player in players:
        player.draw(screen)
        
        hats[player.id].draw(screen)

        player.drawKillsAndShotRect(state, screen, hats[player.id], font)

    for platform in platforms:
        platform.draw(screen)

    for piece in explosionPieces:
        piece.draw(screen)