#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 18:48:22 2017

@author: xijiaqi1997
"""
import pygame, random, sys, time
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 810
WINDOWHEIGHT = 500
FLASHDELAY = 150
BUTTONSIZE = 200
BUTTONGAP = 20 
TIMEOUT = 5

REDFLASH = (255, 0, 0)
GREENFLASH = (0, 255, 0)
BLUEFLASH = (0, 0, 255)
YELLOWFLASH = (255, 255, 0)

RED = (255, 78, 78)
GREEN = (100, 255, 166)
BLUE = (0, 205, 255)
YELLOW = (255, 255, 153)

X_MARGIN = int((WINDOWWIDTH - 2*BUTTONSIZE - BUTTONGAP)/2)
Y_MARGIN = int((WINDOWHEIGHT - 2*BUTTONSIZE - BUTTONGAP)/2)

pygame.init()
pygame.display.set_mode((640,480))
YELLOWRECT = pygame.Rect(X_MARGIN, Y_MARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(X_MARGIN+BUTTONSIZE+BUTTONGAP, Y_MARGIN, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(X_MARGIN, Y_MARGIN+BUTTONSIZE+BUTTONGAP, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(X_MARGIN+BUTTONSIZE+BUTTONGAP, Y_MARGIN+BUTTONSIZE+BUTTONGAP, BUTTONSIZE, BUTTONSIZE)

def simon(commands):
    global SCREEN, YELLOWSOUND,  BLUESOUND, GREENSOUND, REDSOUND
    
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    YELLOWSOUND = pygame.mixer.Sound('beep1.ogg')
    BLUESOUND = pygame.mixer.Sound('beep2.ogg')
    GREENSOUND = pygame.mixer.Sound('beep3.ogg')
    REDSOUND = pygame.mixer.Sound('beep4.ogg')
    
    BASICFONT = pygame.font.Font('freesansbold.ttf',16)
    infoSurf = BASICFONT.render("Let's get your chat started!", 1, (0,0,0))
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWWIDTH-25)
    
    score = 0
    bout = 0
    currentStep = 0
    pattern = []
    #dec_pattern = []
    
    waitforPlayer = False
    
    while bout < 5:
        clicked = None
        SCREEN.fill((255,255,255))
        drawButtons()
        
        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, (0, 0, 0))
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH-100, 10)
        
        SCREEN.blit(scoreSurf,scoreRect)
        SCREEN.blit(infoSurf, infoRect)
        
        checkforQuit()
        
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clicked = getButtonClick(mousex, mousey)
        
        if not waitforPlayer:
            pygame.display.update()
            pygame.time.wait(500)
            for i in range(len(commands[bout])):
                pattern.append((YELLOW, BLUE, GREEN, RED)[commands[bout][i]])
                #dec_pattern.append((YELLOW, BLUE, GREEN, RED)[dec_commands[bout][i]])
            for button in pattern:
                flashAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitforPlayer = True
        
        else:
            if clicked and clicked == pattern[currentStep]:
                flashAnimation(clicked)
                currentStep += 1
                
                if currentStep == len(pattern):
                    drawButtons()
                    score += 1
                    currentStep = 0
                    waitforPlayer = False
                    pattern = []
                    #dec_pattern = []
                    bout += 1
            
            elif clicked and clicked != pattern[currentStep]:
                gameOver()
                currentStep = 0
                waitforPlayer = False
                pattern = []
                #dec_pattern = []
                drawButtons()
                bout += 1

              
        pygame.display.update()
    
    leave()    
    return score

def getButtonClick(x,y):
    if YELLOWRECT.collidepoint((x,y)):
        return YELLOW
    elif BLUERECT.collidepoint((x,y)):
        return BLUE
    elif GREENRECT.collidepoint((x,y)):
        return GREEN
    elif REDRECT.collidepoint((x,y)):
        return RED
    else:
        return None

def flashAnimation(color,speed = 50):
    if color == YELLOW:
        sound = YELLOWSOUND
        flashColor = YELLOWFLASH
        rect = YELLOWRECT
    elif color == BLUE:
        sound = BLUESOUND
        flashColor = BLUEFLASH
        rect = BLUERECT
    elif color == RED:
        sound = REDSOUND
        flashColor = REDFLASH
        rect = REDRECT
    elif color == GREEN:
        sound = GREENSOUND
        flashColor = GREENFLASH
        rect = GREENRECT
     
    origSurf = SCREEN.copy()
    flashSurf = pygame.Surface((BUTTONSIZE,BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r,g,b = flashColor
    sound.play()
    
    for start, end, step in ((0,255,1),(255,0,-1)):
        for alpha in range(start,end,step*speed):
            checkforQuit()
            SCREEN.blit(origSurf,(0,0))
            flashSurf.fill((r,g,b,alpha))
            SCREEN.blit(flashSurf,rect.topleft)
            pygame.display.update()
    SCREEN.blit(origSurf,(0,0))
    
def drawButtons():
    pygame.draw.rect(SCREEN, YELLOW, YELLOWRECT)
    pygame.draw.rect(SCREEN, GREEN, GREENRECT)
    pygame.draw.rect(SCREEN, BLUE, BLUERECT)
    pygame.draw.rect(SCREEN, RED, REDRECT)
    
def gameOver(color=(0,0,0),speed = 50):
    origSurf = SCREEN.copy()
    flashSurf = pygame.Surface((BUTTONSIZE,BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    YELLOWSOUND.play()
    BLUESOUND.play()
    GREENSOUND.play()
    REDSOUND.play()
    r,g,b = color
    for i in range(4):
        for start, end, step in ((0,255,1),(255,0,-1)):
            for alpha in range(start,end,step*speed):
                checkforQuit()
                flashSurf.fill((r,g,b,alpha))
                SCREEN.blit(origSurf,(0,0))
                SCREEN.blit(flashSurf,(0,0))
                drawButtons()
                pygame.display.update()

def checkforQuit():
    for event in pygame.event.get(QUIT):
        leave()
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                leave()
        pygame.event.post(event)
        
def leave():
    pygame.quit()
    sys.exit()
    
#comment lines below when run real in chat_server
#if __name__ == '__main__':
    #simon([[0,3,2,1],[1,3,2,2],[2,3,0,0],[1,1,1,1],[2,0,0,1]],[[0,3,2,1],[1,3,2,3],[0,3,0,0],[1,1,0,1],[2,0,0,1]])           
            
    
               
    