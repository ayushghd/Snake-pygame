import pygame
import time
import random
pygame.init()

white=(255,255,255)
blue=(0,0,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
display_Width=800
display_Height=600
gameDisplay = pygame.display.set_mode((display_Width,display_Height))
pygame.display.set_caption('SNAKE GAME')
block_size=15
apple_thickness=30
clock = pygame.time.Clock()
FPS=30
smallfont=pygame.font.SysFont("comicsansms",20)
mediumfont=pygame.font.SysFont("comicsansms",40)
largefont=pygame.font.SysFont("comicsansms",60)
appleimg = pygame.image.load('apple.png')
snakeimg = pygame.image.load('snake.png')
highest=0

def intro_to_game():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_c:
                    intro=False
                    
        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake Game",green,-150,"large")
        message_to_screen("The objective of the game is to eat as many apples as possible",black,-50,"small")
        message_to_screen("The more you eat, the more you get longer",black,0,"small")
        message_to_screen("If you bump into the walls or into yourself, YOU DIE",black,50,"small")
        message_to_screen("To play press C, to quit press Q",black,150,"small")
        message_to_screen("To pause the game in middle, press P",black,200,"small")
        
        
        pygame.display.update()
        clock.tick(15)
        
def highscore(highest):
    text=smallfont.render("High Score : "+str(highest),True,black)
    gameDisplay.blit(text,[600,0])
    
def score(score):
    text =  smallfont.render("Score : "+str(score),True,black)
    gameDisplay.blit(text,[0,0])

def pause():
    paused=True
    message_to_screen("Paused",black,-100,"large")
    message_to_screen("Press C to continue playing, Press Q to quit",black,0,"small")
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_c:
                    paused=False        
        clock.tick(10)
            
def snake(snakelist,block_size):
    for xny in snakelist:
        pygame.draw.rect(gameDisplay,blue,[xny[0],xny[1],block_size,block_size])

def rand_apple_fun():
    rand_apple_x=round(random.randrange(0,display_Width-apple_thickness))
    rand_apple_y=round(random.randrange(0,display_Height-apple_thickness))
    return rand_apple_x,rand_apple_y


def text_objects(msg,color,size):
    if size=="small":
        textSurf=smallfont.render(msg,True,color)
    elif size=="medium":
        textSurf=mediumfont.render(msg,True,color)
    elif size=="large":
        textSurf=largefont.render(msg,True,color)
    
    return textSurf,textSurf.get_rect()
    
def message_to_screen(msg,color,y_displace=0,size="small"):
    #gameDisplay.blit(screen_text,[display_Width/4,display_Height/2])
    textSurf,textRect = text_objects(msg,color,size)
    textRect.center = (display_Width/2),(display_Height/2) + y_displace
    gameDisplay.blit(textSurf,textRect)

    
def gameLoop(highest):
    gameFalse = False
    gameOver = False
    lead_x=display_Width/2
    lead_y=display_Height/2
    lead_x_change=0
    lead_y_change=0
    snakelist=[]
    snakelength=1
    rand_apple_x,rand_apple_y=rand_apple_fun()

    while not gameFalse:

        if gameOver == True:
            message_to_screen("Game Over",red,-50,size="large")
            message_to_screen("Press C to continue playing or Q to quit",black,50,size="medium")
            pygame.display.update()

        while gameOver==True:            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    gameFalse=True
                    gameOver=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        gameFalse=True
                        gameOver=False
                    if event.key==pygame.K_c:
                        gameLoop(highest)
                    
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameFalse=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT and lead_x_change!=block_size:
                    lead_x_change=-block_size
                    lead_y_change=0
                elif event.key==pygame.K_RIGHT and lead_x_change!=-block_size:
                    lead_x_change=block_size
                    lead_y_change=0
                elif event.key==pygame.K_UP and lead_y_change!=block_size:
                    lead_y_change=-block_size
                    lead_x_change=0
                elif event.key==pygame.K_DOWN and lead_y_change!=-block_size:
                    lead_y_change=block_size
                    lead_x_change=0
                elif event.key==pygame.K_p:
                    pause()

        if lead_x >= display_Width or lead_x < 0 or lead_y >= display_Height or lead_y < 0:
            gameOver = True
        lead_x+=lead_x_change
        lead_y+=lead_y_change

        snakehead=[]
        snakehead.append(lead_x)
        snakehead.append(lead_y)
        snakelist.append(snakehead);

        if len(snakelist) > snakelength:
            del snakelist[0]

        for segment in snakelist[:-1]:
            if segment == snakehead:
                gameOver = True
        gameDisplay.fill(white)
        #pygame.draw.rect(gameDisplay,red,[rand_apple_x,rand_apple_y,apple_thickness,apple_thickness])
        gameDisplay.blit(appleimg,(rand_apple_x,rand_apple_y))
        snake(snakelist,block_size)
        #gameDisplay.fill(red,rect=[lead_x,lead_y,10,10])
        score(snakelength-1)
        if highest < snakelength-1:
            highest=snakelength-1
        highscore(highest)
        pygame.display.update()

        if lead_x>=rand_apple_x and lead_x<=rand_apple_x+apple_thickness or lead_x + block_size > rand_apple_x and lead_x + block_size < rand_apple_x + apple_thickness:
            if lead_y>=rand_apple_y and lead_y<=rand_apple_y+apple_thickness or lead_y + block_size > rand_apple_y and lead_y + block_size < rand_apple_y + apple_thickness:
                snakelength+=1
                rand_apple_x,rand_apple_y=rand_apple_fun()

        clock.tick(FPS)
        
    quit()
    pygame.quit()
intro_to_game()
gameLoop(highest)
