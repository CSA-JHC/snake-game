##MIT License
##
##Permission is hereby granted, free of charge, to any person obtaining a copy
##of this software and associated documentation files (the "Software"), to deal
##in the Software without restriction, including without limitation the rights
##to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##copies of the Software, and to permit persons to whom the Software is
##furnished to do so, subject to the following conditions:
##
##The above copyright notice and this permission notice shall be included in all
##copies or substantial portions of the Software.
##
##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

##Version 0.3
##Jessica Chiu
##Snake where you have the ability to control a snake and gain points
##by eating the red apples. The green apples makes you lose a point.
##Levels increase based on the amount of points you have.

#CHEAT CODES
#level 1 = 1 (easy)
#level 2 = 2 (medium)
#level 3 = 3,4 (hard)
#level 4 = 5,6 (hard2)
#level 5 = 7,8 (obstacle)
#level 6 = 9,10 (hardobstacle)

#find credit image
#fix initials

import pygame,sys
from pygame.locals import *
import random
import time
import os

pygame.init()
pygame.mixer.init()

#colors
BG=(0,0,0)
BROWN=(139,69,19)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,225)
YELLOW=(255,255,0)

#set screen
DISPLAYSURF = pygame.display.set_mode((800, 500))
#DISPLAYSURF.fill(WHITE)
pygame.display.set_caption('Snake')

#snake measurements per box
snakeheight=20
snakewidth=20
margin=3
#global variables to help keep track of score
score=0
level=1
create=5
ticker=5 #speed
number=0

#list to keep track of apples and direction
Apples=[]
BadApples=[]
Direction=['right']
AIDirection=['right']

x_change=snakewidth+margin
y_change=0

a_change=snakewidth+margin
b_change=0

f_change=snakewidth+margin
g_change=0

#reference class
class Basic(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        #snake box
        self.image=pygame.Surface([snakewidth,snakeheight])
        self.image.fill(WHITE)

        #location
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

#player class
class Snake(Basic):
    def __init__(self,x,y):
        super(Snake, self).__init__(x,y)

        self.image.fill(WHITE) #fill white
        self.x_change = snakewidth + margin
        self.y_change = 0

#AI class
class AISnake(Basic):
    def __init__(self,x,y):
        super(AISnake,self).__init__(x,y)

        self.image.fill(BLUE)
        self.a_change = snakewidth + margin
        self.b_change = 0

#apple class
class Apple(Basic):
    def __init__(self,x,y):
        super(Apple, self).__init__(x,y)

        self.image.fill(RED) #fill red

#bad apple class, comes from snake class
class BadApple(Basic):
    def __init__(self,x,y):
        super(BadApple, self).__init__(x,y)

        self.image.fill(GREEN)

class Obstacle(Basic):
    def __init__(self,x,y):
        super(Obstacle, self).__init__(x,y)

        self.image.fill(BROWN)

#checks for collision and adds points
def collision(badsnake,snake,food,pics,sound):
    global score
    for s in snake:
        for a in food:
            #if collided with red apple
            if s.rect.colliderect(a):
                sound.play() #play sound
                #remove from lists
                food.remove(a)
                pics.remove(a)
                #add new box on snake
                x = (x_change + margin)
                y = 30
                segment = Snake(x, y)
                #add to lists
                snake.append(segment)
                pics.add(segment)
                score+=1 #add a point
    for s in badsnake:
        for a in food:
            #if collided with red apple
            if s.rect.colliderect(a):
                sound.play() #play sound
                #remove from lists
                food.remove(a)
                pics.remove(a)
                #add new box on snake
                x = (x_change + margin)
                y = 30
                segment = AISnake(x, y)
                #add to lists
                badsnake.append(segment)
                pics.add(segment)

def specialcollision(badsnake,snake,food,pics,sound,music):
    global score
    global ticker

    if len(badsnake)<=1:
        end_it = False
        while (end_it == False):
            #get font
            textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
            #highscore font, blit in center
            listscore = []
            # open scores file
            file = open('highscores.txt', 'r')
            for line in file:
                listscore.append(int(line))  # add scores to a list
            listscore.append(score)  # add score to a list
            file.close()

            if score >= listscore[0]:  # if the score is >=highscore
                end_it = False
                while (end_it == False):
                    # blit highscore on screen
                    textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                    overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
                    overrect = overobj.get_rect()
                    overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                    overrect.centery = DISPLAYSURF.get_rect().centery - 90
                    DISPLAYSURF.blit(overobj, overrect)
                    os.system('initialstk.py')
                    end_it = True
                pygame.display.flip()
            elif score >= listscore[-1]:  # if the score is >=highscore
                end_it = False
                while (end_it == False):
                    # blit highscore on screen
                    textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                    overobj = textbasics.render("You're in the Top 10!", True, RED)
                    overrect = overobj.get_rect()
                    overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                    overrect.centery = DISPLAYSURF.get_rect().centery - 90
                    DISPLAYSURF.blit(overobj, overrect)
                    os.system('initialstk.py')
                    end_it = True
                pygame.display.flip()
            #blit you win on screen
            overobj = textbasics.render('You Win!', True, RED)
            overrect = overobj.get_rect()
            overrect.centerx = DISPLAYSURF.get_rect().centerx+90
            overrect.centery = DISPLAYSURF.get_rect().centery - 45
            DISPLAYSURF.blit(overobj, overrect)
            #blit the score
            scoreobj=textbasics.render('Score: '+str(score), True, RED)
            scorerect=scoreobj.get_rect()
            scorerect.centerx=DISPLAYSURF.get_rect().centerx+90
            scorerect.centery=DISPLAYSURF.get_rect().centery
            DISPLAYSURF.blit(scoreobj, scorerect)
            #blit play again
            againobj=textbasics.render('Click to Play Again', True, GREEN)
            againrect=againobj.get_rect()
            againrect.centerx=DISPLAYSURF.get_rect().centerx+90
            againrect.centery=DISPLAYSURF.get_rect().centery+90
            DISPLAYSURF.blit(againobj, againrect)
            #blit quit
            quitobj=textbasics.render('QUIT', True, GREEN)
            quitrect=quitobj.get_rect()
            quitrect.centerx=DISPLAYSURF.get_rect().centerx+90
            quitrect.centery=DISPLAYSURF.get_rect().centery+135
            DISPLAYSURF.blit(quitobj, quitrect)

            textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 30)
            topobj=textbasics.render('TOP TEN',True,WHITE)
            toprect=topobj.get_rect()
            toprect.centerx=DISPLAYSURF.get_rect().centerx-225
            toprect.centery=DISPLAYSURF.get_rect().centery-170
            DISPLAYSURF.blit(topobj,toprect)

            initials=[]
            file=open('initials.txt','r')
            for line in file:
                line=line.replace('\n','')
                initials.append(line)
            file.close()
            initials.reverse()

            if len(initials)>10:
                del initials[-1]
            x=-170
            for a,b in zip(listscore,initials):
                y=str((a,b))
                y=y.replace('(','')
                y=y.replace(')','')
                y=y.replace("'",'')
                y=y.replace(',',' - ')
                scobj=textbasics.render(str(y),True,WHITE)
                scorect=scobj.get_rect()
                scorect.centerx=DISPLAYSURF.get_rect().centerx-225
                x=x+35
                scorect.centery=DISPLAYSURF.get_rect().centery+(x)
                DISPLAYSURF.blit(scobj,scorect)

            for event in pygame.event.get():
                #if click screen, go to start screen
                if event.type==MOUSEBUTTONDOWN:
                    #find position of mouse
                    #if mouse says click again
                    x,y=pygame.mouse.get_pos()
                    if x>340 and x<640 and y>310 and y<355:
                        end_it=True
                        music.stop()
                        cutscene()
                    #if mouse says quit
                    if x>445 and x<535 and y>365 and y<400:
                        end_it=True
                        pygame.quit()
                        sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==K_RETURN:
                        end_it=True
                        music.stop()
                        cutscene()
                    #when the key is pressed, change level
                    if event.key==K_1:
                        end_it=True
                        easygame()
                    if event.key==K_2:
                        end_it=True
                        mediumgame()
                    if event.key==K_3 or event.key==K_4:
                        end_it=True
                        hardgame()
                    if event.key==K_5 or event.key==K_6:
                        end_it=True
                        hardgame2()
                    if event.key==K_7 or event.key==K_8:
                        end_it=True
                        obstaclegame()
                    if event.key==K_9 or event.key==K_0:
                        end_it=True
                        hardobstaclegame()
                    if event.key==K_Q:
                        pygame.quit()
                        sys.exit()
                # if quit, exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
    if len(snake)<=1:
        gameover(music,snake)
    
    for s in snake:
        for a in food:
            if s.rect.colliderect(a): #if snake collides with green apple
                sound.play() #play sound
                #remove apple from list and sprites list
                food.remove(a)
                pics.remove(a)
                #remove box on snake
                x=snake.pop() #remove end of snake from list and sprites list
                pics.remove(x)
                score-=1 #-1 from score
                break

    for s in badsnake:
        for a in food:
            if s.rect.colliderect(a): #if snake collides with green apple                
                sound.play() #play sound
                #remove apple from list and sprites list
                food.remove(a)
                pics.remove(a)
                #remove box on snake
                y=badsnake.pop() #remove end of snake from list and sprites list
                pics.remove(y)
                break
                
#checks for collision and adds points
def collision2(badsnake,food,pics,sound):
    global score
    for s in badsnake:
        for a in food:
            #if collided with red apple
            if s.rect.colliderect(a):
                sound.play() #play sound
                #remove from lists
                food.remove(a)
                pics.remove(a)
                #add new box on snake
                x = (x_change + margin)
                y = 30
                segment = AISnake(x, y)
                #add to lists
                badsnake.append(segment)
                pics.add(segment)

def specialcollision2(badsnake,food,pics,sound):
    global score
    global ticker
    for s in badsnake:
        for a in food:
            if s.rect.colliderect(a): #if snake collides with green apple
                sound.play() #play sound
                #remove apple from list and sprites list
                food.remove(a)
                pics.remove(a)
                #remove box on snake
                y=badsnake.pop() #remove end of snake from list and sprites list
                pics.remove(y)
                #ticker+=0.5

#create obstacles
def obstacles(obstlist,spriteslist):
    #one
    rectx=50
    recty=82
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=70
    recty=82
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=50
    recty=102
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=70
    recty=102
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)
    #two
    rectx=155
    recty=253
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=155
    recty=273
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=175
    recty=273
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=175
    recty=253
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)
    #three
    rectx=345
    recty=378
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=345
    recty=358
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=365
    recty=378
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=365
    recty=358
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)
    #four
    rectx=677
    recty=164
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=677
    recty=144
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=697
    recty=164
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=697
    recty=144
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)
    #five
    rectx=567
    recty=278
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=587
    recty=278
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=587
    recty=298
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=567
    recty=298
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)
    #six
    rectx=345
    recty=55
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=325
    recty=55
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=325
    recty=35
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

    rectx=345
    recty=35
    obst=Obstacle(rectx,recty)
    obstlist.append(obst)
    spriteslist.add(obst)

#check obstacle collision
def obstaclecollision(snake,music,route,a,b,obstlist):
    global score
    global ticker
    for s in snake:
        for i in obstlist:
            if s.rect.colliderect(i):
                gameover(music,snake)

#check the borders and snake to snake collisions
def check(badsnake,snake,route,pics,music,badroute,x,y,sm,w):
    dead=False #keeps track whether or not he's dead
    for s in snake: #if he goes past the borders set dead to true
        if s.rect.x>=780:
            dead=True
        elif s.rect.x<=0:
            dead=True
        if s.rect.y>=480:
            dead=True
        elif s.rect.y<=0:
            dead=True
            
    for s in snake: #if player collides with bad snake, set dead to true
        for b in badsnake:
            if s.rect.colliderect(b):
                dead=True

    if dead==True: #if dead is true
        gameover(music,snake) #go to gameover

    #figure out if the snake hit himself or not
    #if yes, gameover
    if 'left' in route and 'right' in route:
        gameover(music,snake)
    elif 'up' in route and 'down' in route:
        gameover(music,snake)

def checkAI2(badsnake, snake,route,pics,music,badroute,x,y,sm,w):
    dead=False #keeps track whether or not he's dead
    for s in snake: #if he goes past the borders set dead to true
        if s.rect.x>=780:
            dead=True
        elif s.rect.x<=0:
            dead=True
        if s.rect.y>=480:
            dead=True
        elif s.rect.y<=0:
            dead=True
            
    for s in snake: #if player collides with bad snake, set dead to true
        for b in badsnake:
            if s.rect.colliderect(b):
                dead=True

    if dead==True: #if dead is true
        gameover(music,snake) #go to gameover

    #figure out if the snake hit himself or not
    #if yes, gameover
    if 'left' in route and 'right' in route:
        gameover(music,snake)
    elif 'up' in route and 'down' in route:
        gameover(music,snake)

#check for gameover with length of snake          
def gameover(gm,snake):
    global score
    global level
    
    #when snake dies...
    listscore=[]
    #open scores file
    file = open('highscores.txt', 'r')
    for line in file:
        listscore.append(int(line)) #add scores to a list
    listscore.append(score) #add score to a list
    listscore = sorted(listscore, reverse=True) #sort list
    file.close()

    del listscore[-1]

    if score>=listscore[0]: #if the score is >=highscore
        end_it = False
        while (end_it == False):
            # blit highscore on screen
            textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
            overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
            overrect = overobj.get_rect()
            overrect.centerx = DISPLAYSURF.get_rect().centerx+90
            overrect.centery = DISPLAYSURF.get_rect().centery - 135
            DISPLAYSURF.blit(overobj, overrect)
            os.system('initialstk.py')
            end_it=True
        pygame.display.flip()
    elif score>=listscore[-1]:
        end_it=False
        while (end_it==False):
            textbasics=pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
            overobj = textbasics.render("You're in the Top 10!", True, RED)
            overrect = overobj.get_rect()
            overrect.centerx = DISPLAYSURF.get_rect().centerx+90
            overrect.centery = DISPLAYSURF.get_rect().centery - 135
            DISPLAYSURF.blit(overobj, overrect)
            os.system('initialstk.py')
            end_it=True
        pygame.display.flip()

    # if len of scores is greater than 10, make it 10
    if len(listscore) > 10:
        del listscore[-1]

    # write list to file to update scores
    file = open('highscores.txt', 'w')
    for i in listscore:
        file.write(str(i) + '\n')
    file.close()

    end_it = False
    while (end_it == False):
        #blit game over on screen
        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)        
        overobj = textbasics.render('Game Over', True, RED)
        overrect = overobj.get_rect()
        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
        overrect.centery = DISPLAYSURF.get_rect().centery - 45
        DISPLAYSURF.blit(overobj, overrect)
        #blit the score
        scoreobj=textbasics.render('Score: '+str(score), True, RED)
        scorerect=scoreobj.get_rect()
        scorerect.centerx=DISPLAYSURF.get_rect().centerx+90
        scorerect.centery=DISPLAYSURF.get_rect().centery
        DISPLAYSURF.blit(scoreobj, scorerect)
        #blit play again
        scoreobj=textbasics.render('Click to Play Again', True, GREEN)
        scorerect=scoreobj.get_rect()
        scorerect.centerx=DISPLAYSURF.get_rect().centerx+90
        scorerect.centery=DISPLAYSURF.get_rect().centery+90
        DISPLAYSURF.blit(scoreobj, scorerect)
        #blit quit
        quitobj=textbasics.render('QUIT', True, GREEN)
        quitrect=quitobj.get_rect()
        quitrect.centerx=DISPLAYSURF.get_rect().centerx+90
        quitrect.centery=DISPLAYSURF.get_rect().centery+135
        DISPLAYSURF.blit(quitobj, quitrect)

        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 30)
        topobj=textbasics.render('TOP TEN',True,WHITE)
        toprect=topobj.get_rect()
        toprect.centerx=DISPLAYSURF.get_rect().centerx-225
        toprect.centery=DISPLAYSURF.get_rect().centery-170
        DISPLAYSURF.blit(topobj,toprect)

        initials=[]
        file=open('initials.txt','r')
        for line in file:
            line=line.replace('\n','')
            initials.append(line)
        file.close()
        initials.reverse()

        if len(initials)>10:
            del initials[-1]
        x=-170
        for a,b in zip(listscore,initials):
            y=str((a,b))
            y=y.replace('(','')
            y=y.replace(')','')
            y=y.replace("'",'')
            y=y.replace(',',' - ')
            scobj=textbasics.render(str(y),True,WHITE)
            scorect=scobj.get_rect()
            scorect.centerx=DISPLAYSURF.get_rect().centerx-225
            x=x+35
            scorect.centery=DISPLAYSURF.get_rect().centery+(x)
            DISPLAYSURF.blit(scobj,scorect)

        for event in pygame.event.get():
            #if click screen, go to start screen
            if event.type==MOUSEBUTTONDOWN:
                #find position of mouse
                #if mouse says click again
                x,y=pygame.mouse.get_pos()
                if x>340 and x<640 and y>310 and y<355:
                    score = 0
                    level=1
                    gm.stop()
                    cutscene()
                #if mouse says quit
                if x>445 and x<535 and y>365 and y<400:
                    pygame.quit()
                    sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==K_RETURN:
                    end_it=True
                    gm.stop()
                    cutscene()
                #when the key is pressed, change level
                if event.key==K_1:
                    end_it=True
                    easygame()
                if event.key==K_2:
                    end_it=True
                    mediumgame()
                if event.key==K_3 or event.key==K_4:
                    end_it=True
                    hardgame()
                if event.key==K_5 or event.key==K_6:
                    end_it=True
                    hardgame2()
                if event.key==K_7 or event.key==K_8:
                    end_it=True
                    obstaclegame()
                if event.key==K_9 or event.key==K_0:
                    end_it=True
                    hardobstaclegame()
                if event.key==K_q:
                    pygame.quit()
                    sys.exit()
            # if quit, exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

def credit(): ###############################
    pygame.init()
    pygame.mixer.init()

    WHITE=(255,255,255)
    
    #set screen
    DISPLAYSURF=pygame.display.set_mode((800,500))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption('Snake')

    #sprite list
    all_sprites_list=pygame.sprite.Group()

    image=pygame.image.load('unicat.jpg')
    #DISPLAYSURF.blit(image,(250, 125))

    all_sprites_list.draw(image)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.flip()

    for ent in all_sprites_list:  # update all
        ent.update()

    #draw everything in list
    all_sprites_list.draw(DISPLAYSURF)

    time.sleep(2)
    cutscene()

def cutscene():
    global score
    global level
    global create
    global ticker

    pygame.init()
    pygame.mixer.init()

    BG=(0,0,0)
    BROWN=(139,69,19)
    WHITE=(255,255,255)
    RED=(255,0,0)
    GREEN=(0,255,0)
    BLUE=(0,0,225)

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    bgmusic.play(-1,0)
    bgmusic.set_volume(0.3)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3
    create=5

    #list to keep track of apples and direction
    Apples=[]
    BadApples=[]
    Direction=['right']
    AIDirection=['right']

    a_change = snakewidth + margin
    b_change = 0
    x_change = snakewidth + margin
    y_change = 0   
    
    clock=pygame.time.Clock()

    #set screen
    DISPLAYSURF=pygame.display.set_mode((800,500))
    DISPLAYSURF.fill(BG)
    pygame.display.set_caption('Snake')

    #sprite list
    all_sprites_list=pygame.sprite.Group()

    #starter snake - player
    snake_segments=[]
    for i in range(3):
        x=(x_change+margin)*i+5
        y=445
        segment=Snake(x,y)
        #add segment to sprites list and snake list
        snake_segments.append(segment)
        all_sprites_list.add(segment)
    #starter snake - AI
    badsnake_segments = []
    for i in range(3):
        a = (a_change + margin) * i +5
        b = 35
        segment = AISnake(a, b)
        # add segment to sprites list and badsnake list
        badsnake_segments.append(segment)
        all_sprites_list.add(segment)

    while True:
        #check(badsnake_segments,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin)  # check lives
        collision(badsnake_segments,snake_segments, Apples,all_sprites_list,bite) #check for collisions with apple
        #specialcollision(badsnake_segments,snake_segments, BadApples,all_sprites_list,bite,bgmusic) #check for collision with special apple

        #blit level on screen
        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 30)
        overobj = textbasics.render('Press Space to Start Game', True, RED)
        overrect = overobj.get_rect()
        overrect.centerx = DISPLAYSURF.get_rect().centerx
        overrect.centery = DISPLAYSURF.get_rect().centery +135
        DISPLAYSURF.blit(overobj, overrect)

        #instructions, blit to center
        instobj=textbasics.render('Instructions',True, GREEN)
        instrect=instobj.get_rect()
        instrect.centerx=DISPLAYSURF.get_rect().centerx
        instrect.centery=DISPLAYSURF.get_rect().centery+45
        DISPLAYSURF.blit(instobj,instrect)

        #blit quit
        quitobj=textbasics.render('QUIT', True, GREEN)
        quitrect=quitobj.get_rect()
        quitrect.centerx=DISPLAYSURF.get_rect().centerx
        quitrect.centery=DISPLAYSURF.get_rect().centery+90
        DISPLAYSURF.blit(quitobj, quitrect)

        #highscore, blit in center
        scores=[]
        file=open('highscores.txt','r')
        for line in file:
            line=line.strip('\n')
            scores.append(int(line))
        blitscore=max(scores)

        #highscore font, blit in center
        overobj = textbasics.render('HIGHSCORE: '+str(blitscore), True, GREEN)
        overrect = overobj.get_rect()
        overrect.centerx = DISPLAYSURF.get_rect().centerx
        overrect.centery = DISPLAYSURF.get_rect().centery - 135
        DISPLAYSURF.blit(overobj, overrect)

        #title font, blit in center
        titleobj = textbasics.render('SNAKE', True, GREEN)
        titlerect = titleobj.get_rect()
        titlerect.centerx = DISPLAYSURF.get_rect().centerx
        titlerect.centery = DISPLAYSURF.get_rect().centery-180
        DISPLAYSURF.blit(titleobj,titlerect)

        for event in pygame.event.get():
            #if mousebuttondown or space pressed start game
            if event.type==MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                #print(pygame.mouse.get_pos())                    
                #305,495
                #275,310
                if x>305 and x<495 and y>275 and y<310:
                    end_it=True
                    beginmusic.stop()
                    instructions()
                if x>365 and x<435 and y>325 and y<352:
                    pygame.quit()
                    sys.exit()
            elif event.type==pygame.KEYDOWN:
                #when the key is pressed, change direction
                if event.key==K_1:
                    end_it=True
                    easygame()
                if event.key==K_2:
                    end_it=True
                    mediumgame()
                if event.key==K_3 or event.key==K_4:
                    end_it=True
                    hardgame()
                if event.key==K_5 or event.key==K_6:
                    end_it=True
                    hardgame2()
                if event.key==K_7 or event.key==K_8:
                    end_it=True
                    obstaclegame()
                if event.key==K_9 or event.key==K_0:
                    end_it=True
                    hardobstaclegame()
                if event.key==K_SPACE:
                    end_it=True
                    easygame()
                if event.key==K_q:
                    pygame.quit()
                    sys.exit()
            #if quit, exit
            elif event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.flip()

        pygame.display.flip()

        if 'up' in AIDirection and 'down' in AIDirection: #determines whether the AI snake will run into itself
            for b in badsnake_segments:
                if b.rect.x>400:
                    direction = 'left'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin) * -1
                    b_change = 0
                    break
                if b.rect.x<400:
                    direction = 'right'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin)
                    b_change = 0
                    break
            AIDirection.pop(0) #keep track of AI direction

            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)
            
            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        if 'left' in AIDirection and 'right' in AIDirection: #determines whether the AI snake will run into itself
            for b in badsnake_segments:
                if b.rect.y>250:
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakewidth + margin) * -1
                    break
                if b.rect.x<250:
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakewidth + margin)
                    break
            AIDirection.pop() #keep track of AI direction
            
            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)

            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        if 'up' in Direction and 'down' in Direction: #determines whether the AI snake will run into itself
            for b in snake_segments:
                if b.rect.x>400:
                    direction = 'left'
                    Direction.append(direction)
                    x_change = (snakewidth + margin) * -1
                    y_change = 0
                    break
                if b.rect.x<400:
                    direction = 'right'
                    Direction.append(direction)
                    x_change = (snakewidth + margin)
                    y_change = 0
                    break
            Direction.pop(0) #keep track of AI direction

            old_segment=snake_segments.pop()
            all_sprites_list.remove(old_segment)
            
            x = snake_segments[0].rect.x + x_change
            y = snake_segments[0].rect.y + y_change
            segment = Snake(x, y)
            # add new box onto list
            snake_segments.insert(0, segment)
            all_sprites_list.add(segment)

        if 'left' in Direction and 'right' in Direction: #determines whether the AI snake will run into itself
            for b in snake_segments:
                if b.rect.y>250:
                    direction = 'up'
                    Direction.append(direction)
                    x_change = 0
                    y_change = (snakewidth + margin) * -1
                    break
                if b.rect.x<250:
                    direction = 'down'
                    Direction.append(direction)
                    x_change = 0
                    y_change = (snakewidth + margin)
                    break
            Direction.pop() #keep track of AI direction
            
            old_segment=snake_segments.pop()
            all_sprites_list.remove(old_segment)

            x = snake_segments[0].rect.x + x_change
            y = snake_segments[0].rect.y + y_change
            segment = Snake(x, y)
            # add new box onto list
            snake_segments.insert(0, segment)
            all_sprites_list.add(segment)

        if create<=0: #if create is less than 0 create new apples
            applex=random.randint(0,770)
            appley=random.randint(0,470)
            for s in snake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            for s in badsnake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            if applex<0:
                applex=0
            if applex>780:
                applex=780
            if appley<=0:
                appley=0
            if appley>=480:
                appley=480
            apple=Apple(applex,appley)
            Apples.append(apple)
            all_sprites_list.add(apple)
            create=30
                    
        for s in snake_segments: #follow the apple up or down
            for a in Apples:
                if (s.rect.x < a.rect.x and s.rect.y > a.rect.y):
                    direction = 'up'
                    Direction.append(direction)
                    x_change = 0
                    y_change = (snakeheight + margin) * -1
                    break

                elif (s.rect.x < a.rect.x and s.rect.y < a.rect.y):
                    direction = 'down'
                    Direction.append(direction)
                    x_change = 0
                    y_change = (snakeheight + margin)
                    break

                elif (s.rect.x > a.rect.x and s.rect.y > a.rect.y):
                    direction = 'up'
                    Direction.append(direction)
                    x_change = 0
                    y_change = (snakeheight + margin) * -1
                    break
                
                elif (s.rect.x > a.rect.x and s.rect.y < a.rect.y):
                    direction = 'down'
                    Direction.append(direction)
                    x_change = 0
                    y_change = (snakeheight + margin)
                    break
        
            if len(Direction)>2:
                Direction.pop(0) #keep track of AI direction
        
        for s in snake_segments: #if the apple and the snake are at the same position - ish, go to apple
            for a in Apples:
                if (s.rect.y <= (a.rect.y + 20)) and (s.rect.y >= (a.rect.y - 20)) and ((s.rect.x <= a.rect.x)):
                    direction = 'right'
                    Direction.append(direction)
                    x_change = (snakewidth + margin)
                    y_change = 0
                    break
                if (s.rect.y <= (a.rect.y + 20)) and (s.rect.y >= (a.rect.y - 20)) and ((s.rect.x >= a.rect.x)):
                    direction = 'left'
                    Direction.append(direction)
                    x_change = (snakewidth + margin) * -1
                    y_change = 0
                    break
                
            if len(Direction)>2:
                Direction.pop(0) #keep track of AI direction
                    
        #if he goes past the borders, reset
        for s in badsnake_segments:
            if s.rect.x > 800 and s.rect.y > 250:
                s.rect.x = 780
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            if s.rect.x > 800 and s.rect.y < 250:
                s.rect.x = 780
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            if s.rect.x < 0 and s.rect.y > 250:
                s.rect.x = 0
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            if s.rect.x < 0 and s.rect.y < 250:
                s.rect.x = 0
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            
        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction
                
        for s in badsnake_segments:
            if s.rect.y > 500 and s.rect.x < 400:
                s.rect.y = 480
                direction = 'right'
                AIDirection.append(direction)
                a_change = (snakewidth + margin)
                b_change = 0
                break
            if s.rect.y > 500 and s.rect.x > 400:
                s.rect.y = 480
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break
            if s.rect.y < 0 and s.rect.x < 400:
                s.rect.y = 0
                direction = 'right'
                AIDirection.append(direction)
                a_change = (snakewidth + margin)
                b_change = 0
                break
            if s.rect.y < 0 and s.rect.x > 400:
                s.rect.y = 0
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break

        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction

        #if he goes past the borders, reset
        for s in snake_segments:
            if s.rect.x > 800 and s.rect.y > 250:
                s.rect.x = 780
                direction = 'up'
                Direction.append(direction)
                x_change = 0
                y_change = (snakeheight + margin) * -1
                break
            if s.rect.x > 800 and s.rect.y < 250:
                s.rect.x = 780
                direction = 'down'
                Direction.append(direction)
                x_change = 0
                y_change = (snakeheight + margin)
                break
            if s.rect.x < 0 and s.rect.y > 250:
                s.rect.x = 0
                direction = 'up'
                Direction.append(direction)
                x_change = 0
                y_change = (snakeheight + margin) * -1
                break
            if s.rect.x < 0 and s.rect.y < 250:
                s.rect.x = 0
                direction = 'down'
                Direction.append(direction)
                x_change = 0
                y_change = (snakeheight + margin)
                break
            
        if len(Direction)>2:
            Direction.pop(0) #keep track of AI direction
                
        for s in snake_segments:
            if s.rect.y > 500 and s.rect.x < 400:
                s.rect.y = 480
                direction = 'right'
                Direction.append(direction)
                x_change = (snakewidth + margin)
                y_change = 0
                break
            if s.rect.y > 500 and s.rect.x > 400:
                s.rect.y = 480
                direction = 'left'
                Direction.append(direction)
                x_change = (snakewidth + margin) * -1
                y_change = 0
                break
            if s.rect.y < 0 and s.rect.x < 400:
                s.rect.y = 0
                direction = 'right'
                Direction.append(direction)
                x_change = (snakewidth + margin)
                y_change = 0
                break
            if s.rect.y < 0 and s.rect.x > 400:
                s.rect.y = 0
                direction = 'left'
                Direction.append(direction)
                x_change = (snakewidth + margin) * -1
                y_change = 0
                break

        if len(Direction)>2:
            Direction.pop(0) #keep track of AI direction

        x = snake_segments[0].rect.x + x_change
        y = snake_segments[0].rect.y + y_change
        segment = Snake(x, y)
        # add new box onto list
        snake_segments.insert(0, segment)
        all_sprites_list.add(segment)

        x = badsnake_segments[0].rect.x + a_change
        y = badsnake_segments[0].rect.y + b_change
        badsegment = AISnake(x, y)
        # add new box onto list
        badsnake_segments.insert(0, badsegment)
        all_sprites_list.add(badsegment)

        try:
            #continuously update snake to maintain length
            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)
            old_segment=snake_segments.pop()
            all_sprites_list.remove(old_segment)
        except:
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    #when the key is pressed, change level
                    if event.key==K_1:
                        end_it=True
                        easygame()
                    if event.key==K_2:
                        end_it=True
                        mediumgame()
                    if event.key==K_3 or event.key==K_4:
                        end_it=True
                        hardgame()
                    if event.key==K_5 or event.key==K_6:
                        end_it=True
                        hardgame2()
                    if event.key==K_7 or event.key==K_8:
                        end_it=True
                        obstaclegame()
                    if event.key==K_9 or event.key==K_0:
                        end_it=True
                        hardobstaclegame()

                # if quit, exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
                
        #draw everything
        DISPLAYSURF.fill(BG)

        for ent in all_sprites_list:  # update all
            ent.update()

        #draw everything in list
        all_sprites_list.draw(DISPLAYSURF)

        clock.tick(ticker)

        create-=1 #subtract from create to keep track of apple spawning

def instructions():
    pygame.init()
    pygame.mixer.init()

    #colors
    BG=(0,0,0)
    BROWN=(139,69,19)
    WHITE=(255,255,255)
    RED=(255,0,0)
    GREEN=(0,255,0)
    BLUE=(0,0,225)

    #set screen
    DISPLAYSURF = pygame.display.set_mode((800, 500))
    DISPLAYSURF.fill(BG)
    pygame.display.set_caption('Snake')

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    beginmusic.play(-1,0)
    beginmusic.set_volume(0.3)

    end_it=False
    while (end_it==False):

        text = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 25)

        #instructions, blit to start screen
        titleobj = text.render('INSTRUCTIONS', True, WHITE)
        titlerect = titleobj.get_rect()
        titlerect.centerx = DISPLAYSURF.get_rect().centerx
        titlerect.centery = DISPLAYSURF.get_rect().centery-200
        DISPLAYSURF.blit(titleobj, titlerect)
        
        moveobj = text.render('1. Use WASD to move up and down', True, WHITE)
        moverect = moveobj.get_rect()
        moverect.centerx = DISPLAYSURF.get_rect().centerx-90
        moverect.centery = DISPLAYSURF.get_rect().centery-160
        DISPLAYSURF.blit(moveobj, moverect)

        goalobj = text.render('2. Try to get five points (or apples) per level', True, WHITE)
        goalrect = moveobj.get_rect()
        goalrect.centerx = DISPLAYSURF.get_rect().centerx-90
        goalrect.centery = DISPLAYSURF.get_rect().centery-120
        DISPLAYSURF.blit(goalobj, goalrect)

        badappleobj = text.render('3. Green Apples reduce score by 2 points', True, WHITE)
        badapplerect = moveobj.get_rect()
        badapplerect.centerx = DISPLAYSURF.get_rect().centerx-90
        badapplerect.centery = DISPLAYSURF.get_rect().centery-80
        DISPLAYSURF.blit(badappleobj, badapplerect)

        appleobj = text.render('4. Red apples increase score by 1 point', True, WHITE)
        applerect = moveobj.get_rect()
        applerect.centerx = DISPLAYSURF.get_rect().centerx-90
        applerect.centery = DISPLAYSURF.get_rect().centery-40
        DISPLAYSURF.blit(appleobj, applerect)
        
        AIobj = text.render('5. AI Snakes will try to eat apples and will chase you', True, WHITE)
        AIrect = moveobj.get_rect()
        AIrect.centerx = DISPLAYSURF.get_rect().centerx-90
        AIrect.centery = DISPLAYSURF.get_rect().centery
        DISPLAYSURF.blit(AIobj, AIrect)
        
        levelobj = text.render('6. Difficulty increases by level!', True, WHITE)
        levelrect = moveobj.get_rect()
        levelrect.centerx = DISPLAYSURF.get_rect().centerx-90
        levelrect.centery = DISPLAYSURF.get_rect().centery+40
        DISPLAYSURF.blit(levelobj, levelrect)

        keyobj=text.render('7. Press Enter or click to go to the next level/play again', True, WHITE)
        keyrect=moveobj.get_rect()
        keyrect.centerx=DISPLAYSURF.get_rect().centerx-90
        keyrect.centery=DISPLAYSURF.get_rect().centery+80
        DISPLAYSURF.blit(keyobj,keyrect)

        quitobj=text.render('8. Press "Q" to quit the game',True,WHITE)
        quitrect=moveobj.get_rect()
        quitrect.centerx=DISPLAYSURF.get_rect().centerx-90
        quitrect.centery=DISPLAYSURF.get_rect().centery+120
        DISPLAYSURF.blit(quitobj,quitrect)

        backobj=text.render('Click to go Back',True,WHITE)
        backrect=backobj.get_rect()
        backrect.centerx=DISPLAYSURF.get_rect().centerx
        backrect.centery=DISPLAYSURF.get_rect().centery+160
        DISPLAYSURF.blit(backobj,backrect)

        for event in pygame.event.get():
            #if click screen, go to start screen
            if event.type==MOUSEBUTTONDOWN:
                end_it=True
                beginmusic.stop()
                cutscene()
            elif event.type==pygame.KEYDOWN:
                #when the key is pressed, change direction
                if event.key==K_1:
                    end_it=True
                    easygame()
                if event.key==K_2:
                    end_it=True
                    mediumgame()
                if event.key==K_3 or event.key==K_4:
                    end_it=True
                    hardgame()
                if event.key==K_5 or event.key==K_6:
                    end_it=True
                    hardgame2()
                if event.key==K_7 or event.key==K_8:
                    end_it=True
                    obstaclegame()
                if event.key==K_9 or event.key==K_0:
                    end_it=True
                    hardobstaclegame()
                if event.key==K_q:
                    pygame.quit()
                    sys.exit()

            # if quit, exit
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

def easygame(): #level 1
    global score
    global level
    global create
    global ticker

    pygame.init()
    pygame.mixer.init()

    score=0

    BG=(0,0,0)
    BROWN=(139,69,19)
    WHITE=(255,255,255)
    RED=(255,0,0)
    GREEN=(0,255,0)
    BLUE=(0,0,225)

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    bgmusic.play(-1,0)
    bgmusic.set_volume(0.3)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3
    create=5
    z=1

    #list to keep track of apples and direction
    Apples=[]
    BadApples=[]
    Direction=['right']
    AIDirection=['right']
    #AIDirection2=['right']

    x_change=snakewidth+margin
    y_change=0

    a_change = snakewidth + margin
    b_change = 0

    f_change=snakewidth+margin
    g_change=0
    
    clock=pygame.time.Clock()

    #set screen
    DISPLAYSURF=pygame.display.set_mode((800,500))
    DISPLAYSURF.fill(BG)
    pygame.display.set_caption('Snake')

    #sprite list
    all_sprites_list=pygame.sprite.Group()

    #starter snake - player
    snake_segments=[]
    for i in range(3):
        x=(x_change+margin)*i+5
        y=250
        segment=Snake(x,y)
        #add segment to sprites list and snake list
        snake_segments.append(segment)
        all_sprites_list.add(segment)
    #starter snake - AI
    badsnake_segments = []
##    for i in range(3):
##        a = (a_change + margin) * i + 5
##        b = 35
##        segment = AISnake(a, b)
##        # add segment to sprites list and badsnake list
##        badsnake_segments.append(segment)
##        #all_sprites_list.add(segment)
    
    while True:            
        check(badsnake_segments,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin)  # check lives
        collision(badsnake_segments,snake_segments, Apples,all_sprites_list,bite) #check for collisions with apple
        #specialcollision(badsnake_segments,snake_segments, BadApples,all_sprites_list,bite) #check for collision with special apple

        #for every 5 apples, go to next level
        if (score/level)==5:
            end_it = False
            while (end_it == False):
                #blit level on screen
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                overobj = textbasics.render('Level '+str(level)+' Complete', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Next Level', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>250 and x<550 and y>310 and y<355:
                            end_it=True
                            level+=1
                            if score>=5:
                                bgmusic.stop()
                                mediumgame()
                            else:
                                bgmusic.stop()
                                easygame()
                        #if mouse says quit
                        if x>355 and x<445 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        #when the key is pressed, change level
                        if event.key==K_RETURN:
                            end_it=True
                            level+=1
                            if score>=5:
                                bgmusic.stop()
                                mediumgame()
                            else:
                                bgmusic.stop()
                                easygame()
                        if event.key==K_1:
                            end_it=True
                            easygame()
                        if event.key==K_2:
                            end_it=True
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            end_it=True
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            end_it=True
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            end_it=True
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            end_it=True
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()

        if create<=0: #if create is less than 0 create new apples
            applex=random.randint(0,770)
            appley=random.randint(0,470)
            for s in snake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            for s in badsnake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            if applex<0:
                applex=0
            if applex>780:
                applex=780
            if appley<=0:
                appley=0
            if appley>=480:
                appley=480
            if applex<140:
                applex=145
            if appley<100:
                appley=110
            apple=Apple(applex,appley)
            Apples.append(apple)
            all_sprites_list.add(apple)
            create=25

        for event in pygame.event.get(): #if quit, quit
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                #when the key is pressed, change direction
                if event.key==K_a:
                    direction='left'
                    Direction.append(direction)
                    x_change=(snakewidth+margin)*-1
                    y_change=0
                if event.key ==K_d:
                    direction='right'
                    Direction.append(direction)
                    x_change =(snakewidth+margin)
                    y_change = 0
                if event.key ==K_w:
                    direction='up'
                    Direction.append(direction)
                    x_change = 0
                    y_change =(snakeheight+margin)* -1
                if event.key ==K_s:
                    direction='down'
                    Direction.append(direction)
                    x_change = 0
                    y_change =(snakeheight+margin)
                #when the key is pressed, change level
                if event.key==K_1:
                    end_it=True
                    easygame()
                if event.key==K_2:
                    end_it=True
                    mediumgame()
                if event.key==K_3 or event.key==K_4:
                    end_it=True
                    hardgame()
                if event.key==K_5 or event.key==K_6:
                    end_it=True
                    hardgame2()
                if event.key==K_7 or event.key==K_8:
                    end_it=True
                    obstaclegame()
                if event.key==K_9 or event.key==K_0:
                    end_it=True
                    hardobstaclegame()
                if event.key==K_q:
                    pygame.quit()
                    sys.exit()

                #if there is more than two directions, remove first term in list
                if len(Direction)>2:
                    Direction.pop(0)

        old_segment = snake_segments.pop()
        all_sprites_list.remove(old_segment)

        if len(snake_segments)<=1:
            gameover(bgmusic,snake_segments)
        else: #otherwise keep going
            x = snake_segments[0].rect.x + x_change
            y = snake_segments[0].rect.y + y_change
            segment = Snake(x, y)
            # add new box onto list
            snake_segments.insert(0, segment)
            all_sprites_list.add(segment)

        #draw everything
        DISPLAYSURF.fill(BG)

        for ent in all_sprites_list:  # update all
            ent.update()

        #draw everything in list
        all_sprites_list.draw(DISPLAYSURF)

        #get font
        text = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
        #title font, blit in center
        titleobj = text.render(str(score), True, WHITE)
        titlerect = titleobj.get_rect()
        titlerect.x = 5
        titlerect.y = 5
        DISPLAYSURF.blit(titleobj,titlerect)
        pygame.display.flip()

        clock.tick(ticker)

        create-=1 #subtract from create to keep track of apple spawning

def mediumgame(): #level 2
    global score
    global level
    global create
    global ticker

    pygame.init()
    pygame.mixer.init()

    BG=(0,0,0)
    BROWN=(139,69,19)
    WHITE=(255,255,255)
    RED=(255,0,0)
    GREEN=(0,255,0)
    BLUE=(0,0,225)

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    bgmusic.play(-1,0)
    bgmusic.set_volume(0.3)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3
    create=5

    #list to keep track of apples and direction
    Apples=[]
    BadApples=[]
    Direction=['right']
    AIDirection=['right']
    AIDirection2=['right']

    x_change=snakewidth+margin
    y_change=0

    a_change = snakewidth + margin
    b_change = 0
    
    f_change=snakewidth+margin
    g_change=0
    
    clock=pygame.time.Clock()

    #set screen
    DISPLAYSURF=pygame.display.set_mode((800,500))
    DISPLAYSURF.fill(BG)
    pygame.display.set_caption('Snake')

    #sprite list
    all_sprites_list=pygame.sprite.Group()

    #starter snake - player
    snake_segments=[]
    for i in range(3):
        x=(x_change+margin)*i+5
        y=250
        segment=Snake(x,y)
        #add segment to sprites list and snake list
        snake_segments.append(segment)
        all_sprites_list.add(segment)
    #starter snake - AI
    badsnake_segments = []
    for i in range(3):
        a = (a_change + margin) * i + 5
        b = 35
        segment = AISnake(a, b)
        # add segment to sprites list and badsnake list
        badsnake_segments.append(segment)
        #all_sprites_list.add(segment)

    while True:
        check(badsnake_segments,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin)  # check lives
        collision(badsnake_segments,snake_segments, Apples,all_sprites_list,bite) #check for collisions with apple
        specialcollision(badsnake_segments,snake_segments, BadApples,all_sprites_list,bite,bgmusic) #check for collision with special apple

        #for every 5 apples, go to next level
        if (score/level)==5:
            end_it = False
            while (end_it == False):
                #blit level on screen
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                overobj = textbasics.render('Level '+str(level)+' Complete', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Next Level', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>250 and x<550 and y>310 and y<355:
                            end_it=True
                            level+=1
                            if score>=10:
                                bgmusic.stop()
                                hardgame()
                            else:
                                bgmusic.stop()
                                mediumgame()
                        #if mouse says quit
                        if x>355 and x<445 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RETURN:
                            end_it=True
                            level+=1
                            if score>=10:
                                bgmusic.stop()
                                hardgame()
                            else:
                                bgmusic.stop()
                                mediumgame()
                        #when the key is pressed, change level
                        if event.key==K_1:
                            end_it=True
                            easygame()
                        if event.key==K_2:
                            end_it=True
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            end_it=True
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            end_it=True
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            end_it=True
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            end_it=True
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()

        if create<=0: #if create is less than 0 create new apples
            applex=random.randint(0,770)
            appley=random.randint(0,470)
            for s in snake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            for s in badsnake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            if applex<0:
                applex=0
            if applex>780:
                applex=780
            if appley<=0:
                appley=0
            if appley>=480:
                appley=480
            if applex<140:
                applex=145
            if appley<100:
                appley=110
            apple=Apple(applex,appley)
            Apples.append(apple)
            all_sprites_list.add(apple)
            create=30

        if create==15: #when create is 25, add special reduction apple
            applex = random.randint(0, 770)
            appley = random.randint(0, 470)
            apple=BadApple(applex,appley)
            BadApples.append(apple)
            for s in snake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            for s in badsnake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            if applex<0:
                applex=0
            if applex>780:
                applex=780
            if appley<=0:
                appley=0
            if appley>=480:
                appley=480
            if applex<140:
                applex=145
            if appley<100:
                appley=110
            apple=BadApple(applex,appley)
            BadApples.append(apple)
            all_sprites_list.add(apple) 

        for event in pygame.event.get(): #if quit, quit
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                #when the key is pressed, change direction
                if event.key==K_a:
                    direction='left'
                    Direction.append(direction)
                    x_change=(snakewidth+margin)*-1
                    y_change=0
                if event.key ==K_d:
                    direction='right'
                    Direction.append(direction)
                    x_change =(snakewidth+margin)
                    y_change = 0
                if event.key ==K_w:
                    direction='up'
                    Direction.append(direction)
                    x_change = 0
                    y_change =(snakeheight+margin)* -1
                if event.key ==K_s:
                    direction='down'
                    Direction.append(direction)
                    x_change = 0
                    y_change =(snakeheight+margin)
                #when the key is pressed, change level
                if event.key==K_1:
                    end_it=True
                    easygame()
                if event.key==K_2:
                    end_it=True
                    mediumgame()
                if event.key==K_3 or event.key==K_4:
                    end_it=True
                    hardgame()
                if event.key==K_5 or event.key==K_6:
                    end_it=True
                    hardgame2()
                if event.key==K_7 or event.key==K_8:
                    end_it=True
                    obstaclegame()
                if event.key==K_9 or event.key==K_0:
                    end_it=True
                    hardobstaclegame()
                if event.key==K_q:
                    pygame.quit()
                    sys.exit()

                #if there is more than two directions, remove first term in list
                if len(Direction)>2:
                    Direction.pop(0)
                    
        if len(snake_segments)<=1:
            gameover(bgmusic,snake_segments)
        else: #otherwise keep going
            x = snake_segments[0].rect.x + x_change
            y = snake_segments[0].rect.y + y_change
            segment = Snake(x, y)
            # add new box onto list
            snake_segments.insert(0, segment)
            all_sprites_list.add(segment)

        old_segment = snake_segments.pop()
        all_sprites_list.remove(old_segment)

        #draw everything
        DISPLAYSURF.fill(BG)

        for ent in all_sprites_list:  # update all
            ent.update()

        #draw everything in list
        all_sprites_list.draw(DISPLAYSURF)

        #get font
        text = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
        #title font, blit in center
        titleobj = text.render(str(score), True, WHITE)
        titlerect = titleobj.get_rect()
        titlerect.x = 5
        titlerect.y = 5
        DISPLAYSURF.blit(titleobj,titlerect)
        pygame.display.flip()

        clock.tick(ticker)

        create-=1 #subtract from create to keep track of apple spawning

def hardgame(): #level 3 and 4
    global score
    global level
    global create
    global ticker

    pygame.init()
    pygame.mixer.init()

    BG=(0,0,0)
    BROWN=(139,69,19)
    WHITE=(255,255,255)
    RED=(255,0,0)
    GREEN=(0,255,0)
    BLUE=(0,0,225)

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    bgmusic.play(-1,0)
    bgmusic.set_volume(0.3)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3
    create=5

    #list to keep track of apples and direction
    Apples=[]
    BadApples=[]
    Direction=['right']
    AIDirection=['right']
    AIDirection2=['right']

    x_change=snakewidth+margin
    y_change=0

    a_change = snakewidth + margin
    b_change = 0

    f_change=snakewidth+margin
    g_change=0
    
    clock=pygame.time.Clock()

    #set screen
    DISPLAYSURF=pygame.display.set_mode((800,500))
    DISPLAYSURF.fill(BG)
    pygame.display.set_caption('Snake')

    #sprite list
    all_sprites_list=pygame.sprite.Group()

    #starter snake - player
    snake_segments=[]
    for i in range(3):
        x=(x_change+margin)*i+5
        y=445
        segment=Snake(x,y)
        #add segment to sprites list and snake list
        snake_segments.append(segment)
        all_sprites_list.add(segment)
    #starter snake - AI
    badsnake_segments = []
    for i in range(3):
        a = (a_change + margin) * i +5
        b = 35
        segment = AISnake(a, b)
        # add segment to sprites list and badsnake list
        badsnake_segments.append(segment)
        all_sprites_list.add(segment)

    while True:
        check(badsnake_segments,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin)  # check lives
        collision(badsnake_segments,snake_segments, Apples,all_sprites_list,bite) #check for collisions with apple
        specialcollision(badsnake_segments,snake_segments, BadApples,all_sprites_list,bite,bgmusic) #check for collision with special apple

        #for every 5 apples, go to next level
        if (score/level)==5:
            #print(score/level)
            #print('level one complete')
            end_it = False
            while (end_it == False):
                #blit level on screen
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                overobj = textbasics.render('Level '+str(level)+' Complete', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Next Level', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>250 and x<550 and y>310 and y<355:
                            end_it=True
                            level+=1
                            #print(level)
                            if score>=20:
                                bgmusic.stop()
                                hardgame2()
                            else:
                                bgmusic.stop()
                                hardgame()
                        #if mouse says quit
                        if x>355 and x<445 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RETURN:
                            end_it=True
                            level+=1
                            if score>=20:
                                bgmusic.stop()
                                hardgame2()
                            else:
                                bgmusic.stop()
                                hardgame()
                        #when the key is pressed, change level
                        if event.key==K_1:
                            end_it=True
                            easygame()
                        if event.key==K_2:
                            end_it=True
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            end_it=True
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            end_it=True
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            end_it=True
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            end_it=True
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()

        if 'up' in AIDirection and 'down' in AIDirection: #determines whether the AI snake will run into itself
            for b in badsnake_segments:
                if b.rect.x>400:
                    direction = 'left'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin) * -1
                    b_change = 0
                    break
                if b.rect.x<400:
                    direction = 'right'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin)
                    b_change = 0
                    break
            AIDirection.pop(0) #keep track of AI direction

            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)
            
            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        if 'left' in AIDirection and 'right' in AIDirection: #determines whether the AI snake will run into itself
            for b in badsnake_segments:
                if b.rect.y>250:
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakewidth + margin) * -1
                    break
                if b.rect.x<250:
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakewidth + margin)
                    break
            AIDirection.pop() #keep track of AI direction
            
            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)

            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        if create<=0: #if create is less than 0 create new apples
            applex=random.randint(0,770)
            appley=random.randint(0,470)
            for s in snake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            for s in badsnake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            if applex<0:
                applex=0
            if applex>780:
                applex=780
            if appley<=0:
                appley=0
            if appley>=480:
                appley=480
            apple=Apple(applex,appley)
            Apples.append(apple)
            all_sprites_list.add(apple)
            create=30

        if create==15: #when create is 25, add special reduction apple
            applex = random.randint(0, 770)
            appley = random.randint(0, 470)
            apple=BadApple(applex,appley)
            BadApples.append(apple)
            for s in snake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            for s in badsnake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            if applex<0:
                applex=0
            if applex>780:
                applex=780
            if appley<=0:
                appley=0
            if appley>=480:
                appley=480
            apple=BadApple(applex,appley)
            BadApples.append(apple)
            all_sprites_list.add(apple)

        for event in pygame.event.get(): #if quit, quit
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                #when the key is pressed, change direction
                if event.key==K_a:
                    direction='left'
                    Direction.append(direction)
                    x_change=(snakewidth+margin)*-1
                    y_change=0
                if event.key ==K_d:
                    direction='right'
                    Direction.append(direction)
                    x_change =(snakewidth+margin)
                    y_change = 0
                if event.key ==K_w:
                    direction='up'
                    Direction.append(direction)
                    x_change = 0
                    y_change =(snakeheight+margin)* -1
                if event.key ==K_s:
                    direction='down'
                    Direction.append(direction)
                    x_change = 0
                    y_change =(snakeheight+margin)
                #when the key is pressed, change level
                if event.key==K_1:
                    end_it=True
                    easygame()
                if event.key==K_2:
                    end_it=True
                    mediumgame()
                if event.key==K_3 or event.key==K_4:
                    end_it=True
                    hardgame()
                if event.key==K_5 or event.key==K_6:
                    end_it=True
                    hardgame2()
                if event.key==K_7 or event.key==K_8:
                    end_it=True
                    obstaclegame()
                if event.key==K_9 or event.key==K_0:
                    end_it=True
                    hardobstaclegame()
                if event.key==K_q:
                    pygame.quit()
                    sys.exit()

                #if there is more than two directions, remove first term in list
                if len(Direction)>2:
                    Direction.pop(0)
                    
        for s in badsnake_segments: #follow the apple up or down
            for a in Apples:
                if (s.rect.x < a.rect.x and s.rect.y > a.rect.y):
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin) * -1
                    break

                elif (s.rect.x < a.rect.x and s.rect.y < a.rect.y):
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin)
                    break

                elif (s.rect.x > a.rect.x and s.rect.y > a.rect.y):
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin) * -1
                    break
                
                elif (s.rect.x > a.rect.x and s.rect.y < a.rect.y):
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin)
                    break
        
            if len(AIDirection)>2:
                AIDirection.pop(0) #keep track of AI direction
        
        for s in badsnake_segments: #if the apple and the snake are at the same position - ish, go to apple
            for a in Apples:
                if (s.rect.y <= (a.rect.y + 20)) and (s.rect.y >= (a.rect.y - 20)) and ((s.rect.x <= a.rect.x)):
                    direction = 'right'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin)
                    b_change = 0
                    break
                if (s.rect.y <= (a.rect.y + 20)) and (s.rect.y >= (a.rect.y - 20)) and ((s.rect.x >= a.rect.x)):
                    direction = 'left'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin) * -1
                    b_change = 0
                    break
                
            if len(AIDirection)>2:
                AIDirection.pop(0) #keep track of AI direction
                    
        #if he goes past the borders, reset
        for s in badsnake_segments:
            if s.rect.x > 800 and s.rect.y > 250:
                s.rect.x = 780
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            if s.rect.x > 800 and s.rect.y < 250:
                s.rect.x = 780
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            if s.rect.x < 0 and s.rect.y > 250:
                s.rect.x = 0
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            if s.rect.x < 0 and s.rect.y < 250:
                s.rect.x = 0
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            
        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction
                
        for s in badsnake_segments:
            if s.rect.y > 500 and s.rect.x < 400:
                s.rect.y = 480
                direction = 'right'
                AIDirection.append(direction)
                a_change = (snakewidth + margin)
                b_change = 0
                break
            if s.rect.y > 500 and s.rect.x > 400:
                s.rect.y = 480
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break
            if s.rect.y < 0 and s.rect.x < 400:
                s.rect.y = 0
                direction = 'right'
                AIDirection.append(direction)
                a_change = (snakewidth + margin)
                b_change = 0
                break
            if s.rect.y < 0 and s.rect.x > 400:
                s.rect.y = 0
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break

        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction

        if len(badsnake_segments)<=1:
            end_it = False
            while (end_it == False):
                #get font
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                #highscore font, blit in center
                listscore = []
                # open scores file
                file = open('highscores.txt', 'r')
                for line in file:
                    listscore.append(int(line))  # add scores to a list
                listscore.append(score)  # add score to a list
                listscore = sorted(listscore, reverse=True)  # sort list
                file.close()

                del listscore[-1]

                if score >= listscore[0]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                elif score >= listscore[-1]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render("You're in the Top 10!", True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                #blit you win on screen
                overobj = textbasics.render('You Win!', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx+90
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Click to Play Again', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx+90
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx+90
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)  

                #blit top ten scores
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 30)
                topobj=textbasics.render('TOP TEN',True,WHITE)
                toprect=topobj.get_rect()
                toprect.centerx=DISPLAYSURF.get_rect().centerx-225
                toprect.centery=DISPLAYSURF.get_rect().centery-170
                DISPLAYSURF.blit(topobj,toprect)

                initials=[]
                file=open('initials.txt','r')
                for line in file:
                    line=line.replace('\n','')
                    initials.append(line)
                file.close()
                initials.reverse()

                if len(initials)>10:
                    del initials[-1]
                x=-170
                for a,b in zip(listscore,initials):
                    y=str((a,b))
                    y=y.replace('(','')
                    y=y.replace(')','')
                    y=y.replace("'",'')
                    y=y.replace(',',' - ')
                    scobj=textbasics.render(str(y),True,WHITE)
                    scorect=scobj.get_rect()
                    scorect.centerx=DISPLAYSURF.get_rect().centerx-225
                    x=x+35
                    scorect.centery=DISPLAYSURF.get_rect().centery+(x)
                    DISPLAYSURF.blit(scobj,scorect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #find position of mouse
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>340 and x<640 and y>310 and y<355:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        #if mouse says quit
                        if x>445 and x<535 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RETURN:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                    #when the key is pressed, change level
                        if event.key==K_1:
                            end_it=True
                            easygame()
                        if event.key==K_2:
                            end_it=True
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            end_it=True
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            end_it=True
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            end_it=True
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            end_it=True
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.flip()
        else:
            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        #figure out where the new box on snake goes
        if len(snake_segments)<=1:
            gameover(bgmusic,snake_segments)
        else: #otherwise keep going
            x = snake_segments[0].rect.x + x_change
            y = snake_segments[0].rect.y + y_change
            segment = Snake(x, y)
            # add new box onto list
            snake_segments.insert(0, segment)
            all_sprites_list.add(segment)

        try:
            #continuously update snake to maintain length -- CRASHING HERE?
            old_segment = snake_segments.pop()
            all_sprites_list.remove(old_segment)
            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)
        except:
            end_it = False
            while (end_it == False):
                #get font
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                #highscore font, blit in center
                listscore = []
                # open scores file
                file = open('highscores.txt', 'r')
                for line in file:
                    listscore.append(int(line))  # add scores to a list
                listscore.append(score)  # add score to a list
                listscore = sorted(listscore, reverse=True)  # sort list
                file.close()

                del listscore[-1]
        
                if score >= listscore[0]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                elif score >= listscore[-1]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render("You're in the Top 10!", True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                #blit you win on screen
                overobj = textbasics.render('You Win!', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx+90
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Click to Play Again', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx+90
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx+90
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)  

                #blit top ten scores
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 30)
                topobj=textbasics.render('TOP TEN',True,WHITE)
                toprect=topobj.get_rect()
                toprect.centerx=DISPLAYSURF.get_rect().centerx-225
                toprect.centery=DISPLAYSURF.get_rect().centery-170
                DISPLAYSURF.blit(topobj,toprect)

                initials=[]
                file=open('initials.txt','r')
                for line in file:
                    line=line.replace('\n','')
                    initials.append(line)
                file.close()
                initials.reverse()

                if len(initials)>10:
                    del initials[-1]
                x=-170
                for a,b in zip(listscore,initials):
                    y=str((a,b))
                    y=y.replace('(','')
                    y=y.replace(')','')
                    y=y.replace("'",'')
                    y=y.replace(',',' - ')
                    scobj=textbasics.render(str(y),True,WHITE)
                    scorect=scobj.get_rect()
                    scorect.centerx=DISPLAYSURF.get_rect().centerx-225
                    x=x+35
                    scorect.centery=DISPLAYSURF.get_rect().centery+(x)
                    DISPLAYSURF.blit(scobj,scorect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #find position of mouse
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>340 and x<640 and y>310 and y<355:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        #if mouse says quit
                        if x>445 and x<535 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RETURN:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        #when the key is pressed, change level
                        if event.key==K_1:
                            end_it=True
                            easygame()
                        if event.key==K_2:
                            end_it=True
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            end_it=True
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            end_it=True
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            end_it=True
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            end_it=True
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.flip()
                
        #draw everything
        DISPLAYSURF.fill(BG)

        for ent in all_sprites_list:  # update all
            ent.update()

        #draw everything in list
        all_sprites_list.draw(DISPLAYSURF)

        #get font
        text = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
        #title font, blit in center
        titleobj = text.render(str(score), True, WHITE)
        titlerect = titleobj.get_rect()
        titlerect.x = 5
        titlerect.y = 5
        DISPLAYSURF.blit(titleobj,titlerect)
        pygame.display.flip()

        clock.tick(ticker)

        create-=1 #subtract from create to keep track of apple spawning
        #print(AIDirection)

def hardgame2(): #level 5 and 6
    global score
    global level
    global create
    global ticker

    pygame.init()
    pygame.mixer.init()

    BG=(0,0,0)
    BROWN=(139,69,19)
    WHITE=(255,255,255)
    RED=(255,0,0)
    GREEN=(0,255,0)
    BLUE=(0,0,225)

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    bgmusic.play(-1,0)
    bgmusic.set_volume(0.3)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3
    create=5

    #list to keep track of apples and direction
    Apples=[]
    BadApples=[]
    Direction=['right']
    AIDirection=['right']
    AIDirection2=['right']

    x_change=snakewidth+margin
    y_change=0

    a_change = snakewidth + margin
    b_change = 0

    f_change=snakewidth+margin
    g_change=0
    
    clock=pygame.time.Clock()

    #set screen
    DISPLAYSURF=pygame.display.set_mode((800,500))
    DISPLAYSURF.fill(BG)
    pygame.display.set_caption('Snake')

    #sprite list
    all_sprites_list=pygame.sprite.Group()

    #starter snake - player
    snake_segments=[]
    for i in range(3):
        x=(x_change+margin)*i+5
        y=445
        segment=Snake(x,y)
        #add segment to sprites list and snake list
        snake_segments.append(segment)
        all_sprites_list.add(segment)
    #starter snake - AI
    badsnake_segments = []
    for i in range(3):
        a = (a_change + margin) * i + 5
        b = 35
        segment = AISnake(a, b)
        # add segment to sprites list and badsnake list
        badsnake_segments.append(segment)
        all_sprites_list.add(segment)

    while True:
        check(badsnake_segments,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin)  # check lives
        collision(badsnake_segments,snake_segments, Apples,all_sprites_list,bite) #check for collisions with apple
        specialcollision(badsnake_segments,snake_segments, BadApples,all_sprites_list,bite,bgmusic) #check for collision with special apple

        #for every 5 apples, go to next level
        if (score/level)==5:
            #print(score/level)
            #print('level one complete')
            end_it = False
            while (end_it == False):
                #blit level on screen
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                overobj = textbasics.render('Level '+str(level)+' Complete', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Next Level', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>250 and x<550 and y>310 and y<355:
                            end_it=True
                            level+=1
                            #print(level)
                            if score>=30:
                                bgmusic.stop()
                                obstaclegame()
                            else:
                                bgmusic.stop()
                                hardgame()
                        #if mouse says quit
                        if x>355 and x<445 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RETURN:
                            end_it=True
                            level+=1
                            if score>=30:
                                bgmusic.stop()
                                obstaclegame()
                            else:
                                bgmusic.stop()
                                hardgame2()
                        #when the key is pressed, change level
                        if event.key==K_1:
                            end_it=True
                            easygame()
                        if event.key==K_2:
                            end_it=True
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            end_it=True
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            end_it=True
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            end_it=True
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            end_it=True
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()

        if 'up' in AIDirection and 'down' in AIDirection: #determines whether the AI snake will run into itself
            for b in badsnake_segments:
                if b.rect.x>400:
                    direction = 'left'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin) * -1
                    b_change = 0
                    break
                if b.rect.x<400:
                    direction = 'right'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin)
                    b_change = 0
                    break
            AIDirection.pop(0) #keep track of AI direction

            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)
            
            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        if 'left' in AIDirection and 'right' in AIDirection: #determines whether the AI snake will run into itself
            for b in badsnake_segments:
                if b.rect.y>250:
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakewidth + margin) * -1
                    break
                if b.rect.x<250:
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakewidth + margin)
                    break
            AIDirection.pop() #keep track of AI direction
            
            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)

            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        if create<=0: #if create is less than 0 create new apples
            applex=random.randint(0,770)
            appley=random.randint(0,470)
            for s in snake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            for s in badsnake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            if applex<0:
                applex=0
            if applex>780:
                applex=780
            if appley<=0:
                appley=0
            if appley>=480:
                appley=480
            apple=Apple(applex,appley)
            Apples.append(apple)
            all_sprites_list.add(apple)
            create=30

        if create==15: #when create is 25, add special reduction apple
            applex = random.randint(0, 770)
            appley = random.randint(0, 470)
            apple=BadApple(applex,appley)
            BadApples.append(apple)
            for s in snake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            for s in badsnake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            if applex<0:
                applex=0
            if applex>780:
                applex=780
            if appley<=0:
                appley=0
            if appley>=480:
                appley=480
            apple=BadApple(applex,appley)
            BadApples.append(apple)
            all_sprites_list.add(apple)

        for event in pygame.event.get(): #if quit, quit
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                #when the key is pressed, change direction
                if event.key==K_a:
                    direction='left'
                    Direction.append(direction)
                    x_change=(snakewidth+margin)*-1
                    y_change=0
                if event.key ==K_d:
                    direction='right'
                    Direction.append(direction)
                    x_change =(snakewidth+margin)
                    y_change = 0
                if event.key ==K_w:
                    direction='up'
                    Direction.append(direction)
                    x_change = 0
                    y_change =(snakeheight+margin)* -1
                if event.key ==K_s:
                    direction='down'
                    Direction.append(direction)
                    x_change = 0
                    y_change =(snakeheight+margin)
                #when the key is pressed, change level
                if event.key==K_1:
                    easygame()
                if event.key==K_2:
                    mediumgame()
                if event.key==K_3 or event.key==K_4:
                    hardgame()
                if event.key==K_5 or event.key==K_6:
                    hardgame2()
                if event.key==K_7 or event.key==K_8:
                    obstaclegame()
                if event.key==K_9 or event.key==K_0:
                    hardobstaclegame()
                if event.key==K_q:
                    pygame.quit()
                    sys.exit()

                #if there is more than two directions, remove first term in list
                if len(Direction)>2:
                    Direction.pop(0)
                    
        for s in badsnake_segments: #follow the apple up or down
            for a in Apples:
                if (s.rect.x < a.rect.x and s.rect.y > a.rect.y):
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin) * -1
                    break

                elif (s.rect.x < a.rect.x and s.rect.y < a.rect.y):
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin)
                    break

                elif (s.rect.x > a.rect.x and s.rect.y > a.rect.y):
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin) * -1
                    break
                
                elif (s.rect.x > a.rect.x and s.rect.y < a.rect.y):
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin)
                    break
        
            if len(AIDirection)>2:
                AIDirection.pop(0) #keep track of AI direction
        
        for s in badsnake_segments: #if the apple and the snake are at the same position - ish, go to apple
            for a in Apples:
                if (s.rect.y <= (a.rect.y + 20)) and (s.rect.y >= (a.rect.y - 20)) and ((s.rect.x <= a.rect.x)):
                    direction = 'right'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin)
                    b_change = 0
                    break
                if (s.rect.y <= (a.rect.y + 20)) and (s.rect.y >= (a.rect.y - 20)) and ((s.rect.x >= a.rect.x)):
                    direction = 'left'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin) * -1
                    b_change = 0
                    break
                
            if len(AIDirection)>2:
                AIDirection.pop(0) #keep track of AI direction
                
        ###AI - chasing the player
        if len(Apples)==0: #if there isn't an apple
            for b in badsnake_segments: #follow the snake up or down
                for s in snake_segments:
                    if (b.rect.x < s.rect.x and b.rect.y > s.rect.y):
                        direction = 'up'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin) * -1
                        break

                    if (b.rect.x < s.rect.x and b.rect.y < s.rect.y):
                        direction = 'down'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)
                        break

                    if (b.rect.x > s.rect.x and b.rect.y > s.rect.y):
                        direction = 'up'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin) * -1
                        break
                    
                    if (b.rect.x > s.rect.x and b.rect.y < s.rect.y):
                        direction = 'down'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)
                        break
    
                if len(AIDirection)>2:
                    AIDirection.pop(0) #keep track of AI direction

            for b in badsnake_segments: #if the AI snake and the snake are at the same position - ish, go to snake
                for s in snake_segments:
                    if (b.rect.y <= (s.rect.y + 20)) and (b.rect.y >= (s.rect.y - 20)) and ((b.rect.x <= s.rect.x)):
                        direction = 'right'
                        AIDirection.append(direction)
                        a_change = (snakewidth + margin)
                        b_change = 0
                        break
                    if (b.rect.y <= (s.rect.y + 20)) and (b.rect.y >= (s.rect.y - 20)) and ((b.rect.x >= s.rect.x)):
                        direction = 'left'
                        AIDirection.append(direction)
                        a_change = (snakewidth + margin) * -1
                        b_change = 0
                        break
                    
                if len(AIDirection)>2:
                    AIDirection.pop(0) #keep track of AI direction
                    
        #if he goes past the borders, reset
        for s in badsnake_segments:
            if s.rect.x > 800 and s.rect.y > 250:
                s.rect.x = 770
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            if s.rect.x > 800 and s.rect.y < 250:
                s.rect.x = 770
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            if s.rect.x < 0 and s.rect.y > 250:
                s.rect.x = 0
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            if s.rect.x < 0 and s.rect.y < 250:
                s.rect.x = 0
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            
        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction
                
        for s in badsnake_segments:
            if s.rect.y > 500 and s.rect.x < 400:
                s.rect.y = 470
                direction = 'right'
                AIDirection.append(direction)
                a_change = (snakewidth + margin)
                b_change = 0
                break
            if s.rect.y > 500 and s.rect.x > 400:
                s.rect.y = 470
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break
            if s.rect.y < 0 and s.rect.x < 400:
                s.rect.y = 0
                direction = 'right'
                AIDirection.append(direction)
                a_change = (snakewidth + margin)
                b_change = 0
                break
            if s.rect.y < 0 and s.rect.x > 400:
                s.rect.y = 0
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break

        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction

        if len(badsnake_segments)<=1:
            end_it = False
            while (end_it == False):
                #get font
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                #highscore font, blit in center
                listscore = []
                # open scores file
                file = open('highscores.txt', 'r')
                for line in file:
                    listscore.append(int(line))  # add scores to a list
                listscore.append(score)  # add score to a list
                listscore = sorted(listscore, reverse=True)  # sort list
                file.close()

                del listscore[-1]

                if score >= listscore[0]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                elif score >= listscore[-1]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render("You're in the Top 10!", True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                #blit you win on screen
                overobj = textbasics.render('You Win!', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx+90
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Click to Play Again', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx+90
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx+90
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)

                #blit top ten scores
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 30)
                topobj=textbasics.render('TOP TEN',True,WHITE)
                toprect=topobj.get_rect()
                toprect.centerx=DISPLAYSURF.get_rect().centerx-225
                toprect.centery=DISPLAYSURF.get_rect().centery-170
                DISPLAYSURF.blit(topobj,toprect)

                initials=[]
                file=open('initials.txt','r')
                for line in file:
                    line=line.replace('\n','')
                    initials.append(line)
                file.close()
                initials.reverse()

                if len(initials)>10:
                    del initials[-1]
                x=-170
                for a,b in zip(listscore,initials):
                    y=str((a,b))
                    y=y.replace('(','')
                    y=y.replace(')','')
                    y=y.replace("'",'')
                    y=y.replace(',',' - ')
                    scobj=textbasics.render(str(y),True,WHITE)
                    scorect=scobj.get_rect()
                    scorect.centerx=DISPLAYSURF.get_rect().centerx-225
                    x=x+35
                    scorect.centery=DISPLAYSURF.get_rect().centery+(x)
                    DISPLAYSURF.blit(scobj,scorect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #find position of mouse
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>340 and x<640 and y>310 and y<355:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        #if mouse says quit
                        if x>445 and x<545 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RETURN:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        #when the key is pressed, change level
                        if event.key==K_1:
                            end_it=True
                            easygame()
                        if event.key==K_2:
                            end_it=True
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            end_it=True
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            end_it=True
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            end_it=True
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            end_it=True
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.flip()
        else:
            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        #figure out where the new box on snake goes
        if len(snake_segments)<=1:
            gameover(bgmusic,snake_segments)
        else: #otherwise keep going
            x = snake_segments[0].rect.x + x_change
            y = snake_segments[0].rect.y + y_change
            segment = Snake(x, y)
            # add new box onto list
            snake_segments.insert(0, segment)
            all_sprites_list.add(segment)
        try:
            #continuously update snake to maintain length
            old_segment = snake_segments.pop()
            all_sprites_list.remove(old_segment)
            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)
        except:
            end_it = False
            while (end_it == False):
                #get font
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                #highscore font, blit in center
                listscore = []
                # open scores file
                file = open('highscores.txt', 'r')
                for line in file:
                    listscore.append(int(line))  # add scores to a list
                listscore.append(score)  # add score to a list
                listscore = sorted(listscore, reverse=True)  # sort list
                file.close()

                del listscore[-1]

                if score >= listscore[0]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                elif score >= listscore[-1]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render("You're in the Top 10!", True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                #blit you win on screen
                overobj = textbasics.render('You Win!', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx+90
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Click to Play Again', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx+90
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx+90
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)  

                #blit top ten scores
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 30)
                topobj=textbasics.render('TOP TEN',True,WHITE)
                toprect=topobj.get_rect()
                toprect.centerx=DISPLAYSURF.get_rect().centerx-225
                toprect.centery=DISPLAYSURF.get_rect().centery-170
                DISPLAYSURF.blit(topobj,toprect)

                initials=[]
                file=open('initials.txt','r')
                for line in file:
                    line=line.replace('\n','')
                    initials.append(line)
                file.close()
                initials.reverse()

                if len(initials)>10:
                    del initials[-1]
                x=-170
                for a,b in zip(listscore,initials):
                    y=str((a,b))
                    y=y.replace('(','')
                    y=y.replace(')','')
                    y=y.replace("'",'')
                    y=y.replace(',',' - ')
                    scobj=textbasics.render(str(y),True,WHITE)
                    scorect=scobj.get_rect()
                    scorect.centerx=DISPLAYSURF.get_rect().centerx-225
                    x=x+35
                    scorect.centery=DISPLAYSURF.get_rect().centery+(x)
                    DISPLAYSURF.blit(scobj,scorect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #find position of mouse
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>340 and x<640 and y>310 and y<355:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        #if mouse says quit
                        if x>445 and x<535 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        #when the key is pressed, change level
                        if event.key==K_RETURN:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        if event.key==K_1:
                            end_it=True
                            easygame()
                        if event.key==K_2:
                            end_it=True
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            end_it=True
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            end_it=True
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            end_it=True
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            end_it=True
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.flip()

        #draw everything
        DISPLAYSURF.fill(BG)

        for ent in all_sprites_list:  # update all
            ent.update()

        #draw everything in list
        all_sprites_list.draw(DISPLAYSURF)

        #get font
        text = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
        #title font, blit in center
        titleobj = text.render(str(score), True, WHITE)
        titlerect = titleobj.get_rect()
        titlerect.x = 5
        titlerect.y = 5
        DISPLAYSURF.blit(titleobj,titlerect)
        pygame.display.flip()

        clock.tick(ticker)

        create-=1 #subtract from create to keep track of apple spawning
        #print(AIDirection)

def obstaclegame(): #level 7 and 8
    global score
    global level
    global create
    global ticker

    pygame.init()
    pygame.mixer.init()

    BG=(0,0,0)
    BROWN=(139,69,19)
    WHITE=(255,255,255)
    RED=(255,0,0)
    GREEN=(0,255,0)
    BLUE=(0,0,225)

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    bgmusic.play(-1,0)
    bgmusic.set_volume(0.3)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3
    create=5

    #list to keep track of apples and direction
    Apples=[]
    BadApples=[]
    Obst=[]
    Direction=['right']
    AIDirection=['right']
    AIDirection2=['right']

    x_change=snakewidth+margin
    y_change=0

    a_change = snakewidth + margin
    b_change = 0
    
    clock=pygame.time.Clock()

    #set screen
    DISPLAYSURF=pygame.display.set_mode((800,500))
    DISPLAYSURF.fill(BG)
    pygame.display.set_caption('Snake')

    #sprite list
    all_sprites_list=pygame.sprite.Group()
    
    #starter snake - player
    snake_segments=[]
    for i in range(3):
        x=(x_change+margin)*i+5
        y=445
        segment=Snake(x,y)
        #add segment to sprites list and snake list
        snake_segments.append(segment)
        all_sprites_list.add(segment)
    #starter snake - AI
    badsnake_segments = []
    for i in range(3):
        a = (a_change + margin) * i + 5
        b = 35
        segment = AISnake(a, b)
        # add segment to sprites list and badsnake list
        badsnake_segments.append(segment)
        all_sprites_list.add(segment)

    while True:
        obstacles(Obst,all_sprites_list) #create obstacles
        check(badsnake_segments,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin)  # check lives
        collision(badsnake_segments,snake_segments, Apples,all_sprites_list,bite) #check for collisions with apple
        specialcollision(badsnake_segments,snake_segments, BadApples,all_sprites_list,bite,bgmusic) #check for collision with special apple
        obstaclecollision(snake_segments,bgmusic,AIDirection,a_change,b_change,Obst) #check collision with snake and obstacle

        #for every 5 apples, go to next level
        if (score/level)==5:
            #print(score/level)
            #print('level one complete')
            end_it = False
            while (end_it == False):
                #blit level on screen
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                overobj = textbasics.render('Level '+str(level)+' Complete', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Next Level', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>250 and x<550 and y>310 and y<355:
                            end_it=True
                            level+=1
                            #print(level)
                            if score>=40:
                                bgmusic.stop()
                                hardobstaclegame()
                            else:
                                bgmusic.stop()
                                obstaclegame()
                        #if mouse says quit
                        if x>355 and x<445 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RETURN:
                            end_it=True
                            level+=1
                            if score>=40:
                                bgmusic.stop()
                                hardobstaclegame()
                            else:
                                bgmusic.stop()
                                obstaclegame()
                        #when the key is pressed, change level
                        if event.key==K_1:
                            end_it=True
                            easygame()
                        if event.key==K_2:
                            end_it=True
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            end_it=True
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            end_it=True
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            end_it=True
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            end_it=True
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    #if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()

        if 'up' in AIDirection and 'down' in AIDirection: #determines whether the AI snake will run into itself
            for b in badsnake_segments:
                if b.rect.x>400:
                    direction = 'left'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin) * -1
                    b_change = 0
                    break
                elif b.rect.x<400:
                    direction = 'right'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin)
                    b_change = 0
                    break
            AIDirection.pop(0) #keep track of AI direction

            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)
            
            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        if 'left' in AIDirection and 'right' in AIDirection: #determines whether the AI snake will run into itself
            for b in badsnake_segments:
                if b.rect.y>250:
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakewidth + margin) * -1
                    break
                elif b.rect.x<250:
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakewidth + margin)
                    break
            AIDirection.pop() #keep track of AI direction
            
            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)

            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        if create<=0: #if create is less than 0 create new apples
            applex=random.randint(0,770)
            appley=random.randint(0,470)
            for s in snake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            for s in badsnake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            if applex<0:
                applex=0
            if applex>780:
                applex=780
            if appley<=0:
                appley=0
            if appley>=480:
                appley=480
            apple=Apple(applex,appley)
            Apples.append(apple)
            all_sprites_list.add(apple)
            create=18

        if create==10: #when create is 25, add special reduction apple
            applex = random.randint(0, 770)
            appley = random.randint(0, 470)
            apple=BadApple(applex,appley)
            BadApples.append(apple)
            for s in snake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            for s in badsnake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            if applex<0:
                applex=0
            if applex>780:
                applex=780
            if appley<=0:
                appley=0
            if appley>=480:
                appley=480
            apple=BadApple(applex,appley)
            BadApples.append(apple)
            all_sprites_list.add(apple)

        for i in Obst: #check for obstacle collision with apples
            for a in Apples:
                if i.rect.colliderect(a):
                    Apples.remove(a)
                    all_sprites_list.remove(a)
        for i in Obst:
            for b in BadApples:
                if i.rect.colliderect(b):
                    BadApples.remove(b)
                    all_sprites_list.remove(b)

        #if he goes past the borders, reset
        for s in badsnake_segments:
            if s.rect.x > 800 and s.rect.y > 250:
                #print('up')
                s.rect.x = 780
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            if s.rect.x > 800 and s.rect.y < 250:
                #print('down')
                s.rect.x = 780
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            if s.rect.x < 0 and s.rect.y > 250:
                #print('up')
                s.rect.x = 0
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            if s.rect.x < 0 and s.rect.y < 250:
                #print('down')
                s.rect.x = 0
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            if s.rect.y>500:
                #print('right')
                s.rect.y = 480
                direction = 'right'
                AIDirection.append(direction)
                a_change = (snakewidth + margin)
                b_change = 0
                
        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction
                
        for s in badsnake_segments:
            if s.rect.y > 500 and s.rect.x < 400:
                #print('right')
                s.rect.y = 480
                direction = 'right'
                AIDirection.append(direction)
                a_change = (snakewidth + margin)
                b_change = 0
                break
            if s.rect.y > 500 and s.rect.x > 400:
                #print('left')
                s.rect.y = 480
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break
            if s.rect.y < 0 and s.rect.x < 400:
                #print('right')
                s.rect.y = 0
                direction = 'right'
                AIDirection.append(direction)
                a_change = (snakewidth + margin)
                b_change = 0
                break
            if s.rect.y < 0 and s.rect.x > 400:
                #print('left')
                s.rect.y = 0
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break

        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction

        for event in pygame.event.get(): #if quit, quit
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                #when the key is pressed, change direction
                if event.key==K_a:
                    direction='left'
                    Direction.append(direction)
                    x_change=(snakewidth+margin)*-1
                    y_change=0
                if event.key ==K_d:
                    direction='right'
                    Direction.append(direction)
                    x_change =(snakewidth+margin)
                    y_change = 0
                if event.key ==K_w:
                    direction='up'
                    Direction.append(direction)
                    x_change = 0
                    y_change =(snakeheight+margin)* -1
                if event.key ==K_s:
                    direction='down'
                    Direction.append(direction)
                    x_change = 0
                    y_change =(snakeheight+margin)
                #when the key is pressed, change level
                if event.key==K_1:
                    end_it=True
                    easygame()
                if event.key==K_2:
                    end_it=True
                    mediumgame()
                if event.key==K_3 or event.key==K_4:
                    end_it=True
                    hardgame()
                if event.key==K_5 or event.key==K_6:
                    end_it=True
                    hardgame2()
                if event.key==K_7 or event.key==K_8:
                    end_it=True
                    obstaclegame()
                if event.key==K_9 or event.key==K_0:
                    end_it=True
                    hardobstaclegame()
                if event.key==K_q:
                    pygame.quit()
                    sys.exit()
                #if there is more than two directions, remove first term in list
                if len(Direction)>2:
                    Direction.pop(0)

        for s in badsnake_segments: #follow the apple up or down
            for a in Apples:
                if (s.rect.x < a.rect.x and s.rect.y > a.rect.y):
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin) * -1
                    break
                if (s.rect.x < a.rect.x and s.rect.y < a.rect.y):
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin)
                    break
                if (s.rect.x > a.rect.x and s.rect.y > a.rect.y):
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin) * -1
                    break
                if (s.rect.x > a.rect.x and s.rect.y < a.rect.y):
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin)
                    break
        
            if len(AIDirection)>2:
                AIDirection.pop(0) #keep track of AI direction
        
        for s in badsnake_segments: #if the apple and the snake are at the same position - ish, go to apple
            for a in Apples:
                if (s.rect.y <= (a.rect.y + 20)) and (s.rect.y >= (a.rect.y - 20)) and ((s.rect.x <= a.rect.x)):
                    direction = 'right'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin)
                    b_change = 0
                    break
                if (s.rect.y <= (a.rect.y + 20)) and (s.rect.y >= (a.rect.y - 20)) and ((s.rect.x >= a.rect.x)):
                    direction = 'left'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin) * -1
                    b_change = 0
                    break
                
            if len(AIDirection)>2:
                AIDirection.pop(0) #keep track of AI direction

        #avoid obstacles
        for b in badsnake_segments:
            for i in Obst:
                if b.rect.colliderect(i):
                    if AIDirection[-1]=='right':
                        if b.rect.x+20>=50 and b.rect.x+20<=90:#
                            b.rect.x=25
                        if b.rect.x+20>=155 and b.rect.x+20<=195:
                            b.rect.x=130
                        if b.rect.x+20>=345 and b.rect.x+20<=385:
                            b.rect.x=320
                        if b.rect.x+20>=677 and b.rect.x+20<=717:
                            b.rect.x=652
                        if b.rect.x+20>=567 and b.rect.x+20<=607:
                            b.rect.x=542
                        if b.rect.x+20>=325 and b.rect.x+20<=365:#
                            b.rect.x=300
                        direction = 'down'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)
                        break
                    if AIDirection[-1]=='left':
                        if b.rect.x>=50 and b.rect.x<=90:
                            b.rect.x=94
                        if b.rect.x>=155 and b.rect.x<=195:
                            b.rect.x=199
                        if b.rect.x>=345 and b.rect.x<=385:
                            b.rect.x=389
                        if b.rect.x>=677 and b.rect.x<=717:
                            b.rect.x=721
                        if b.rect.x>=567 and b.rect.x<=607:
                            b.rect.x=611
                        if b.rect.x>=325 and b.rect.x<=365:
                            b.rect.x=369
                        direction = 'up'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)*-1
                        break
                    if AIDirection[-1]=='up':
                        if b.rect.y>=82 and b.rect.y<=122:  
                            b.rect.y=126
                        if b.rect.y>=253 and b.rect.y<=293:
                            b.rect.y=297
                        if b.rect.y>=358 and b.rect.y<=398:#
                            b.rect.y=402
                        if b.rect.y>=144 and b.rect.y<=184:
                            b.rect.y=188
                        if b.rect.y>=278 and b.rect.y<=308:
                            b.rect.y=312
                        if b.rect.y>=35 and b.rect.y<=75:
                            b.rect.y=79
                        direction='left'
                        AIDirection.append(direction)
                        a_change=(snakewidth + margin)*-1
                        b_change=0
                        break
                    if AIDirection[-1]=='down':
                        if b.rect.y+20>=82 and b.rect.y+20<=122:
                            b.rect.y=57
                        if b.rect.y+20>=253 and b.rect.y+20<=293:
                            b.rect.y=228
                        if b.rect.y+20>=358 and b.rect.y+20<=398:
                            b.rect.y=333
                        if b.rect.y+20>=144 and b.rect.y+20<=184:
                            b.rect.y=119
                        if b.rect.y+20>=278 and b.rect.y+20<=308:
                            b.rect.y=253
                        if b.rect.y+20>=35 and b.rect.y+20<=75:
                            b.rect.y=10
                        direction='right'
                        AIDirection.append(direction)
                        a_change=(snakewidth + margin)
                        b_change=0
                        break

        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction

        ###AI - chasing the player
        if len(Apples)<=0: #if there isn't an apple
            for b in badsnake_segments: #follow the snake up or down
                for s in snake_segments:
                    if (b.rect.x < s.rect.x and b.rect.y > s.rect.y):
                        direction = 'up'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin) * -1
                        break

                    if (b.rect.x < s.rect.x and b.rect.y < s.rect.y):
                        direction = 'down'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)
                        break

                    if (b.rect.x > s.rect.x and b.rect.y > s.rect.y):
                        direction = 'up'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin) * -1
                        break
                    
                    if (b.rect.x > s.rect.x and b.rect.y < s.rect.y):
                        direction = 'down'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)
                        break
    
                if len(AIDirection)>2:
                    AIDirection.pop(0) #keep track of AI direction

            for b in badsnake_segments: #if the AI snake and the snake are at the same position - ish, go to snake
                for s in snake_segments:
                    if (b.rect.y <= (s.rect.y + 20)) and (b.rect.y >= (s.rect.y - 20)) and ((b.rect.x <= s.rect.x)):
                        direction = 'right'
                        AIDirection.append(direction)
                        a_change = (snakewidth + margin)
                        b_change = 0
                        break
                    if (b.rect.y <= (s.rect.y + 20)) and (b.rect.y >= (s.rect.y - 20)) and ((b.rect.x >= s.rect.x)):
                        direction = 'left'
                        AIDirection.append(direction)
                        a_change = (snakewidth + margin) * -1
                        b_change = 0
                        break
                    
                if len(AIDirection)>2:
                    AIDirection.pop(0) #keep track of AI direction

        if len(badsnake_segments)<=1: #or len(badsnake_segments2)<=0:
            end_it = False
            while (end_it == False):
                #get font
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                #highscore font, blit in center
                listscore = []
                # open scores file
                file = open('highscores.txt', 'r')
                for line in file:
                    listscore.append(int(line))  # add scores to a list
                listscore.append(score)  # add score to a list
                listscore = sorted(listscore, reverse=True)  # sort list
                file.close()

                del listscore[-1]

                if score >= listscore[0]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                elif score > listscore[-1]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render("You're in the Top 10!", True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                #blit you win on screen
                overobj = textbasics.render('You Win!', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx+90
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Click to Play Again', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx+90
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx+90
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)

                #blit top ten scores
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 30)
                topobj=textbasics.render('TOP TEN',True,WHITE)
                toprect=topobj.get_rect()
                toprect.centerx=DISPLAYSURF.get_rect().centerx-225
                toprect.centery=DISPLAYSURF.get_rect().centery-170
                DISPLAYSURF.blit(topobj,toprect)

                initials=[]
                file=open('initials.txt','r')
                for line in file:
                    line=line.replace('\n','')
                    initials.append(line)
                file.close()
                initials.reverse()

                if len(initials)>10:
                    del initials[-1]
                x=-170
                for a,b in zip(listscore,initials):
                    y=str((a,b))
                    y=y.replace('(','')
                    y=y.replace(')','')
                    y=y.replace("'",'')
                    y=y.replace(',',' - ')
                    scobj=textbasics.render(str(y),True,WHITE)
                    scorect=scobj.get_rect()
                    scorect.centerx=DISPLAYSURF.get_rect().centerx-225
                    x=x+35
                    scorect.centery=DISPLAYSURF.get_rect().centery+(x)
                    DISPLAYSURF.blit(scobj,scorect)
                
                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #find position of mouse
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>340 and x<640 and y>310 and y<355:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        #if mouse says quit
                        if x>445 and x<535 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RETURN:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        #when the key is pressed, change level
                        if event.key==K_1:
                            end_it=True
                            easygame()
                        if event.key==K_2:
                            end_it=True
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            end_it=True
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            end_it=True
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            end_it=True
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            end_it=True
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.flip()
        else:
            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        if len(snake_segments)<=1:
            gameover(bgmusic,snake_segments)
        else: #otherwise keep going
            x = snake_segments[0].rect.x + x_change
            y = snake_segments[0].rect.y + y_change
            segment = Snake(x, y)
            # add new box onto list
            snake_segments.insert(0, segment)
            all_sprites_list.add(segment)

        try:
            #continuously update snake to maintain length
            old_segment = snake_segments.pop()
            all_sprites_list.remove(old_segment)
            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)
        except:
            end_it = False
            while (end_it == False):
                #get font
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                #highscore font, blit in center
                listscore = []
                # open scores file
                file = open('highscores.txt', 'r')
                for line in file:
                    listscore.append(int(line))  # add scores to a list
                listscore.append(score)  # add score to a list
                listscore = sorted(listscore, reverse=True)  # sort list
                file.close()

                del listscore[-1]

                if score >= listscore[0]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                elif score > listscore[-1]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render("You're in the Top 10!", True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                #blit you win on screen
                overobj = textbasics.render('You Win!', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx+90
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Click to Play Again', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx+90
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx+90
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)  

                #blit top ten scores
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 30)
                topobj=textbasics.render('TOP TEN',True,WHITE)
                toprect=topobj.get_rect()
                toprect.centerx=DISPLAYSURF.get_rect().centerx-225
                toprect.centery=DISPLAYSURF.get_rect().centery-170
                DISPLAYSURF.blit(topobj,toprect)

                initials=[]
                file=open('initials.txt','r')
                for line in file:
                    line=line.replace('\n','')
                    initials.append(line)
                file.close()
                initials.reverse()

                if len(initials)>10:
                    del initials[-1]
                x=-170
                for a,b in zip(listscore,initials):
                    y=str((a,b))
                    y=y.replace('(','')
                    y=y.replace(')','')
                    y=y.replace("'",'')
                    y=y.replace(',',' - ')
                    scobj=textbasics.render(str(y),True,WHITE)
                    scorect=scobj.get_rect()
                    scorect.centerx=DISPLAYSURF.get_rect().centerx-225
                    x=x+35
                    scorect.centery=DISPLAYSURF.get_rect().centery+(x)
                    DISPLAYSURF.blit(scobj,scorect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #find position of mouse
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>340 and x<640 and y>310 and y<355:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        #if mouse says quit
                        if x>445 and x<535 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RETURN:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        #when the key is pressed, change level
                        if event.key==K_1:
                            end_it=True
                            easygame()
                        if event.key==K_2:
                            end_it=True
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            end_it=True
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            end_it=True
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            end_it=True
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            end_it=True
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()
                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.flip()
                
        #draw everything
        DISPLAYSURF.fill(BG)

        for ent in all_sprites_list:  # update all
            ent.update()

        #draw everything in list
        all_sprites_list.draw(DISPLAYSURF)

        #get font
        text = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
        #title font, blit in center
        titleobj = text.render(str(score), True, WHITE)
        titlerect = titleobj.get_rect()
        titlerect.x = 5
        titlerect.y = 5
        DISPLAYSURF.blit(titleobj,titlerect)        
        
        pygame.display.flip()

        clock.tick(ticker)

        create-=1 #subtract from create to keep track of apple spawning

def hardobstaclegame(): #level 9 and 10   --- NEEDS CLICK TO PLAY AGAIN
    global score
    global level
    global create
    global ticker

    pygame.init()
    pygame.mixer.init()

    BG=(0,0,0)
    BROWN=(139,69,19)
    WHITE=(255,255,255)
    RED=(255,0,0)
    GREEN=(0,255,0)
    BLUE=(0,0,225)

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    bgmusic.play(-1,0)
    bgmusic.set_volume(0.3)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3
    create=5

    #list to keep track of apples and direction
    Apples=[]
    BadApples=[]
    Boost=[]
    Obst=[]
    Direction=['right']
    AIDirection=['right']
    AIDirection2=['right']

    x_change=snakewidth+margin
    y_change=0

    a_change = snakewidth + margin
    b_change = 0

    f_change=snakewidth + margin
    g_change=0
    
    clock=pygame.time.Clock()

    #set screen
    DISPLAYSURF=pygame.display.set_mode((800,500))
    DISPLAYSURF.fill(BG)
    pygame.display.set_caption('Snake')

    #sprite list
    all_sprites_list=pygame.sprite.Group()
    
    #starter snake - player
    snake_segments=[]
    for i in range(3):
        x=(x_change+margin)*i+5
        y=250
        segment=Snake(x,y)
        #add segment to sprites list and snake list
        snake_segments.append(segment)
        all_sprites_list.add(segment)
    #starter snake - AI
    badsnake_segments = []
    for i in range(3):
        a = (a_change + margin) * i + 5
        b = 35
        segment = AISnake(a, b)
        # add segment to sprites list and badsnake list
        badsnake_segments.append(segment)
        all_sprites_list.add(segment)
    #starter snake - AI2
    badsnake_segments2 = []
    for i in range(3):
        f = (f_change + margin) * i + 5
        g = 465
        segment = AISnake(f, g)
        # add segment to sprites list and badsnake list
        badsnake_segments2.append(segment)
        all_sprites_list.add(segment)

    while True:
        obstacles(Obst,all_sprites_list)
        check(badsnake_segments,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin)  # check lives
        checkAI2(badsnake_segments2,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin) #check lives with second AI
        collision(badsnake_segments,snake_segments, Apples,all_sprites_list,bite) #check for collisions with apple
        collision2(badsnake_segments2,Apples,all_sprites_list,bite) #check second snake for collision with apple
        specialcollision(badsnake_segments,snake_segments, BadApples,all_sprites_list,bite,bgmusic) #check for collision with special apple
        specialcollision2(badsnake_segments2,BadApples,all_sprites_list,bite) #check second snake for collision with special apple
        obstaclecollision(snake_segments,bgmusic,AIDirection,a_change,b_change,Obst) #check snake_segments collision with obstacle

        #for every 5 apples, go to next level
        if (score/level)==5:
            end_it = False
            while (end_it == False):
                #blit level on screen
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                overobj = textbasics.render('Level '+str(level)+' Complete', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Next Level', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>250 and x<550 and y>310 and y<355:
                            end_it=True
                            level+=1
                            if score>=50:
                                winobj=textbasics.render('You Win!', True, RED)
                                winrect=winobj.get_rect()
                                winrect.centerx=DISPLAYSURF.get_rect().centerx
                                winrect.centery=DISPLAYSURF.get_rect().centery-45
                                DISPLAYSURF.blit(winobj, winrect)
                                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                                scorerect=scoreobj.get_rect()
                                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                                scorerect.centery=DISPLAYSURF.get_rect().centery
                                DISPLAYSURF.blit(scoreobj, scorerect)
                                quitobj=textbasics.render('QUIT', True, GREEN)
                                quitrect=quitobj.get_rect()
                                quitrect.centerx=DISPLAYSURF.get_rect().centerx
                                quitrect.centery=DISPLAYSURF.get_rect().centery+90
                                DISPLAYSURF.blit(quitobj, quitrect)
                                x,y=pygame.mouse.get_pos()
                                if x>250 and x<550 and y>310 and y<355:
                                    bgmusic.stop()
                                    cutscene()
                            else:
                                bgmusic.stop()
                                hardobstaclegame()
                        #if mouse says quit
                        if x>355 and x<445 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RETURN:
                            end_it=True
                            level+=1
                            if score>=50:
                                winobj=textbasics.render('You Win!', True, RED)
                                winrect=winobj.get_rect()
                                winrect.centerx=DISPLAYSURF.get_rect().centerx
                                winrect.centery=DISPLAYSURF.get_rect().centery-45
                                DISPLAYSURF.blit(winobj, winrect)
                                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                                scorerect=scoreobj.get_rect()
                                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                                scorerect.centery=DISPLAYSURF.get_rect().centery
                                DISPLAYSURF.blit(scoreobj, scorerect)
                                quitobj=textbasics.render('QUIT', True, GREEN)
                                quitrect=quitobj.get_rect()
                                quitrect.centerx=DISPLAYSURF.get_rect().centerx
                                quitrect.centery=DISPLAYSURF.get_rect().centery+90
                                DISPLAYSURF.blit(quitobj, quitrect)
                                x,y=pygame.mouse.get_pos()
                                if x>250 and x<550 and y>310 and y<355:
                                    bgmusic.stop()
                                    cutscene()
                            else:
                                bgmusic.stop()
                                hardobstaclegame()
                        #when the key is pressed, change level
                        if event.key==K_1:
                            easygame()
                        if event.key==K_2:
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    #if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()

        if 'up' in AIDirection and 'down' in AIDirection: #determines whether the AI snake will run into itself
            for b in badsnake_segments:
                if b.rect.x>400:
                    direction = 'left'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin) * -1
                    b_change = 0
                    break
                elif b.rect.x<400:
                    direction = 'right'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin)
                    b_change = 0
                    break
            AIDirection.pop(0) #keep track of AI direction
        if 'up' in AIDirection2 and 'down' in AIDirection2: #determines whether the AI snake will run into itself
            for b in badsnake_segments2:
                if b.rect.x>400:
                    direction = 'left'
                    AIDirection2.append(direction)
                    f_change = (snakewidth + margin) * -1
                    g_change = 0
                    break
                elif b.rect.x<400:
                    direction = 'right'
                    AIDirection2.append(direction)
                    f_change = (snakewidth + margin)
                    g_change = 0
                    break
            AIDirection2.pop()

            old_segment=badsnake_segments2.pop()
            all_sprites_list.remove(old_segment)
            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)

            x = badsnake_segments2[0].rect.x + f_change
            y = badsnake_segments2[0].rect.y + g_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments2.insert(0, badsegment)
            all_sprites_list.add(badsegment)
            
            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        if 'left' in AIDirection and 'right' in AIDirection: #determines whether the AI snake will run into itself
            for b in badsnake_segments:
                if b.rect.y>250:
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakewidth + margin) * -1
                    break
                elif b.rect.x<250:
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakewidth + margin)
                    break
            AIDirection.pop() #keep track of AI direction
        if 'left' in AIDirection2 and 'right' in AIDirection2: #determines whether the AI snake will run into itself
            for b in badsnake_segments2:
                if b.rect.y>250:
                    direction = 'up'
                    AIDirection2.append(direction)
                    f_change = 0
                    g_change = (snakewidth + margin) * -1
                    break
                elif b.rect.x<250:
                    direction = 'down'
                    AIDirection2.append(direction)
                    f_change = 0
                    g_change = (snakewidth + margin)
                    break
            AIDirection2.pop() #keep track of AI direction
            
            old_segment=badsnake_segments2.pop()
            all_sprites_list.remove(old_segment)
            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)

            x = badsnake_segments2[0].rect.x + f_change
            y = badsnake_segments2[0].rect.y + g_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments2.insert(0, badsegment)
            all_sprites_list.add(badsegment)
            
            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        if create<=0: #if create is less than 0 create new apples
            applex=random.randint(0,770)
            appley=random.randint(0,470)
            for s in snake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            for s in badsnake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            if applex<0:
                applex=0
            if applex>780:
                applex=780
            if appley<=0:
                appley=0
            if appley>=480:
                appley=480
            apple=Apple(applex,appley)
            Apples.append(apple)
            all_sprites_list.add(apple)
            create=30

        if create==15: #when create is 25, add special reduction apple
            applex = random.randint(0, 770)
            appley = random.randint(0, 470)
            apple=BadApple(applex,appley)
            BadApples.append(apple)
            for s in snake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            for s in badsnake_segments:
                if applex>=s.rect.x and applex<=(s.rect.x+20):
                    applex+=30
                if applex>=s.rect.y and applex<=(s.rect.y+20):
                    appley+=30
            if applex<0:
                applex=0
            if applex>780:
                applex=780
            if appley<=0:
                appley=0
            if appley>=480:
                appley=480
            apple=BadApple(applex,appley)
            BadApples.append(apple)
            all_sprites_list.add(apple)       

        for i in Obst:
            for a in Apples:
                if i.rect.colliderect(a):
                    Apples.remove(a)
                    all_sprites_list.remove(a)
        for i in Obst:
            for b in BadApples:
                if i.rect.colliderect(b):
                    BadApples.remove(b)
                    all_sprites_list.remove(b)

        #if AI goes past the borders, reset
        for s in badsnake_segments:
            if s.rect.x > 800 and s.rect.y > 250:
                s.rect.x = 780
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            elif s.rect.x > 800 and s.rect.y < 250:
                s.rect.x = 780
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            elif s.rect.x < 0 and s.rect.y > 250:
                s.rect.x = 0
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            elif s.rect.x < 0 and s.rect.y < 250:
                s.rect.x = 0
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break 
        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction
                
        for s in badsnake_segments: #AI borders
            if s.rect.y > 500 and s.rect.x < 400:
                s.rect.y = 480
                direction = 'right'
                AIDirection.append(direction)
                a_change = (snakewidth + margin)
                b_change = 0
                break
            elif s.rect.y > 500 and s.rect.x > 400:
                s.rect.y = 480
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break
            elif s.rect.y < 0 and s.rect.x < 400:
                s.rect.y = 0
                direction = 'right'
                AIDirection.append(direction)
                a_change = (snakewidth + margin)
                b_change = 0
                break
            elif s.rect.y < 0 and s.rect.x > 400:
                s.rect.y = 0
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break
        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction

        #if AI2 goes past the borders, reset
        for s in badsnake_segments2:
            if s.rect.x > 800 and s.rect.y > 250:
                s.rect.x = 780
                direction = 'up'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin) * -1
                break
            elif s.rect.x > 800 and s.rect.y < 250:
                s.rect.x = 780
                direction = 'down'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin)
                break
            elif s.rect.x < 0 and s.rect.y > 250:
                s.rect.x = 0
                direction = 'up'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin) * -1
                break
            elif s.rect.x < 0 and s.rect.y < 250:
                s.rect.x = 0
                direction = 'down'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin)
                break
        if len(AIDirection2)>2:
            AIDirection2.pop(0) #keep track of AI direction
                
        for s in badsnake_segments2: #AI2 borders
            if s.rect.y > 500 and s.rect.x < 400:
                s.rect.y = 480
                direction = 'right'
                AIDirection2.append(direction)
                f_change = (snakewidth + margin)
                g_change = 0
                break
            elif s.rect.y > 500 and s.rect.x > 400:
                s.rect.y = 480
                direction = 'left'
                AIDirection2.append(direction)
                f_change = (snakewidth + margin) * -1
                g_change = 0
                break
            elif s.rect.y < 0 and s.rect.x < 400:
                s.rect.y = 0
                direction = 'right'
                AIDirection2.append(direction)
                f_change = (snakewidth + margin)
                g_change = 0
                break
            elif s.rect.y < 0 and s.rect.x > 400:
                s.rect.y = 0
                direction = 'left'
                AIDirection2.append(direction)
                f_change = (snakewidth + margin) * -1
                g_change = 0
                break
        if len(AIDirection2)>2:
            AIDirection2.pop(0) #keep track of AI2 direction

        for s in badsnake_segments: #follow the apple up or down
            for a in Apples:
                if (s.rect.x < a.rect.x and s.rect.y > a.rect.y):
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin) * -1
                    break
                elif (s.rect.x < a.rect.x and s.rect.y < a.rect.y):
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin)
                    break
                elif (s.rect.x > a.rect.x and s.rect.y > a.rect.y):
                    direction = 'up'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin) * -1
                    break
                elif (s.rect.x > a.rect.x and s.rect.y < a.rect.y):
                    direction = 'down'
                    AIDirection.append(direction)
                    a_change = 0
                    b_change = (snakeheight + margin)
                    break
            if len(AIDirection)>2:
                AIDirection.pop(0) #keep track of AI direction
        
        for s in badsnake_segments: #if the apple and the snake are at the same position - ish, go to apple
            for a in Apples:
                if (s.rect.y <= (a.rect.y + 20)) and (s.rect.y >= (a.rect.y - 20)) and ((s.rect.x <= a.rect.x)):
                    direction = 'right'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin)
                    b_change = 0
                    break
                elif (s.rect.y <= (a.rect.y + 20)) and (s.rect.y >= (a.rect.y - 20)) and ((s.rect.x >= a.rect.x)):
                    direction = 'left'
                    AIDirection.append(direction)
                    a_change = (snakewidth + margin) * -1
                    b_change = 0
                    break
            if len(AIDirection)>2:
                AIDirection.pop(0) #keep track of AI direction

        for b in badsnake_segments2: #follow the snake up or down
            for s in snake_segments:
                if (b.rect.x < s.rect.x and b.rect.y > s.rect.y):
                    direction = 'up'
                    AIDirection.append(direction)
                    f_change = 0
                    g_change = (snakeheight + margin) * -1
                    break
                elif (b.rect.x < s.rect.x and b.rect.y < s.rect.y):
                    direction = 'down'
                    AIDirection.append(direction)
                    f_change = 0
                    g_change = (snakeheight + margin)
                    break
                elif (b.rect.x > s.rect.x and b.rect.y > s.rect.y):
                    direction = 'up'
                    AIDirection.append(direction)
                    f_change = 0
                    g_change = (snakeheight + margin) * -1
                    break
                elif (b.rect.x > s.rect.x and b.rect.y < s.rect.y):
                    direction = 'down'
                    AIDirection.append(direction)
                    f_change = 0
                    g_change = (snakeheight + margin)
                    break
            if len(AIDirection2)>2:
                AIDirection2.pop(0) #keep track of AI direction

        for b in badsnake_segments2: #if the AI snake and the snake are at the same position - ish, go to snake
            for s in snake_segments:
                if (b.rect.y <= (s.rect.y + 20)) and (b.rect.y >= (s.rect.y - 20)) and ((b.rect.x <= s.rect.x)):
                    direction = 'right'
                    AIDirection.append(direction)
                    f_change = (snakewidth + margin)
                    g_change = 0
                    break
                elif (b.rect.y <= (s.rect.y + 20)) and (b.rect.y >= (s.rect.y - 20)) and ((b.rect.x >= s.rect.x)):
                    direction = 'left'
                    AIDirection.append(direction)
                    f_change = (snakewidth + margin) * -1
                    g_change = 0
                    break
            if len(AIDirection2)>2:
                AIDirection2.pop(0) #keep track of AI direction
    
        #avoid obstacles
        for b in badsnake_segments:
            for i in Obst:
                if b.rect.colliderect(i):
                    if AIDirection[-1]=='right':
                        if b.rect.x+20>=50 and b.rect.x+20<=90:#
                            b.rect.x=25
                        if b.rect.x+20>=155 and b.rect.x+20<=195:
                            b.rect.x=130
                        if b.rect.x+20>=345 and b.rect.x+20<=385:
                            b.rect.x=320
                        if b.rect.x+20>=677 and b.rect.x+20<=717:
                            b.rect.x=652
                        if b.rect.x+20>=567 and b.rect.x+20<=607:
                            b.rect.x=542
                        if b.rect.x+20>=325 and b.rect.x+20<=365:#
                            b.rect.x=300
                        direction = 'down'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)
                        break
                    if AIDirection[-1]=='left':
                        if b.rect.x>=50 and b.rect.x<=90:
                            b.rect.x=94
                        if b.rect.x>=155 and b.rect.x<=195:
                            b.rect.x=199
                        if b.rect.x>=345 and b.rect.x<=385:
                            b.rect.x=389
                        if b.rect.x>=677 and b.rect.x<=717:
                            b.rect.x=721
                        if b.rect.x>=567 and b.rect.x<=607:
                            b.rect.x=611
                        if b.rect.x>=325 and b.rect.x<=365:
                            b.rect.x=369
                        direction = 'up'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)*-1
                        break
                    if AIDirection[-1]=='up':
                        if b.rect.y>=82 and b.rect.y<=122:
                            b.rect.y=126
                        if b.rect.y>=253 and b.rect.y<=293:
                            b.rect.y=297
                        if b.rect.y>=358 and b.rect.y<=398:#
                            b.rect.y=402
                        if b.rect.y>=144 and b.rect.y<=184:
                            b.rect.y=188
                        if b.rect.y>=278 and b.rect.y<=308:
                            b.rect.y=312
                        if b.rect.y>=35 and b.rect.y<=75:
                            b.rect.y=79
                        direction='left'
                        AIDirection.append(direction)
                        a_change=(snakewidth + margin)*-1
                        b_change=0
                        break
                    if AIDirection[-1]=='down':
                        if b.rect.y+20>=82 and b.rect.y+20<=122:
                            b.rect.y=57
                        if b.rect.y+20>=253 and b.rect.y+20<=293:
                            b.rect.y=228
                        if b.rect.y+20>=358 and b.rect.y+20<=398:
                            b.rect.y=333
                        if b.rect.y+20>=144 and b.rect.y+20<=184:
                            b.rect.y=119
                        if b.rect.y+20>=278 and b.rect.y+20<=308:
                            b.rect.y=253
                        if b.rect.y+20>=35 and b.rect.y+20<=75:
                            b.rect.y=10
                        direction='right'
                        AIDirection.append(direction)
                        a_change=(snakewidth + margin)
                        b_change=0
                        break   
        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction

        #second snake avoid obstacles
        for b in badsnake_segments2:
            for i in Obst:
                if b.rect.colliderect(i):
                    if AIDirection2[-1]=='right':
                        if b.rect.x+20>=50 and b.rect.x+20<=90:#
                            b.rect.x=25
                        if b.rect.x+20>=155 and b.rect.x+20<=195:#
                            b.rect.x=130
                        if b.rect.x+20>=345 and b.rect.x+20<=385:
                            b.rect.x=320
                        if b.rect.x+20>=677 and b.rect.x+20<=717:
                            b.rect.x=652
                        if b.rect.x+20>=567 and b.rect.x+20<=607:
                            b.rect.x=542
                        if b.rect.x+20>=325 and b.rect.x+20<=365:#
                            b.rect.x=300
                        direction = 'down'
                        AIDirection2.append(direction)
                        f_change = 0
                        g_change = (snakeheight + margin)
                        break
                    if AIDirection2[-1]=='left':
                        if b.rect.x>=50 and b.rect.x<=90:
                            b.rect.x=94
                        if b.rect.x>=155 and b.rect.x<=195:
                            b.rect.x=199
                        if b.rect.x>=345 and b.rect.x<=385:
                            b.rect.x=389
                        if b.rect.x>=677 and b.rect.x<=717:
                            b.rect.x=721
                        if b.rect.x>=567 and b.rect.x<=607:
                            b.rect.x=611
                        if b.rect.x>=325 and b.rect.x<=365:
                            b.rect.x=369
                        direction = 'up'
                        AIDirection2.append(direction)
                        f_change = 0
                        g_change = (snakeheight + margin)*-1
                        break
                    if AIDirection2[-1]=='up':
                        if b.rect.y>=82 and b.rect.y<=122:
                            b.rect.y=126
                        if b.rect.y>=253 and b.rect.y<=293:
                            b.rect.y=297
                        if b.rect.y>=358 and b.rect.y<=398:#
                            b.rect.y=402
                        if b.rect.y>=144 and b.rect.y<=184:
                            b.rect.y=188
                        if b.rect.y>=278 and b.rect.y<=308:
                            b.rect.y=312
                        if b.rect.y>=35 and b.rect.y<=75:
                            b.rect.y=79
                        direction='left'
                        AIDirection2.append(direction)
                        f_change=(snakewidth + margin)*-1
                        g_change=0
                        break
                    if AIDirection2[-1]=='down':
                        if b.rect.y+20>=82 and b.rect.y+20<=122:
                            b.rect.y=57
                        if b.rect.y+20>=253 and b.rect.y+20<=293:
                            b.rect.y=228
                        if b.rect.y+20>=358 and b.rect.y+20<=398:
                            b.rect.y=333
                        if b.rect.y+20>=144 and b.rect.y+20<=184:
                            b.rect.y=119
                        if b.rect.y+20>=278 and b.rect.y+20<=308:
                            b.rect.y=253
                        if b.rect.y+20>=35 and b.rect.y+20<=75:
                            b.rect.y=10
                        direction='right'
                        AIDirection2.append(direction)
                        f_change=(snakewidth + margin)
                        g_change=0
                        break
        if len(AIDirection2)>2:
            AIDirection2.pop(0) #keep track of AI direction
                        
        for event in pygame.event.get(): #if quit, quit
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                #when the key is pressed, change direction
                if event.key==K_a:
                    direction='left'
                    Direction.append(direction)
                    x_change=(snakewidth+margin)*-1
                    y_change=0
                if event.key ==K_d:
                    direction='right'
                    Direction.append(direction)
                    x_change =(snakewidth+margin)
                    y_change = 0
                if event.key ==K_w:
                    direction='up'
                    Direction.append(direction)
                    x_change = 0
                    y_change =(snakeheight+margin)* -1
                if event.key ==K_s:
                    direction='down'
                    Direction.append(direction)
                    x_change = 0
                    y_change =(snakeheight+margin)
                #when the key is pressed, change level
                if event.key==K_1:
                    easygame()
                if event.key==K_2:
                    mediumgame()
                if event.key==K_3 or event.key==K_4:
                    hardgame()
                if event.key==K_5 or event.key==K_6:
                    hardgame2()
                if event.key==K_7 or event.key==K_8:
                    obstaclegame()
                if event.key==K_9 or event.key==K_0:
                    hardobstaclegame()
                if event.key==K_q:
                    pygame.quit()
                    sys.exit()

                #if there is more than two directions, remove first term in list
                if len(Direction)>2:
                    Direction.pop(0)

        if len(badsnake_segments)<=1 or len(badsnake_segments2)<=1:
            end_it = False
            while (end_it == False):
                #get font
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                #highscore font, blit in center
                listscore = []
                # open scores file
                file = open('highscores.txt', 'r')
                for line in file:
                    listscore.append(int(line))  # add scores to a list
                listscore.append(score)  # add score to a list
                listscore = sorted(listscore, reverse=True)  # sort list
                file.close()

                del listscore[-1]

                if score >= listscore[0]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                elif score >= listscore[-1]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render("You're in the Top 10!", True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                #blit you win on screen
                overobj = textbasics.render('You Win!', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx+90
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Click to Play Again', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx+90
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx+90
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)

                #blit top ten scores
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 30)
                topobj=textbasics.render('TOP TEN',True,WHITE)
                toprect=topobj.get_rect()
                toprect.centerx=DISPLAYSURF.get_rect().centerx-225
                toprect.centery=DISPLAYSURF.get_rect().centery-170
                DISPLAYSURF.blit(topobj,toprect)

                initials=[]
                file=open('initials.txt','r')
                for line in file:
                    line=line.replace('\n','')
                    initials.append(line)
                file.close()
                initials.reverse()

                if len(initials)>10:
                    del initials[-1]
                x=-170
                for a,b in zip(listscore,initials):
                    y=str((a,b))
                    y=y.replace('(','')
                    y=y.replace(')','')
                    y=y.replace("'",'')
                    y=y.replace(',',' - ')
                    scobj=textbasics.render(str(y),True,WHITE)
                    scorect=scobj.get_rect()
                    scorect.centerx=DISPLAYSURF.get_rect().centerx-225
                    x=x+35
                    scorect.centery=DISPLAYSURF.get_rect().centery+(x)
                    DISPLAYSURF.blit(scobj,scorect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #find position of mouse
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>340 and x<640 and y>310 and y<355:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        #if mouse says quit
                        if x>445 and x<535 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RETURN:
                            bgmusic.stop()
                            cutscene()
                        #when the key is pressed, change level
                        if event.key==K_1:
                            easygame()
                        if event.key==K_2:
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.flip()
        else:
            x = badsnake_segments[0].rect.x + a_change
            y = badsnake_segments[0].rect.y + b_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments.insert(0, badsegment)
            all_sprites_list.add(badsegment)

            x = badsnake_segments2[0].rect.x + f_change
            y = badsnake_segments2[0].rect.y + g_change
            badsegment = AISnake(x, y)
            # add new box onto list
            badsnake_segments2.insert(0, badsegment)
            all_sprites_list.add(badsegment)

        if len(snake_segments)<=1:
            gameover(bgmusic,snake_segments)
            
        else: #otherwise keep going
            x = snake_segments[0].rect.x + x_change
            y = snake_segments[0].rect.y + y_change
            segment = Snake(x, y)
            # add new box onto list
            snake_segments.insert(0, segment)
            all_sprites_list.add(segment)

        try:
            #continuously update snake to maintain length
            old_segment = snake_segments.pop()
            all_sprites_list.remove(old_segment)
            old_segment=badsnake_segments.pop()
            all_sprites_list.remove(old_segment)
            old_segment=badsnake_segments2.pop()
            all_sprites_list.remove(old_segment)
        except:
            end_it = False
            while (end_it == False):
                #get font
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                #highscore font, blit in center
                listscore = []
                # open scores file
                file = open('highscores.txt', 'r')
                for line in file:
                    listscore.append(int(line))  # add scores to a list
                listscore.append(score)  # add score to a list
                listscore = sorted(listscore, reverse=True)  # sort list
                file.close()

                del listscore[-1]

                if score >= listscore[0]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                elif score > listscore[-1]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render("You're in the Top 10!", True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        os.system('initialstk.py')
                        end_it = True
                    pygame.display.flip()
                #blit you win on screen
                overobj = textbasics.render('You Win!', True, RED)
                overrect = overobj.get_rect()
                overrect.centerx = DISPLAYSURF.get_rect().centerx+90
                overrect.centery = DISPLAYSURF.get_rect().centery - 45
                DISPLAYSURF.blit(overobj, overrect)
                #blit the score
                scoreobj=textbasics.render('Score: '+str(score), True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx+90
                scorerect.centery=DISPLAYSURF.get_rect().centery
                DISPLAYSURF.blit(scoreobj, scorerect)
                #blit play again
                againobj=textbasics.render('Click to Play Again', True, GREEN)
                againrect=againobj.get_rect()
                againrect.centerx=DISPLAYSURF.get_rect().centerx+90
                againrect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(againobj, againrect)
                #blit quit
                quitobj=textbasics.render('QUIT', True, GREEN)
                quitrect=quitobj.get_rect()
                quitrect.centerx=DISPLAYSURF.get_rect().centerx+90
                quitrect.centery=DISPLAYSURF.get_rect().centery+135
                DISPLAYSURF.blit(quitobj, quitrect)
                
                #blit top ten scores
                textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 30)
                topobj=textbasics.render('TOP TEN',True,WHITE)
                toprect=topobj.get_rect()
                toprect.centerx=DISPLAYSURF.get_rect().centerx-225
                toprect.centery=DISPLAYSURF.get_rect().centery-170
                DISPLAYSURF.blit(topobj,toprect)

                initials=[]
                file=open('initials.txt','r')
                for line in file:
                    line=line.replace('\n','')
                    initials.append(line)
                file.close()
                initials.reverse()

                if len(initials)>10:
                    del initials[-1]
                x=-170
                for a,b in zip(listscore,initials):
                    y=str((a,b))
                    y=y.replace('(','')
                    y=y.replace(')','')
                    y=y.replace("'",'')
                    y=y.replace(',',' - ')
                    scobj=textbasics.render(str(y),True,WHITE)
                    scorect=scobj.get_rect()
                    scorect.centerx=DISPLAYSURF.get_rect().centerx-225
                    x=x+35
                    scorect.centery=DISPLAYSURF.get_rect().centery+(x)
                    DISPLAYSURF.blit(scobj,scorect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        #find position of mouse
                        #if mouse says click again
                        x,y=pygame.mouse.get_pos()
                        if x>340 and x<640 and y>310 and y<355:
                            end_it=True
                            bgmusic.stop()
                            cutscene()
                        #if mouse says quit
                        if x>445 and x<535 and y>365 and y<400:
                            pygame.quit()
                            sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RETURN:
                            bgmusic.stop()
                            cutscene()
                        #when the key is pressed, change level
                        if event.key==K_1:
                            easygame()
                        if event.key==K_2:
                            mediumgame()
                        if event.key==K_3 or event.key==K_4:
                            hardgame()
                        if event.key==K_5 or event.key==K_6:
                            hardgame2()
                        if event.key==K_7 or event.key==K_8:
                            obstaclegame()
                        if event.key==K_9 or event.key==K_0:
                            hardobstaclegame()
                        if event.key==K_q:
                            pygame.quit()
                            sys.exit()

                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.flip()

        #draw everything
        DISPLAYSURF.fill(BG)

        for ent in all_sprites_list:  # update all
            ent.update()

        #draw everything in list
        all_sprites_list.draw(DISPLAYSURF)

        #get font
        text = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
        #title font, blit in center
        titleobj = text.render(str(score), True, WHITE)
        titlerect = titleobj.get_rect()
        titlerect.x = 5
        titlerect.y = 5
        DISPLAYSURF.blit(titleobj,titlerect)        
        
        pygame.display.flip()

        clock.tick(ticker)

        create-=1 #subtract from create to keep track of apple spawning
        all_sprites_list.remove(old_segment)

credit()
