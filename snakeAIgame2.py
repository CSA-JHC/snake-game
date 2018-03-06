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
##by eating the red apples. The green apples makes you lose a point and
##speed increases. There is also an AI snake that tries to eat the apples and
##follows you around.

#LEVELS ---
#if 0-5 and 5-10, try to get another five apples -- level 1 and 2 -- DONE
#if 10-15 and 15-20, add bad apples every time a good apple spawns -- level 3 and 4 -- DONE
#if 20-25 and 25-30, add AI snake try to get apples and player -- level 5 and 6 -- DONE
#if 30-35 and 35-40, add obstacles (think about what boosts to add) -- level 7 and 8 -- DONE
#if 40-45 and 45-50, add another AI snake -- level 9 and 10 -- DONE

##add boosts - extra points?
##work on quit ability (at game over and after each level)
    #mouse position
##set goals for each level
##make apples spawn faster
##fix audio

import pygame,sys
from pygame.locals import *
import random

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
DISPLAYSURF.fill(BG)
pygame.display.set_caption('Snake')

#snake measurements per box
snakeheight=20
snakewidth=20
margin=3
#global variables to help keep track of score
score=0
level=1
create=5
ticker=5
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

#bad apple class, comes from snake class
class BoostApple(Basic):
    def __init__(self,x,y):
        super(BoostApple, self).__init__(x,y)

        self.image.fill(YELLOW)

class Obstacle(Basic):
    def __init__(self,x,y):
        super(Obstacle, self).__init__(x,y)

        self.image.fill(BROWN)

#checks for collision and adds points
def collision(badsnake,snake, food,pics,sound):
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

def specialcollision(badsnake,snake,food,pics,sound):
    global score
    global ticker
    for s in snake:
        for a in food:
            if s.rect.colliderect(a): #if snake collides with green apple
                sound.play() #play sound
                #remove apple from list and sprites list
                food.remove(a)
                pics.remove(a)
                #remove box on snake
                snake=snake.pop() #remove end of snake from list and sprites list
                pics.remove(snake)
                score-=1 #-1 from score
                ticker+=0.5
    for s in badsnake:
        for a in food:
            if s.rect.colliderect(a): #if snake collides with green apple
                sound.play() #play sound
                #remove apple from list and sprites list
                food.remove(a)
                pics.remove(a)
                #remove box on snake
                badsnake=badsnake.pop() #remove end of snake from list and sprites list
                pics.remove(badsnake)
                #enemyscore-=1 #-1 from score
                ticker+=0.5

#checks for collision and adds points
def collision2(badsnake,snake, food,pics,sound):
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

def specialcollision2(badsnake,snake,food,pics,sound):
    global score
    global ticker
    for s in snake:
        for a in food:
            if s.rect.colliderect(a): #if snake collides with green apple
                sound.play() #play sound
                #remove apple from list and sprites list
                food.remove(a)
                pics.remove(a)
                #remove box on snake
                snake=snake.pop() #remove end of snake from list and sprites list
                pics.remove(snake)
                score-=1 #-1 from score
                ticker+=0.5
    for s in badsnake:
        for a in food:
            if s.rect.colliderect(a): #if snake collides with green apple
                sound.play() #play sound
                #remove apple from list and sprites list
                food.remove(a)
                pics.remove(a)
                #remove box on snake
                badsnake=badsnake.pop() #remove end of snake from list and sprites list
                pics.remove(badsnake)
                #enemyscore-=1 #-1 from score
                ticker+=0.5

def boostcollision():
    print('ai snake freezes')
def boostcollision2():
    print('player loses one point')

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

def obstaclecollision(snake,music,route,a,b,obstlist):
    global score
    global ticker

    for s in snake:
        for i in obstlist:
            if s.rect.colliderect(i):
                gameover(music)
        
def check(badsnake,snake,route,pics,music,badroute,x,y,sm,w):
    dead=False #keeps track whether or not he's dead
    for s in snake: #if he goes past the borders set dead to true
        if s.rect.x>=785:
            dead=True
        elif s.rect.x<=0:
            dead=True
        if s.rect.y>=485:
            dead=True
        elif s.rect.y<=0:
            dead=True
            
    for s in snake: #if player collides with bad snake, set dead to true
        for b in badsnake:
            if s.rect.colliderect(b):
                dead=True

    if dead==True: #if dead is true
        gameover(music) #go to gameover

    #figure out if the snake hit himself or not
    #if yes, gameover
    if 'left' in route and 'right' in route:
        gameover(music)
    elif 'up' in route and 'down' in route:
        gameover(music)

def checkAI2(badsnake, snake,route,pics,music,badroute,x,y,sm,w):
    dead=False #keeps track whether or not he's dead
    for s in snake: #if he goes past the borders set dead to true
        if s.rect.x>=785:
            dead=True
        elif s.rect.x<=0:
            dead=True
        if s.rect.y>=485:
            dead=True
        elif s.rect.y<=0:
            dead=True
            
    for s in snake: #if player collides with bad snake, set dead to true
        for b in badsnake:
            if s.rect.colliderect(b):
                dead=True

    if dead==True: #if dead is true
        gameover(music) #go to gameover

    #figure out if the snake hit himself or not
    #if yes, gameover
    if 'left' in route and 'right' in route:
        gameover(music)
    elif 'up' in route and 'down' in route:
        gameover(music)
                
def gameover(gm):
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

    if score>=listscore[0]: #if the score is >=highscore
        end_it = False
        while (end_it == False):
            # blit highscore on screen
            textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
            overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
            overrect = overobj.get_rect()
            overrect.centerx = DISPLAYSURF.get_rect().centerx
            overrect.centery = DISPLAYSURF.get_rect().centery - 135
            DISPLAYSURF.blit(overobj, overrect)
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
        scoreobj=textbasics.render('Click to Play Again', True, RED)
        scorerect=scoreobj.get_rect()
        scorerect.centerx=DISPLAYSURF.get_rect().centerx
        scorerect.centery=DISPLAYSURF.get_rect().centery+90
        DISPLAYSURF.blit(scoreobj, scorerect)
        #quit
        quitobj=textbasics.render('QUIT', True, GREEN)
        quitrect=quitobj.get_rect()
        quitrect.centerx=DISPLAYSURF.get_rect().centerx
        quitrect.centery=DISPLAYSURF.get_rect().centery+135
        DISPLAYSURF.blit(quitobj, quitrect)

        for event in pygame.event.get():
            #if click screen, go to start screen
            if event.type==MOUSEBUTTONDOWN:
                #find position of mouse
                #if mouse says click again
                pygame.mouse.get_pos()
                
                score = 0
                level=1
                gm.stop()
                start()
                #if mouse says quit
                #then pygame.quit(), sys.exit()
            # if quit, exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

def start():
    global score
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
    beginmusic.set_volume(0.07)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3
    
    # global variables to help keep track of score,death,etc.
    create=5
    ticker=5

    #list to keep track of apples and direction
    Apples=[]
    BadApples=[]
    Direction=['right']
    AIDirection=['right']

    x_change=snakewidth+margin
    y_change=0

    a_change = snakewidth + margin
    b_change = 0

    f_change=snakewidth+margin
    g_change=0

    end_it=False
    while (end_it==False):
        #get font
        text = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
        text2=pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 25)

        #highscore, blit in center
        scores=[]
        file=open('highscores.txt','r')
        for line in file:
            scores.append(int(line))
        blitscore=scores[0]

        #highscore font, blit in center
        overobj = text.render('HIGHSCORE: '+str(blitscore), True, RED)
        overrect = overobj.get_rect()
        overrect.centerx = DISPLAYSURF.get_rect().centerx
        overrect.centery = DISPLAYSURF.get_rect().centery - 135
        DISPLAYSURF.blit(overobj, overrect)

        #title font, blit in center
        titleobj = text.render('Snake', True, WHITE)
        titlerect = titleobj.get_rect()
        titlerect.centerx = DISPLAYSURF.get_rect().centerx
        titlerect.centery = DISPLAYSURF.get_rect().centery-180
        DISPLAYSURF.blit(titleobj,titlerect)

        #click to font, blit in center
        clickobj = text2.render('Click To', True, GREEN)
        clickrect = clickobj.get_rect()
        clickrect.centerx = DISPLAYSURF.get_rect().centerx
        clickrect.centery = DISPLAYSURF.get_rect().centery-45
        DISPLAYSURF.blit(clickobj, clickrect)

        #start game font, blit in center
        startobj = text.render('Start Game', True, GREEN)
        startrect = startobj.get_rect()
        startrect.centerx = DISPLAYSURF.get_rect().centerx
        startrect.centery = DISPLAYSURF.get_rect().centery
        DISPLAYSURF.blit(startobj, startrect)

        #instructions, blit to start screen
        moveobj = text.render('Use WASD to move up and down', True, GREEN)
        moverect = moveobj.get_rect()
        moverect.centerx = DISPLAYSURF.get_rect().centerx
        moverect.centery = DISPLAYSURF.get_rect().centery+90
        DISPLAYSURF.blit(moveobj, moverect)

        for event in pygame.event.get():
            #if mousebuttondown or space pressed start game
            if event.type==MOUSEBUTTONDOWN:
                end_it=True
                beginmusic.stop()
                bgmusic.play(-1,0)
                bgmusic.set_volume(0.05)
                easygame()
            #if quit, exit
            elif event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

def easygame():
    global score
    global level
    global create
    global ticker

    pygame.init()
    pygame.mixer.init()

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    beginmusic.play(-1,0)
    beginmusic.set_volume(0.07)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3

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
        specialcollision(badsnake_segments,snake_segments, BadApples,all_sprites_list,bite) #check for collision with special apple

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
                scoreobj=textbasics.render('Click to Keep Going', True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(scoreobj, scorerect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        end_it=True
                        level+=1
                        #print(level)
                        if score>=10:
                            mediumgame()
                        else:
                            easygame()
                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()

        if create<=0: #if create is less than 0 create new apples
            applex=random.randint(0,770)
            appley=random.randint(0,470)
##            if applex==30:
##                applex=30
##            if appley==45:
##                appley=45
            for s in snake_segments:
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
            for s in badsnake_segments:
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
            apple=Apple(applex,appley)
            Apples.append(apple)
            all_sprites_list.add(apple)
            create=50

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

                #if there is more than two directions, remove first term in list
                if len(Direction)>2:
                    Direction.pop(0)

        old_segment = snake_segments.pop()
        all_sprites_list.remove(old_segment)

        if len(snake_segments)<=0:
            gameover(bgmusic)
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
        titlerect.y = 0
        DISPLAYSURF.blit(titleobj,titlerect)
        pygame.display.flip()

        clock.tick(ticker)

        create-=1 #subtract from create to keep track of apple spawning

def mediumgame():
    global score
    global level
    global create
    global ticker

    pygame.init()
    pygame.mixer.init()

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    beginmusic.play(-1,0)
    beginmusic.set_volume(0.07)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3

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
        specialcollision(badsnake_segments,snake_segments, BadApples,all_sprites_list,bite) #check for collision with special apple

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
                scoreobj=textbasics.render('Click to Keep Going', True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(scoreobj, scorerect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        end_it=True
                        level+=1
                        #print(level)
                        if score>=20:
                            hardgame()
                        else:
                            mediumgame()
                    # if quit, exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()

        if create<=0: #if create is less than 0 create new apples
            applex=random.randint(0,770)
            appley=random.randint(0,470)
##            if applex==30:
##                applex=30
##            if appley==45:
##                appley=45
            for s in snake_segments:
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
            for s in badsnake_segments:
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
            apple=Apple(applex,appley)
            Apples.append(apple)
            all_sprites_list.add(apple)
            create=50

        if create==25: #when create is 25, add special reduction apple
            applex = random.randint(0, 770)
            appley = random.randint(0, 470)
##            if applex == 30:
##                applex = 30
##            if appley == 45:
##                appley = 45
            for s in snake_segments:
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
            for s in badsnake_segments:
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
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

                #if there is more than two directions, remove first term in list
                if len(Direction)>2:
                    Direction.pop(0)

        old_segment = snake_segments.pop()
        all_sprites_list.remove(old_segment)

        if len(snake_segments)<=0:
            gameover(bgmusic)
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
        titlerect.y = 0
        DISPLAYSURF.blit(titleobj,titlerect)
        pygame.display.flip()

        clock.tick(ticker)

        create-=1 #subtract from create to keep track of apple spawning

def hardgame():
    global score
    global level
    global create
    global ticker

    pygame.init()
    pygame.mixer.init()

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    beginmusic.play(-1,0)
    beginmusic.set_volume(0.07)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3

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
        all_sprites_list.add(segment)
    #starter snake - AI2
##    badsnake_segments2 = []
##    for i in range(3):
##        f = (f_change + margin) * i + 5
##        g = 465
##        segment = AISnake(f, g)
##        # add segment to sprites list and badsnake list
##        badsnake_segments2.append(segment)
##        #all_sprites_list.add(segment)

    #spawn special apple - AI snake freezes for 5sec
    applex=random.randint(0,770)
    appley=random.randint(0,470)
    for s in snake_segments:
        if applex==s.rect.x:
            applex+=15
        if appley==s.rect.y:
            appley+=15
    for s in badsnake_segments:
        if applex==s.rect.x:
            applex+=15
        if appley==s.rect.y:
            appley+=15            
    apple=BoostApple(applex,appley)
    Boost.append(apple)
    all_sprites_list.add(apple)

    while True:
        check(badsnake_segments,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin)  # check lives
        #checkAI2(badsnake_segments2,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin) #check lives with AI2
        collision(badsnake_segments,snake_segments, Apples,all_sprites_list,bite) #check for collisions with apple
        specialcollision(badsnake_segments,snake_segments, BadApples,all_sprites_list,bite) #check for collision with special apple

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
                scoreobj=textbasics.render('Click to Keep Going', True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(scoreobj, scorerect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        end_it=True
                        level+=1
                        #print(level)
                        if score>=30:
                            print('yeet')
                        else:
                            obstaclegame()
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
##            if applex==30:
##                applex=30
##            if appley==45:
##                appley=45
            for s in snake_segments:
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
            for s in badsnake_segments:
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
            apple=Apple(applex,appley)
            Apples.append(apple)
            all_sprites_list.add(apple)
            create=50

        if create==25: #when create is 25, add special reduction apple
            applex = random.randint(0, 770)
            appley = random.randint(0, 470)
##            if applex == 30:
##                applex = 30
##            if appley == 45:
##                appley = 45
            for s in snake_segments:
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
            for s in badsnake_segments:
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
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

                #if there is more than two directions, remove first term in list
                if len(Direction)>2:
                    Direction.pop(0)
                    
        if len(Apples)==1: #if there is an apple
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
                    if (s.rect.y < (a.rect.y + 5)) and (s.rect.y > (a.rect.y - 5)) and ((s.rect.x < a.rect.x)):
                        direction = 'right'
                        AIDirection.append(direction)
                        a_change = (snakewidth + margin)
                        b_change = 0
                        break
                    if (s.rect.y < (a.rect.y + 5)) and (s.rect.y > (a.rect.y - 5)) and ((s.rect.x > a.rect.x)):
                        direction = 'left'
                        AIDirection.append(direction)
                        a_change = (snakewidth + margin) * -1
                        b_change = 0
                        break
                    
                if len(AIDirection)>2:
                    AIDirection.pop(0) #keep track of AI direction
                
        ###AI - chasing the player
        else: #if there isn't an apple
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

        #continuously update snake to maintain length
        old_segment = snake_segments.pop()
        all_sprites_list.remove(old_segment)

        old_segment=badsnake_segments.pop()
        all_sprites_list.remove(old_segment)

        if len(badsnake_segments)<=0:
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

                if score >= listscore[0]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        end_it = True
                    pygame.display.flip()
                #blit you win on screen
                overobj = textbasics.render('You Win!', True, RED)
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
                scoreobj=textbasics.render('Click to Play Again', True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(scoreobj, scorerect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        bgmusic.stop()
                        start()
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
        if len(snake_segments)<=0:
            gameover(bgmusic)
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
        titlerect.y = 0
        DISPLAYSURF.blit(titleobj,titlerect)
        pygame.display.flip()

        clock.tick(ticker)

        create-=1 #subtract from create to keep track of apple spawning
        #print(AIDirection)

def obstaclegame():
    global score
    global level
    global create
    global ticker

    pygame.init()
    pygame.mixer.init()

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    beginmusic.play(-1,0)
    beginmusic.set_volume(0.07)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3

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
        all_sprites_list.add(segment)
    #starter snake - AI2
##    badsnake_segments2 = []
##    for i in range(3):
##        f = (f_change + margin) * i + 5
##        g = 465
##        segment = AISnake(f, g)
##        # add segment to sprites list and badsnake list
##        badsnake_segments2.append(segment)
##        #all_sprites_list.add(segment)

    #spawn special apple - freezes AI snake for 5sec
    applex=random.randint(0,770)
    appley=random.randint(0,470)
    for s in snake_segments:
        if applex==s.rect.x:
            applex+=15
        if appley==s.rect.y:
            appley+=15
    for s in badsnake_segments:
        if applex==s.rect.x:
            applex+=15
        if appley==s.rect.y:
            appley+=15            
    apple=BoostApple(applex,appley)
    Boost.append(apple)
    all_sprites_list.add(apple)

    while True:
        obstacles(Obst,all_sprites_list)
        check(badsnake_segments,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin)  # check lives
        #checkAI2(badsnake_segments2,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin)
        collision(badsnake_segments,snake_segments, Apples,all_sprites_list,bite) #check for collisions with apple
        specialcollision(badsnake_segments,snake_segments, BadApples,all_sprites_list,bite) #check for collision with special apple
        obstaclecollision(snake_segments,bgmusic,AIDirection,a_change,b_change,Obst)

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
                scoreobj=textbasics.render('Click to Keep Going', True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(scoreobj, scorerect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        end_it=True
                        level+=1
                        #print(level)
                        if score>=30:
                            print('yeet')
                        else:
                            hardobstaclegame()
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
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
            for s in badsnake_segments:
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
            apple=Apple(applex,appley)
            Apples.append(apple)
            all_sprites_list.add(apple)
            create=50

        if create==25: #when create is 25, add special reduction apple
            applex = random.randint(0, 770)
            appley = random.randint(0, 470)
            for s in snake_segments:
                if applex==s.rect.x:
                    applex+=30
                if appley==s.rect.y:
                    appley+=30
            for s in badsnake_segments:
                if applex==s.rect.x:
                    applex+=30
                if appley==s.rect.y:
                    appley+=30
            for i in Obst:
                if applex>=i.rect.x and applex<=i.rect.x+30:
                    applex+=30
                if appley>=i.rect.y and applex<=i.rect.y:
                    appley+=30
            apple=BadApple(applex,appley)
            BadApples.append(apple)
            all_sprites_list.add(apple)        


        for i in Obst:
            for a in Apples:
                if i.rect.colliderect(a):
                    all_sprites_list.remove(a)
        for i in Obst:
            for b in BadApples:
                if i.rect.colliderect(b):
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

        #avoid obstacles -- SNAKE NOT MOVING? -- GET AI2 SNAKE MOVING
        for b in badsnake_segments:
            #one
            if b.rect.x>=50 and b.rect.x<=90 and b.rect.y+20>=82 and b.rect.y+20<=102:
                print('right')
                b.rect.y=62
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break
            if b.rect.x>=50 and b.rect.x<=90 and b.rect.y>=102 and b.rect.y<=122:
                print('right')
                b.rect.y=124
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break
            if b.rect.y>=82 and b.rect.y<=122 and b.rect.x+20>=50 and b.rect.x+20<=70:
                print('down')
                b.rect.x=30
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            if b.rect.y>=82 and b.rect.y<=122 and b.rect.x>=70 and b.rect.x<=90:
                print('down')
                b.rect.x=92
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            #two
            if b.rect.x>=155 and b.rect.x<=195 and b.rect.y+20>=253 and b.rect.y+20<=273:
                print('right')
                b.rect.y=233
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break
            if b.rect.x>=155 and b.rect.x<=195 and b.rect.y>=273 and b.rect.y<=293:
                print('right')
                b.rect.y=295
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break
            if b.rect.y>=253 and b.rect.y<=293 and b.rect.x+20>=155 and b.rect.x+20<=175:
                print('down')
                b.rect.x=135
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            if b.rect.y>=253 and b.rect.y<=293 and b.rect.x>=175 and b.rect.x<=195:
                print('down')
                b.rect.x=197
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            #three
            if b.rect.x>=345 and b.rect.x<=385 and b.rect.y+20>=358 and b.rect.y+20<=378:
                print('right')
                b.rect.y=338
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break
            if b.rect.x>=345 and b.rect.x<=385 and b.rect.y>=378 and b.rect.y<=398:
                print('right')
                b.rect.y=400
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break
            if b.rect.y>=358 and b.rect.y<=398 and b.rect.x+20>=345 and b.rect.x+20<=365:
                print('up')
                b.rect.x=325
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            if b.rect.y>=358 and b.rect.y<=398 and b.rect.x>=365 and b.rect.x<=385:
                print('up')
                b.rect.x=387
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            #four
            if b.rect.x>=677 and b.rect.x<=717 and b.rect.y+20>=144 and b.rect.y+20<=164:
                print('left')
                b.rect.y=124
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break 
            if b.rect.x>=677 and b.rect.x<=717 and b.rect.y>=164 and b.rect.y<=184:
                print('left')
                b.rect.y=186
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break
            if b.rect.y>=144 and b.rect.y<=184 and b.rect.x+20>=677 and b.rect.x+20<=697:
                print('down')
                b.rect.x=657
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            if b.rect.y>=144 and b.rect.y<=184 and b.rect.x>=697 and b.rect.x<=717:
                print('down')
                b.rect.x=719
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            #five
            if b.rect.x>=567 and b.rect.x<=607 and b.rect.y+20>=278 and b.rect.y+20<=298:
                print('left')
                b.rect.y=258
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break
            if b.rect.x>=567 and b.rect.x<=607 and b.rect.y>=298 and b.rect.y<=318:
                print('left')
                b.rect.y=320
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break
            if b.rect.y>=278 and b.rect.y<=318 and b.rect.x+20>=567 and b.rect.x+20<=587:
                print('up')
                b.rect.x=547
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            if b.rect.y>=278 and b.rect.y<=318 and b.rect.x>=587 and b.rect.x<=607:
                print('up')
                b.rect.x=609
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            #six
            if b.rect.x>=325 and b.rect.x<=365 and b.rect.y+20>=35 and b.rect.y+20<=75:
                print('right')
                b.rect.y=15
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break 
            if b.rect.x>=325 and b.rect.x<=365 and b.rect.y>=75 and b.rect.y<=95:
                print('right')
                b.rect.y=97
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break 
            if b.rect.y>=35 and b.rect.y<=95 and b.rect.x+20>=325 and b.rect.x+20<=345:
                print('down')
                b.rect.x=305
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break  
            if b.rect.y>=35 and b.rect.y<=95 and b.rect.x>=345 and b.rect.x<=365:
                print('down')
                b.rect.x=367
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
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

                #if there is more than two directions, remove first term in list
                if len(Direction)>2:
                    Direction.pop(0)

        if len(Apples)==1: #if there is an apple            
            for s in badsnake_segments: #follow the apple up or down
                for a in Apples:   
                    if (s.rect.x < a.rect.x and s.rect.y > a.rect.y):
                        #print('up')
                        direction = 'up'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin) * -1
                        break
                    if (s.rect.x < a.rect.x and s.rect.y < a.rect.y):
                        #print('down')
                        direction = 'down'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)
                        break
                    if (s.rect.x > a.rect.x and s.rect.y > a.rect.y):
                        #print('up')
                        direction = 'up'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin) * -1
                        break
                    if (s.rect.x > a.rect.x and s.rect.y < a.rect.y):
                        #print('down')
                        direction = 'down'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)
                        break
                            
                if len(AIDirection)>2:
                    AIDirection.pop(0) #keep track of AI direction
            
            for s in badsnake_segments: #if the apple and the snake are at the same position - ish, go to apple
                for a in Apples:
                    if (s.rect.y < (a.rect.y + 5)) and (s.rect.y > (a.rect.y - 5)) and ((s.rect.x < a.rect.x)):
                        #print('right')
                        direction = 'right'
                        AIDirection.append(direction)
                        a_change = (snakewidth + margin)
                        b_change = 0
                        break
                    if (s.rect.y < (a.rect.y + 5)) and (s.rect.y > (a.rect.y - 5)) and ((s.rect.x > a.rect.x)):
                        #print('left')
                        direction = 'left'
                        AIDirection.append(direction)
                        a_change = (snakewidth + margin) * -1
                        b_change = 0
                        break
                
                if len(AIDirection)>2:
                    AIDirection.pop(0) #keep track of AI direction

        else:
            for b in badsnake_segments: #follow the snake up or down
                for s in snake_segments:
                    if (b.rect.x < s.rect.x and b.rect.y > s.rect.y):
                        #print('up')
                        direction = 'up'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin) * -1
                        break

                    if (b.rect.x < s.rect.x and b.rect.y < s.rect.y):
                        #print('down')
                        direction = 'down'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)
                        break

                    if (b.rect.x > s.rect.x and b.rect.y > s.rect.y):
                        #print('up')
                        direction = 'up'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin) * -1
                        break
                    
                    if (b.rect.x > s.rect.x and b.rect.y < s.rect.y):
                        #print('down')
                        direction = 'down'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)
                        break
    
                if len(AIDirection2)>2:
                    AIDirection2.pop(0) #keep track of AI direction

            for b in badsnake_segments: #if the AI snake and the snake are at the same position - ish, go to snake
                for s in snake_segments:
                    if (b.rect.y <= (s.rect.y + 20)) and (b.rect.y >= (s.rect.y - 20)) and ((b.rect.x <= s.rect.x)):
                        #print('right')
                        direction = 'right'
                        AIDirection.append(direction)
                        a_change = (snakewidth + margin)
                        b_change = 0
                        break
                    if (b.rect.y <= (s.rect.y + 20)) and (b.rect.y >= (s.rect.y - 20)) and ((b.rect.x >= s.rect.x)):
                        #print('left')
                        direction = 'left'
                        AIDirection.append(direction)
                        a_change = (snakewidth + margin) * -1
                        b_change = 0
                        break
                    
                if len(AIDirection)>2:
                    AIDirection.pop(0) #keep track of AI direction
                        
        #continuously update snake to maintain length
        old_segment = snake_segments.pop()
        all_sprites_list.remove(old_segment)
        old_segment=badsnake_segments.pop()
        all_sprites_list.remove(old_segment)
##        old_segment=badsnake_segments2.pop()
##        all_sprites_list.remove(old_segment)

        if len(badsnake_segments)<=0: #or len(badsnake_segments2)<=0:
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

                if score >= listscore[0]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        end_it = True
                    pygame.display.flip()
                #blit you win on screen
                overobj = textbasics.render('You Win!', True, RED)
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
                scoreobj=textbasics.render('Click to Play Again', True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(scoreobj, scorerect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        bgmusic.stop()
                        start()
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

##            x = badsnake_segments2[0].rect.x + f_change
##            y = badsnake_segments2[0].rect.y + g_change
##            badsegment = AISnake(x, y)
##            # add new box onto list
##            badsnake_segments2.insert(0, badsegment)
##            all_sprites_list.add(badsegment)

        if len(snake_segments)<=0:
            gameover(bgmusic)
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
        titlerect.y = 0
        DISPLAYSURF.blit(titleobj,titlerect)        
        
        pygame.display.flip()

        clock.tick(ticker)

        create-=1 #subtract from create to keep track of apple spawning

def hardobstaclegame():
    global score
    global level
    global create
    global ticker

    pygame.init()
    pygame.mixer.init()

    #load sound
    bite=pygame.mixer.Sound('bite.wav')
    bgmusic=pygame.mixer.Sound('playmusic.wav')
    beginmusic=pygame.mixer.Sound('intromusic.wav')
    beginmusic.play(-1,0)
    beginmusic.set_volume(0.07)

    #snake measurements per box
    snakeheight=20
    snakewidth=20
    margin=3

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

    #spawn special apple - freezes both AI snakes for 5sec
    applex=random.randint(0,770)
    appley=random.randint(0,470)
    for s in snake_segments:
        if applex==s.rect.x:
            applex+=15
        if appley==s.rect.y:
            appley+=15
    for s in badsnake_segments:
        if applex==s.rect.x:
            applex+=15
        if appley==s.rect.y:
            appley+=15            
    apple=BoostApple(applex,appley)
    Boost.append(apple)
    all_sprites_list.add(apple)

    while True:
        obstacles(Obst,all_sprites_list)
        check(badsnake_segments,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin)  # check lives
        checkAI2(badsnake_segments2,snake_segments,Direction,all_sprites_list,bgmusic,AIDirection,a_change,b_change,snakewidth,margin)
        collision(badsnake_segments,snake_segments, Apples,all_sprites_list,bite) #check for collisions with apple
        collision2(badsnake_segments2,snake_segments, Apples,all_sprites_list,bite)
        specialcollision(badsnake_segments,snake_segments, BadApples,all_sprites_list,bite) #check for collision with special apple
        specialcollision(badsnake_segments2,snake_segments, BadApples,all_sprites_list,bite)
        obstaclecollision(snake_segments,bgmusic,AIDirection,a_change,b_change,Obst)

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
                scoreobj=textbasics.render('Click to Keep Going', True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(scoreobj, scorerect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        end_it=True
                        level+=1
                        #print(level)
                        if score>=30:
                            print('yeet')
                        else:
                            hardobstaclegame()
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
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15
            for s in badsnake_segments:
                if applex==s.rect.x:
                    applex+=15
                if appley==s.rect.y:
                    appley+=15            
            apple=Apple(applex,appley)
            Apples.append(apple)
            all_sprites_list.add(apple)
            create=50

        if create==25: #when create is 25, add special reduction apple
            applex = random.randint(0, 770)
            appley = random.randint(0, 470)
            for s in snake_segments:
                if applex==s.rect.x:
                    applex+=30
                if appley==s.rect.y:
                    appley+=30
            for s in badsnake_segments:
                if applex==s.rect.x:
                    applex+=30
                if appley==s.rect.y:
                    appley+=30
            apple=BadApple(applex,appley)
            BadApples.append(apple)
            all_sprites_list.add(apple)        

        for i in Obst:
            for a in Apples:
                if i.rect.colliderect(a):
                    all_sprites_list.remove(a)
        for i in Obst:
            for b in BadApples:
                if i.rect.colliderect(b):
                    all_sprites_list.remove(b)

        #if AI goes past the borders, reset
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
                
        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction
                
        for s in badsnake_segments: #AI borders
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

        #if AI2 goes past the borders, reset
        for s in badsnake_segments2:
            if s.rect.x > 800 and s.rect.y > 250:
                #print('up')
                s.rect.x = 780
                direction = 'up'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin) * -1
                break
            if s.rect.x > 800 and s.rect.y < 250:
                #print('down')
                s.rect.x = 780
                direction = 'down'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin)
                break
            if s.rect.x < 0 and s.rect.y > 250:
                #print('up')
                s.rect.x = 0
                direction = 'up'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin) * -1
                break
            if s.rect.x < 0 and s.rect.y < 250:
                #print('down')
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
                #print('right')
                s.rect.y = 480
                direction = 'right'
                AIDirection2.append(direction)
                f_change = (snakewidth + margin)
                g_change = 0
                break
            if s.rect.y > 500 and s.rect.x > 400:
                #print('left')
                s.rect.y = 480
                direction = 'left'
                AIDirection2.append(direction)
                f_change = (snakewidth + margin) * -1
                g_change = 0
                break
            if s.rect.y < 0 and s.rect.x < 400:
                #print('right')
                s.rect.y = 0
                direction = 'right'
                AIDirection2.append(direction)
                f_change = (snakewidth + margin)
                g_change = 0
                break
            if s.rect.y < 0 and s.rect.x > 400:
                #print('left')
                s.rect.y = 0
                direction = 'left'
                AIDirection2.append(direction)
                f_change = (snakewidth + margin) * -1
                g_change = 0
                break

        if len(AIDirection2)>2:
            AIDirection2.pop(0) #keep track of AI2 direction
    
        #avoid obstacles -- SNAKE NOT MOVING? -- GET AI2 SNAKE MOVING
        for b in badsnake_segments:
            #one
            if b.rect.x>=50 and b.rect.x<=90 and b.rect.y+20>=82 and b.rect.y+20<=102:
                print('right')
                b.rect.y=62
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break
            if b.rect.x>=50 and b.rect.x<=90 and b.rect.y>=102 and b.rect.y<=122:
                print('right')
                b.rect.y=124
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break
            if b.rect.y>=82 and b.rect.y<=122 and b.rect.x+20>=50 and b.rect.x+20<=70:
                print('down')
                b.rect.x=30
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            if b.rect.y>=82 and b.rect.y<=122 and b.rect.x>=70 and b.rect.x<=90:
                print('down')
                b.rect.x=92
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            #two
            if b.rect.x>=155 and b.rect.x<=195 and b.rect.y+20>=253 and b.rect.y+20<=273:
                print('right')
                b.rect.y=233
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break
            if b.rect.x>=155 and b.rect.x<=195 and b.rect.y>=273 and b.rect.y<=293:
                print('right')
                b.rect.y=295
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break
            if b.rect.y>=253 and b.rect.y<=293 and b.rect.x+20>=155 and b.rect.x+20<=175:
                print('down')
                b.rect.x=135
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            if b.rect.y>=253 and b.rect.y<=293 and b.rect.x>=175 and b.rect.x<=195:
                print('down')
                b.rect.x=177
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            #three
            if b.rect.x>=345 and b.rect.x<=385 and b.rect.y+20>=358 and b.rect.y+20<=378:
                print('right')
                b.rect.y=338
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break
            if b.rect.x>=345 and b.rect.x<=385 and b.rect.y>=378 and b.rect.y<=398:
                print('right')
                b.rect.y=400
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break
            if b.rect.y>=358 and b.rect.y<=398 and b.rect.x+20>=345 and b.rect.x+20<=365:
                print('up')
                b.rect.x=325
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            if b.rect.y>=358 and b.rect.y<=398 and b.rect.x>=365 and b.rect.x<=385:
                print('up')
                b.rect.x=387
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            #four
            if b.rect.x>=677 and b.rect.x<=717 and b.rect.y+20>=144 and b.rect.y+20<=164:
                print('left')
                b.rect.y=124
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break 
            if b.rect.x>=677 and b.rect.x<=717 and b.rect.y>=164 and b.rect.y<=184:
                print('left')
                b.rect.y=186
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break
            if b.rect.y>=144 and b.rect.y<=184 and b.rect.x+20>=677 and b.rect.x+20<=697:
                print('down')
                b.rect.x=657
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            if b.rect.y>=144 and b.rect.y<=184 and b.rect.x>=697 and b.rect.x<=717:
                print('down')
                b.rect.x=719
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
            #five
            if b.rect.x>=567 and b.rect.x<=607 and b.rect.y+20>=278 and b.rect.y+20<=298:
                print('left')
                b.rect.y=258
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break
            if b.rect.x>=567 and b.rect.x<=607 and b.rect.y>=298 and b.rect.y<=318:
                print('left')
                b.rect.y=320
                direction = 'left'
                AIDirection.append(direction)
                a_change = (snakewidth + margin) * -1
                b_change = 0
                break
            if b.rect.y>=278 and b.rect.y<=318 and b.rect.x+20>=567 and b.rect.x+20<=587:
                print('up')
                b.rect.x=547
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            if b.rect.y>=278 and b.rect.y<=318 and b.rect.x>=587 and b.rect.x<=607:
                print('up')
                b.rect.x=609
                direction = 'up'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin) * -1
                break
            #six
            if b.rect.x>=325 and b.rect.x<=365 and b.rect.y+20>=35 and b.rect.y+20<=75:
                print('right')
                b.rect.y=15
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break 
            if b.rect.x>=325 and b.rect.x<=365 and b.rect.y>=75 and b.rect.y<=95:
                print('right')
                b.rect.y=97
                direction='right'
                AIDirection.append(direction)
                a_change=(snakewidth + margin)
                b_change=0
                break 
            if b.rect.y>=35 and b.rect.y<=95 and b.rect.x+20>=325 and b.rect.x+20<=345:
                print('down')
                b.rect.x=305
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break  
            if b.rect.y>=35 and b.rect.y<=95 and b.rect.x>=345 and b.rect.x<=365:
                print('down')
                b.rect.x=3675
                direction = 'down'
                AIDirection.append(direction)
                a_change = 0
                b_change = (snakeheight + margin)
                break
                    
        if len(AIDirection)>2:
            AIDirection.pop(0) #keep track of AI direction

        for b in badsnake_segments2:
            #one
            if b.rect.x>=50 and b.rect.x<=90 and b.rect.y+20>=82 and b.rect.y+20<=102:
                print('right')
                b.rect.y=62
                direction='right'
                AIDirection2.append(direction)
                f_change=(snakewidth + margin)
                g_change=0
                break
            if b.rect.x>=50 and b.rect.x<=90 and b.rect.y>=102 and b.rect.y<=122:
                print('right')
                b.rect.y=124
                direction='right'
                AIDirection2.append(direction)
                f_change=(snakewidth + margin)
                g_change=0
                break
            if b.rect.y>=82 and b.rect.y<=122 and b.rect.x+20>=50 and b.rect.x+20<=70:
                print('down')
                b.rect.x=30
                direction = 'down'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin)
                break
            if b.rect.y>=82 and b.rect.y<=122 and b.rect.x>=70 and b.rect.x<=90:
                print('down')
                b.rect.x=92
                direction = 'down'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin)
                break
            #two
            if b.rect.x>=155 and b.rect.x<=195 and b.rect.y+20>=253 and b.rect.y+20<=273:
                print('right')
                b.rect.y=233
                direction='right'
                AIDirection2.append(direction)
                f_change=(snakewidth + margin)
                g_change=0
                break
            if b.rect.x>=155 and b.rect.x<=195 and b.rect.y>=273 and b.rect.y<=293:
                print('right')
                b.rect.y=295
                direction='right'
                AIDirection2.append(direction)
                f_change=(snakewidth + margin)
                g_change=0
                break
            if b.rect.y>=253 and b.rect.y<=293 and b.rect.x+20>=155 and b.rect.x+20<=175:
                print('down')
                b.rect.x=135
                direction = 'down'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin)
                break
            if b.rect.y>=253 and b.rect.y<=293 and b.rect.x>=175 and b.rect.x<=195:
                print('down')
                b.rect.x=177
                direction = 'down'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin)
                break
            #three
            if b.rect.x>=345 and b.rect.x<=385 and b.rect.y+20>=358 and b.rect.y+20<=378:
                print('right')
                b.rect.y=338
                direction='right'
                AIDirection2.append(direction)
                f_change=(snakewidth + margin)
                g_change=0
                break
            if b.rect.x>=345 and b.rect.x<=385 and b.rect.y>=378 and b.rect.y<=398:
                print('right')
                b.rect.y=400
                direction='right'
                AIDirection2.append(direction)
                f_change=(snakewidth + margin)
                g_change=0
                break
            if b.rect.y>=358 and b.rect.y<=398 and b.rect.x+20>=345 and b.rect.x+20<=365:
                print('up')
                b.rect.x=325
                direction = 'up'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin) * -1
                break
            if b.rect.y>=358 and b.rect.y<=398 and b.rect.x>=365 and b.rect.x<=385:
                print('up')
                b.rect.x=387
                direction = 'up'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin) * -1
                break
            #four
            if b.rect.x>=677 and b.rect.x<=717 and b.rect.y+20>=144 and b.rect.y+20<=164:
                print('left')
                b.rect.y=124
                direction = 'left'
                AIDirection2.append(direction)
                f_change = (snakewidth + margin) * -1
                g_change = 0
                break 
            if b.rect.x>=677 and b.rect.x<=717 and b.rect.y>=164 and b.rect.y<=184:
                print('left')
                b.rect.y=186
                direction = 'left'
                AIDirection2.append(direction)
                f_change = (snakewidth + margin) * -1
                g_change = 0
                break
            if b.rect.y>=144 and b.rect.y<=184 and b.rect.x+20>=677 and b.rect.x+20<=697:
                print('down')
                b.rect.x=657
                direction = 'down'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin)
                break
            if b.rect.y>=144 and b.rect.y<=184 and b.rect.x>=697 and b.rect.x<=717:
                print('down')
                b.rect.x=719
                direction = 'down'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin)
                break
            #five
            if b.rect.x>=567 and b.rect.x<=607 and b.rect.y+20>=278 and b.rect.y+20<=298:
                print('left')
                b.rect.y=258
                direction = 'left'
                AIDirection2.append(direction)
                f_change = (snakewidth + margin) * -1
                g_change = 0
                break
            if b.rect.x>=567 and b.rect.x<=607 and b.rect.y>=298 and b.rect.y<=318:
                print('left')
                b.rect.y=320
                direction = 'left'
                AIDirection2.append(direction)
                f_change = (snakewidth + margin) * -1
                g_change = 0
                break
            if b.rect.y>=278 and b.rect.y<=318 and b.rect.x+20>=567 and b.rect.x+20<=587:
                print('up')
                b.rect.x=547
                direction = 'up'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin) * -1
                break
            if b.rect.y>=278 and b.rect.y<=318 and b.rect.x>=587 and b.rect.x<=607:
                print('up')
                b.rect.x=609
                direction = 'up'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin) * -1
                break
            #six
            if b.rect.x>=325 and b.rect.x<=365 and b.rect.y+20>=35 and b.rect.y+20<=75:
                print('right')
                b.rect.y=15
                direction='right'
                AIDirection2.append(direction)
                f_change=(snakewidth + margin)
                g_change=0
                break 
            if b.rect.x>=325 and b.rect.x<=365 and b.rect.y>=75 and b.rect.y<=95:
                print('right')
                b.rect.y=97
                direction='right'
                AIDirection2.append(direction)
                f_change=(snakewidth + margin)
                g_change=0
                break 
            if b.rect.y>=35 and b.rect.y<=95 and b.rect.x+20>=325 and b.rect.x+20<=345:
                print('down')
                b.rect.x=305
                direction = 'down'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin)
                break  
            if b.rect.y>=35 and b.rect.y<=95 and b.rect.x>=345 and b.rect.x<=365:
                print('down')
                b.rect.x=367
                direction = 'down'
                AIDirection2.append(direction)
                f_change = 0
                g_change = (snakeheight + margin)
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

                #if there is more than two directions, remove first term in list
                if len(Direction)>2:
                    Direction.pop(0)

        if len(Apples)==1: #if there is an apple            
            for s in badsnake_segments: #follow the apple up or down
                for a in Apples:   
                    if (s.rect.x < a.rect.x and s.rect.y > a.rect.y):
                        #print('up')
                        direction = 'up'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin) * -1
                        break
                    if (s.rect.x < a.rect.x and s.rect.y < a.rect.y):
                        #print('down')
                        direction = 'down'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)
                        break
                    if (s.rect.x > a.rect.x and s.rect.y > a.rect.y):
                        #print('up')
                        direction = 'up'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin) * -1
                        break
                    if (s.rect.x > a.rect.x and s.rect.y < a.rect.y):
                        #print('down')
                        direction = 'down'
                        AIDirection.append(direction)
                        a_change = 0
                        b_change = (snakeheight + margin)
                        break
                            
                if len(AIDirection)>2:
                    AIDirection.pop(0) #keep track of AI direction
            
            for s in badsnake_segments: #if the apple and the snake are at the same position - ish, go to apple
                for a in Apples:
                    if (s.rect.y < (a.rect.y + 5)) and (s.rect.y > (a.rect.y - 5)) and ((s.rect.x < a.rect.x)):
                        #print('right')
                        direction = 'right'
                        AIDirection.append(direction)
                        a_change = (snakewidth + margin)
                        b_change = 0
                        break
                    if (s.rect.y < (a.rect.y + 5)) and (s.rect.y > (a.rect.y - 5)) and ((s.rect.x > a.rect.x)):
                        #print('left')
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
                    #print('up')
                    direction = 'up'
                    AIDirection2.append(direction)
                    f_change = 0
                    g_change = (snakeheight + margin) * -1
                    break

                if (b.rect.x < s.rect.x and b.rect.y < s.rect.y):
                    #print('down')
                    direction = 'down'
                    AIDirection2.append(direction)
                    f_change = 0
                    g_change = (snakeheight + margin)
                    break

                if (b.rect.x > s.rect.x and b.rect.y > s.rect.y):
                    #print('up')
                    direction = 'up'
                    AIDirection2.append(direction)
                    f_change = 0
                    g_change = (snakeheight + margin) * -1
                    break
                
                if (b.rect.x > s.rect.x and b.rect.y < s.rect.y):
                    #print('down')
                    direction = 'down'
                    AIDirection2.append(direction)
                    f_change = 0
                    g_change = (snakeheight + margin)
                    break

            if len(AIDirection2)>2:
                AIDirection2.pop(0) #keep track of AI direction

        for b in badsnake_segments2: #if the AI snake and the snake are at the same position - ish, go to snake
            for s in snake_segments:
                if (b.rect.y <= (s.rect.y + 20)) and (b.rect.y >= (s.rect.y - 20)) and ((b.rect.x <= s.rect.x)):
                    #print('right')
                    direction = 'right'
                    AIDirection2.append(direction)
                    f_change = (snakewidth + margin)
                    g_change = 0
                    break
                if (b.rect.y <= (s.rect.y + 20)) and (b.rect.y >= (s.rect.y - 20)) and ((b.rect.x >= s.rect.x)):
                    #print('left')
                    direction = 'left'
                    AIDirection2.append(direction)
                    f_change = (snakewidth + margin) * -1
                    g_change = 0
                    break
                
            if len(AIDirection2)>2:
                AIDirection2.pop(0) #keep track of AI direction
                        
        #continuously update snake to maintain length
        old_segment = snake_segments.pop()
        all_sprites_list.remove(old_segment)

        old_segment=badsnake_segments.pop()
        all_sprites_list.remove(old_segment)

        old_segment=badsnake_segments2.pop()
        all_sprites_list.remove(old_segment)

        if len(badsnake_segments)<=0 and len(badsnake_segments2)<=0:
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

                if score >= listscore[0]:  # if the score is >=highscore
                    end_it = False
                    while (end_it == False):
                        # blit highscore on screen
                        textbasics = pygame.font.Font("C:\Windows\Fonts\Calibri.ttf", 40)
                        overobj = textbasics.render('YOU GOT A HIGHSCORE!', True, RED)
                        overrect = overobj.get_rect()
                        overrect.centerx = DISPLAYSURF.get_rect().centerx
                        overrect.centery = DISPLAYSURF.get_rect().centery - 90
                        DISPLAYSURF.blit(overobj, overrect)
                        end_it = True
                    pygame.display.flip()
                #blit you win on screen
                overobj = textbasics.render('You Win!', True, RED)
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
                scoreobj=textbasics.render('Click to Play Again', True, RED)
                scorerect=scoreobj.get_rect()
                scorerect.centerx=DISPLAYSURF.get_rect().centerx
                scorerect.centery=DISPLAYSURF.get_rect().centery+90
                DISPLAYSURF.blit(scoreobj, scorerect)

                for event in pygame.event.get():
                    #if click screen, go to start screen
                    if event.type==MOUSEBUTTONDOWN:
                        bgmusic.stop()
                        start()
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

        if len(snake_segments)<=0:
            gameover(bgmusic)
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
        titlerect.y = 0
        DISPLAYSURF.blit(titleobj,titlerect)        
        
        pygame.display.flip()

        clock.tick(ticker)

        create-=1 #subtract from create to keep track of apple spawning
        all_sprites_list.remove(old_segment)

hardobstaclegame()
