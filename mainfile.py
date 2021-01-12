import pygame
import random
import math
from pygame import mixer

pygame.init()

#Create The Screen
screen = pygame.display.set_mode((800,600))

# Background & Background Sound
background= pygame.image.load('backg.png')
mixer.music.load('background01.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption('Alien Hunter 2D')
icon=pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Player
player_img=pygame.image.load('player.png')
playerX=370
playerY=480
playerX_change=0

# Enemy
enemy_img=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemy=6

for i in range(num_of_enemy):
    enemy_img.append(pygame.image.load('alien2.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bullet_img=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state='ready'

# Score
score_value=0
font = pygame.font.Font('freesansbold.ttf',20)
textX=10
textY=10

game_over_font = pygame.font.Font('freesansbold.ttf',40)

def game_over():
    game_over_text = game_over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(game_over_text, (250, 250))

def showScore(x,y):
    score = font.render('Score : '+str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))

def player(x,y):
    screen.blit(player_img, (x,y)) # blit means to draw.

def enemy(x,y,i):
    screen.blit(enemy_img[i], (x,y)) # blit means to draw.

def fireBullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bullet_img,(x+16 , y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+ math.pow(enemyX-bulletY,2))
    if distance<27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # If keystroke is pressed check whether its right or left..
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change= -5.0
            if event.key == pygame.K_RIGHT:
                playerX_change= 5.0
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX =playerX
                    fireBullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change= 0.0

    # Checking Boundary For SpaceShip.
    playerX+= playerX_change

    if playerX<=0:
        playerX = 0
    elif playerX>=736:
        playerX=736

    # Enemy Movement.
    for i in range(num_of_enemy):
        #Game Over
        if enemyY[i]>440:
            for j in range(num_of_enemy):
                enemyY[j]=2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4.0
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4.0
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i],i)

    # Bullet Movement
    if bulletY<=0:
        bulletY=480
        bullet_state='ready'

    if bullet_state is 'fire':
        fireBullet(bulletX,bulletY)
        bulletY-= bulletY_change

    player(playerX, playerY)
    showScore(textX,textY)
    pygame.display.update()


#2.10.00 / 2.15.48