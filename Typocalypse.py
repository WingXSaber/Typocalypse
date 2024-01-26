#Import Built-in Modules
import sys;
import os;
import time as time;

#Import Third Party Modules
import pygame as pyg;
from pygame.locals import *;    #for keywords such as event 

#Import and initialize Project Modules ======================================
import Window

#Initialize variables ======================= ===============================
pyg.init();                     #Initialze Pygame
pygClock = pyg.time.Clock();    #Initialze Pygame's clock

framerateCap = 60;      #Framerate limit, 0 is unlimited
TARGET_FRAMERATE = 60;  #targeted 'universal' framerate for all computers
prevTime = time.time(); #used for calculating deltaTime
#currentFrame = 0;       #current frame number
#currentFPS = 0;         #For FPS Display

isDebugMode = False;    #flag for showing debug details or not
  




timerFramerate = 0;


#Create Window and main display
mainSurface = pyg.display.set_mode((Window.screenWidth, Window.screenHeight), Window.DISPLAY_FLAGS);
mainSurface.fill(pyg.Color(128, 128, 128));     
pyg.display.update();  
     
    
#Initialize fonts ==========================================================
pyg.font.init();
font = pyg.font.SysFont('None',30);






rectPos = 0;
isRectForward = True;

#Main Gane Loop =============================================================
while(True):    
    #Limit Framerate of PyGame
    pygClock.tick(framerateCap);
    
    #compute the detla time, used for framerate independence of objects
    #we only multiply deltaTime to things that change over time, like assigning position, not constants like speed
    now = time.time();
    deltaTime = now - prevTime;
    prevTime = now;      
    
    #define 'scale', used to multiply to whatever value that is being updated. ie. Speed
    SCALE = TARGET_FRAMERATE * deltaTime; 
    
    # Update ========================================================
    for event in pyg.event.get():             #Getting the current event list available and execute action        
        #if event.type == pyg.VIDEORESIZE:     #when window is resized
            #Update Camera
            #camera["x"] -= (event.size[0]-SCREEN_WIDTH)/2;
            #camera["y"] -= (event.size[1]-SCREEN_HEIGHT)/2;
            #Update current window size
            #screenWidth = event.size[0];
            #screenHeight = event.size[1];         
        if (event.type== pyg.locals.QUIT):   #when exit buttton event is pressed   
            print("See You Space Cowboy.");
            pyg.quit();          #Quit Pygame
            sys.exit()           #Quit entire program     
        if event.type == pyg.KEYDOWN:
            print(pyg.key.name(event.key) );
            if event.key == pyg.K_F2:
                isDebugMode = not isDebugMode;
            if event.key == pyg.K_UP:
                framerateCap+=5;
            if event.key == pyg.K_DOWN and framerateCap -5 > 0:
                framerateCap-=5;
   
   
   
    
    if(isRectForward):
        rectPos+= 5 * SCALE;
    else:
        rectPos-= 5 * SCALE;
    
    if(rectPos <0):
        isRectForward = True;
    elif( rectPos > 500):
        isRectForward = False;
        
        
    # Render ========================================================= 
    mainSurface.fill(pyg.Color(128, 128, 128)); #(re)fill screen with background color
    
    mainSurface.blit(font.render("dt:"+str(deltaTime), True, (0,0,0)), (10, 10));        
    mainSurface.blit(font.render("FPS:"+str(round(pygClock.get_fps())), True, (0,0,0)), (10, 50));            
    mainSurface.blit(font.render("timer:"+str(round(timerFramerate/60,2)), True, (0,0,0)), (10, 100));            
    mainSurface.blit(font.render("width:"+str(mainSurface.get_width()), True, (0,0,0)), (10, 150));            
    mainSurface.blit(font.render("height:"+str(mainSurface.get_height()), True, (0,0,0)), (10, 200));            
   
    
    
    pyg.draw.rect(mainSurface, pyg.Color(0,0,0), (0,0,mainSurface.get_width()+1, mainSurface.get_height()+1), 2);
        
    pyg.draw.rect(mainSurface, pyg.Color(0,0,0), (rectPos, mainSurface.get_height()/2,50,50), 2);
           
    pyg.display.update();  #refresh the display and render 


    timerFramerate += deltaTime;
    #if(timerFramerate > 1):
    #    timerFramerate = 0;
    #    currentFrameRate = currentFrame;
    
    

