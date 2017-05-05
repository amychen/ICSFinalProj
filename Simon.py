import random, sys, time, pygame
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 810
WINDOWHEIGHT = 500
FLASHDELAY = 200
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

XMARGIN = int((WINDOWWIDTH - 2*BUTTONSIZE - BUTTONGAP) / 2)
YMARGIN = int((WINDOWHEIGHT - 2*BUTTONSIZE - BUTTONGAP) / 2)

YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAP, YMARGIN, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAP, YMARGIN + BUTTONSIZE + BUTTONGAP, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAP, BUTTONSIZE, BUTTONSIZE)

def main():
    
    global DISPLAY, YELLOWSOUND, GREENSOUND, BLUESOUND, REDSOUND
    
    pygame.init()
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    
    #sound played with every BRIGHT color
    YELLOWSOUND = pygame.mixer.Sound("beep1.ogg")
    GREENSOUND = pygame.mixer.Sound("beep2.ogg")
    BLUESOUND = pygame.mixer.Sound("beep3.ogg")
    REDSOUND = pygame.mixer.Sound("beep4.ogg")
    
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Decipher the code.', 1, (0,0,0))
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)
    
    #start of the game
    pattern = []
    currentStep = 0 
    score = 0
    
    #person is playing the Simon
    waitforPlayer = False
    
    #player is looking to follow Simon
    while True:
        clicked = None
        DISPLAY.fill((255, 255, 255))
        drawButtons()

        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, (0, 0, 0))
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        
        DISPLAY.blit(scoreSurf, scoreRect)
        DISPLAY.blit(infoSurf, infoRect)
        
        checkForQuit()
        
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clicked = getButtonClicked(mousex, mousey)
        
        ###IMPLEMENT: THIS IS WHERE THE PLAYER CAN BE SIMON
        if not waitforPlayer:
            pygame.display.update()
            pygame.time.wait(500)
            pattern.append(random.choice((YELLOW, RED, BLUE, GREEN)))
            for button in pattern:
                flashAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitforPlayer = True
        ##IMPLEMENT: THIS IS WHERE THE PLAYER HAS TO TRY TO FIGURE OUT THE PATTERN
        else:
            if clicked and clicked == pattern[currentStep]:
                flashAnimation(clicked)
                currentStep += 1 
                
                if currentStep == len(pattern):
                    drawButtons()
                    score += 1 
                    waitforPlayer = False
                    currentStep = 0 
                    
            elif clicked and clicked != pattern[currentStep]:
                gameOver()
                
                pattern = []
                currentStep = 0 
                score = 0
                waitforPlayer = False
                drawButtons()
        
        pygame.display.update()
        

def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint((x,y)):
        return YELLOW
    elif GREENRECT.collidepoint((x,y)):
        return GREEN
    elif BLUERECT.collidepoint((x,y)):
        return BLUE
    elif REDRECT.collidepoint((x,y)):
        return RED
    else:
        return None
    
def flashAnimation(color, animationSpeed = 50):
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
        
    origSurf = DISPLAY.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    
    #brighten then dim
    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAY.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAY.blit(flashSurf, rect.topleft)
            pygame.display.update()
    DISPLAY.blit(origSurf, (0, 0))
    
def drawButtons():
    #draws out the game buttons
    pygame.draw.rect(DISPLAY, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAY, GREEN, GREENRECT)
    pygame.draw.rect(DISPLAY, BLUE, BLUERECT)
    pygame.draw.rect(DISPLAY, RED, REDRECT)

def gameOver(color = (0, 0, 0), animationSpeed = 50):


    origSurf = DISPLAY.copy()
    flashSurf = pygame.Surface(DISPLAY.get_size())
    flashSurf = flashSurf.convert_alpha()
    YELLOWSOUND.play() # play all four beeps at the same time, roughly.
    BLUESOUND.play()
    GREENSOUND.play()
    REDSOUND.play()
    r, g, b = color
    for i in range(3): # do the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animationSpeed * step): # animation loop
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAY.blit(origSurf, (0, 0))
                DISPLAY.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        leave() # terminate if any QUIT events are present
        for event in pygame.event.get(KEYUP): # get all the KEYUP events
            if event.key == K_ESCAPE:
                leave() # terminate if the KEYUP event was for the Esc key
            pygame.event.post(event) # put the other KEYUP event objects back

def leave():
    pygame.quit()
    sys.exit()
    
    
if __name__ == '__main__':
    main()