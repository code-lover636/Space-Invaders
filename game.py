import pygame
import sys
from math import sqrt
from random import randint, choice

pygame.init()

# screen
WIDTH, HEIGHT = 795, 530
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
pygame.display.set_caption("SPACE INVADERS")
flag = pygame.image.load('assets/bg/flag.png')
SPACE_BG = pygame.image.load('assets/bg/space_bg.jpg')
RELOADING_BG = pygame.image.load('assets/bg/reloading_bg.jpg')
GAME_OVER_BG = pygame.image.load('assets/bg/game_over_bg.jpg')
background = SPACE_BG
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Music
exploding_sound = pygame.mixer.Sound("assets/sound/explosion.wav")

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

def scoreboard():
    global score, text
    text = font.render(f'Score:{score}', True, (255,0,0))
    screen.blit(text, (620,500))

# play again
mode = "play"

def play_again(pos):
    global score, mode, alien_vel, ship_vel, missile_vel, ALIEN, alienX, alienY, background
    if mode=="game over" and (350 < pos[0] < 445 and 25 < pos[1] < 105):
        score = 0
        background = SPACE_BG
        mode = "play"
        alien_vel = [ randint(5,10)/10 for _ in range(NoOfAliens) ]
        ship_vel = 0.7
        missile_vel = 0.5
        for x in range(NoOfAliens):
            ALIEN[x] = choice(alienimg)
            alienX[x], alienY[x] = randint(10,700), randint(-200,0)
        
# Collission checking  
def is_collision(pos_m,pos_a,x):
    global alienX, alienY, alien_vel, missileX, missileY, blasted, fired, background, alienimg, alien_pos, score
    if sqrt( pow((pos_a[0]-pos_m[0]),2) + pow((pos_a[1]-pos_m[1]),2) ) < 55:
        pygame.mixer.Sound.play(exploding_sound); pygame.mixer.music.stop()
        score += 5 
        # Bullet respawning
        fired = False
        missileX, missileY = shipX+68, SHIPY+20
        background = SPACE_BG
        # Alien respawning
        ALIEN[x] = choice(alienimg)
        alien_pos = (alienX[x], alienY[x])
        alienX[x], alienY[x] = randint(10,700), randint(-200,0)
        blasted[x] = True

# Space ship
SPACE_SHIP = pygame.image.load('assets/rocket.png')
shipX, SHIPY = 370,370
ship_vel = shipXchange = 0.7

def ship():
    global shipX, ship_vel, missileX
    screen.blit(SPACE_SHIP, (shipX, SHIPY))
    if -50 < shipX < 680: 
        shipX += ship_vel
        if not fired: missileX += ship_vel
    else: 
        shipX -= ship_vel
        ship_vel *= -1
        if not fired: missileX -= ship_vel


# Missile
MISSILE = pygame.image.load('assets/bullet.png')
missileX, missileY = shipX+68, SHIPY+20
missile_vel = 0.5
fired = False

def missile():
    global missileX, missileY, fired, background
    screen.blit(MISSILE, (missileX, missileY))
    for x in range(NoOfAliens):
        if fired:
            missileY -= missile_vel
            is_collision([missileX, missileY], [alienX[x],alienY[x]],x)
    if missileY < -10: 
        fired = False
        missileY = SHIPY+20
        missileX = shipX+67
        background = SPACE_BG

# Alien
NoOfAliens = 7
alienimg = [ pygame.image.load(f'assets/alien/{x}.png') for x in range(1,5) ]
ALIEN = [ choice(alienimg) for _ in range(NoOfAliens)]
BLAST = pygame.image.load('assets/alien/blast.png')
blasted = [ False for _ in range(NoOfAliens) ]
count = 0
alienX = [ randint(10,700) for _ in range(NoOfAliens) ]
alienY = [ randint(-200,0) for _ in range(NoOfAliens) ]
alien_vel = [ randint(5,10)/10 for _ in range(NoOfAliens) ]

def game_over(x):
    global alien_vel, ship_vel, missile_vel, mode, background, count, blasted, missileX, missileY
    if alienY[x] > 320:
        count = 0
        missileX, missileY = shipX+68, SHIPY+20
        blasted = [ False for _ in range(NoOfAliens) ]
        mode = "game over"
        background = GAME_OVER_BG
        alien_vel = [0]*NoOfAliens
        ship_vel = 0
        missile_vel = 0
        
        
def alien():
    global alienX, alienY, alien_vel, count, blasted
    for x in range(NoOfAliens):
        game_over(x)
        if 0 < alienX[x] < 730: 
            alienX[x] += alien_vel[x]
        else: 
            alienY[x] += randint(50,100)
            alienX[x] -= alien_vel[x]
            alien_vel[x] *= -1
        if blasted[x]:
            screen.blit(BLAST, alien_pos)
            count += 1
        if count == 100:
            count = 0
            blasted[x] = False
                
        screen.blit(ALIEN[x], (alienX[x], alienY[x]))

counter = 1
# MAIN LOOP
while 1:
    
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(flag, (5,350))
    screen.blit(flag, (670,350))
    
    scoreboard(); missile(); ship(); 
    if mode == "play": alien() 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            if mode == "game over": play_again(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:        
                if mode == "play": ship_vel = -shipXchange
            elif event.key == pygame.K_RIGHT:
                if mode == "play": ship_vel = shipXchange
            elif event.key == pygame.K_SPACE:
                if mode == "play": 
                    fired = True
                    background = RELOADING_BG
            elif event.key == pygame.K_TAB:
                if counter: alien_vel=[0]*NoOfAliens; counter = 0
                else: alien_vel = [ randint(5,10)/10 for _ in range(NoOfAliens) ]; counter=1
            
    pygame.display.update()