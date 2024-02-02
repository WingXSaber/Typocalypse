#Import Built-in Modules
import sys;
import os;
import time as time;

#Import Third Party Modules
import pygame as pyg;
from pygame.locals import *;    #for keywords such as event 

#Import and initialize Project Modules ======================================
from Core import Core;
from ObjectPlayer import ObjectPlayer;
from ObjectEnemy import ObjectEnemy;
#from StateMachine import State, generate_transition_table


class Typocalpyse():
    
    def __init__(self):        
        #Initialze Pygame  =========================================================
        pyg.init();                          
        self.pygClock = pyg.time.Clock();    #Initialze Pygame's clock
        #Initialize game loop variables ============================================
        self.UPDATE_TICKRATE = 30;     #target logic rate
        self.DISPLAY_FRAMERATE = 60;    #target display FPS
        
        self.updateTickCount = 0; #count current ticks have displayed
        self.updateAverageTPS = 0; #count average ticks have displayed per second

        self.displayFrameCount = 0; #count current frames have displayed
        self.displayAverageFPS = 0; #count average frames have displayed per second

        self.isRunning = True;  #Flag for whole application if running
        self.isPaused = False;  #Flag for application if paused (like minimized)
        
        self.isDebugMode = False;    #flag for showing debug details or not

        #Initialize modules of Typocalypse =========================================
        self.core = Core(); #initialized first, it contains variables shared by other modules        
        
        self.player = ObjectPlayer(self.core, 500, 500, 20, 20, 10);  
        self.enemy1 = ObjectEnemy(self.core, 250, 250, 20, 20, 10);  
        self.enemy2 = ObjectEnemy(self.core, 500, 250, 20, 20, 10);  
        self.enemy3 = ObjectEnemy(self.core, 750, 250, 20, 20, 10);  
        
        self.core.addToObjectList(self.player);
        self.core.addToObjectList(self.enemy1);
        self.core.addToObjectList(self.enemy2);
        self.core.addToObjectList(self.enemy3);
        
        self.__run__();
    


    def __tick__(self, deltaTime):      
        
        #Getting the current event list available and execute action        
        for event in pyg.event.get():            
            # Events ========================================================            
            
            #if event.type == pyg.VIDEORESIZE:     #when window is resized
            #    #Update Camera
            #    #camera["x"] -= (event.size[0]-SCREEN_WIDTH)/2;
            #    #camera["y"] -= (event.size[1]-SCREEN_HEIGHT)/2;
            #    #Update current window size
            #    self.window.screenWidth = event.size[0];
            #    self.window.screenHeight = event.size[1];         
            if (event.type== pyg.locals.QUIT): #when exit buttton event is pressed   
                self.isRunning = False;     
                
            # Inputs ========================================================    
            self.core.eventCheck(event);
        #            
        #        
        ##Update Objects =====================================================          
       
        #self.enemy1.tick(deltaTime);
        #self.enemy2.tick(deltaTime);
        #self.enemy3.tick(deltaTime);
        #self.player.tick(deltaTime);
        for obj in self.core.gameObjectList:
            obj.tick(deltaTime);
        
       
        
        #Update UI ==========================================================    
        pass;
    
    def __render__(self):
        self.core.mainSurface.fill(pyg.Color(128, 128, 128)); #(re)fill screen with background color    
        #self.mainSurface.blit(self.font.render("dt:"+str(deltaTime), True, (0,0,0)), (10, 10));        
        self.core.mainSurface.blit(self.core.fontDefault.render("TPS:"+str(round(self.updateAverageTPS)), True, (0,0,0)), (10, 10));            
        self.core.mainSurface.blit(self.core.fontDefault.render("FPS:"+str(round(self.displayAverageFPS)), True, (0,0,0)), (10, 50));            
        self.core.mainSurface.blit(self.core.fontDefault.render("width:"+ str(self.core.mainSurface.get_width()), True, (0,0,0)), (10, 150));            
        self.core.mainSurface.blit(self.core.fontDefault.render("height:"+str(self.core.mainSurface.get_height()), True, (0,0,0)), (10, 200));            
        #self.core.mainSurface.blit(self.core.fontDefault.render("width:"+ str(self.window.screenWidth),  True, (0,0,0)), (150, 150));            
        #self.core.mainSurface.blit(self.co re.fontDefault.render("height:"+str(self.window.screenHeight), True, (0,0,0)), (150, 200));            
        #pyg.draw.rect(self.core.mainSurface, pyg.Color(0,0,0), (0,0,self.core.mainSurface.get_width()/2, self.core.mainSurface.get_height()/2), 2);
        
        
        #pyg.draw.rect(self.core.mainSurface, pyg.Color(0,0,0), (self.enemy1.x, self.enemy1.y, self.enemy1.sizeX, self.enemy1.sizeY ), 2);
        #pyg.draw.rect(self.core.mainSurface, pyg.Color(0,0,0), (self.enemy2.x, self.enemy2.y, self.enemy2.sizeX, self.enemy2.sizeY ), 2);
        #pyg.draw.rect(self.core.mainSurface, pyg.Color(0,0,0), (self.enemy3.x, self.enemy3.y, self.enemy3.sizeX, self.enemy3.sizeY ), 2);
        #self.player.render();
        #self.enemy1.render();
        #self.enemy2.render();
        #self.enemy3.render();
        for obj in self.core.gameObjectList:
            obj.render();
        
        
        pyg.display.update();  #refresh the display and render 
        
    
    def __stop__(self):        
        print("See You Space Cowboy.");
        pyg.quit();          #Quit Pygame
        sys.exit()           #Quit entire program   
    
    def __run__(self):
        #Jeric's Game Loop

        #Calculate how many ns each frame should take for our target update framerate.
        TIME_BETWEEN_UPDATES = 1000000000 / self.UPDATE_TICKRATE;                        
        #Think of MAX_UPDATES_BEFORE_RENDER as similar to buffered updates.
        #If worried about visual hitches more than perfect timing, set this to 1.
        MAX_UPDATES_BEFORE_RENDER = 5;                
        lastUpdateTime = time.time_ns(); #Store the last update time.
                                
        #If we are able to get as high as this FPS, don't render again.        
        TARGET_TIME_BETWEEN_RENDERS = 1000000000 / self.DISPLAY_FRAMERATE;                        
        lastRenderTime =time.time_ns(); #Store the last time we rendered.               
        
        #Simple timer for finding TPS and FPS.
        lastSecondTime = int(lastUpdateTime / 1000000000);

        #Main Gane Loop =============================================================
        while(self.isRunning):  
            
            now = time.time_ns(); #Current time in nanoseconds
            
            if (not self.isPaused):
                # UPDATE CALLS ============================================================                
                #Using a loop for calling tick()
                #At the very most we will update the game this many times before a new render.
                #This is done so physics is more consistent at the cost of visuals        
                currentTickCount = 0;                
                while (now - lastUpdateTime > TIME_BETWEEN_UPDATES and currentTickCount < MAX_UPDATES_BEFORE_RENDER):
                    
                    #deltaTime is multiplied to any value that changes over time: such as velocity
                    #Do not multiply deltaTime to anything that is a fixed value: such as speed, distance                    
                    deltaTime = self.UPDATE_TICKRATE * (now - lastUpdateTime)  / 1000000000           
                    
                    #Call the main update method + use deltaTime
                    self.__tick__(deltaTime);          
                             
                    #Used for Counter: for Tick rate            
                    self.updateTickCount +=1;                    
                    lastUpdateTime = now;  
                    
                    currentTickCount+=1; #To find out how many ticks we have done.
                    
                                           
                # RENDER CALLS ===========================================================
                now = time.time_ns();
                if (now - lastRenderTime > TARGET_TIME_BETWEEN_RENDERS):
                    #Call the main render method
                    self.__render__(); 
                    
                    #Used for Counter: for render rate            
                    self.displayFrameCount+=1;
                    lastRenderTime = now;                               
                
                
                #Counter: Update the frames we got for counter.============================
                currentSecondTime = int(lastUpdateTime / 1000000000);
                if (currentSecondTime > lastSecondTime):              
                   self.updateAverageTPS = self.updateTickCount;
                   self.updateTickCount = 0;             
                    
                   self.displayAverageFPS = self.displayFrameCount;
                   self.displayFrameCount = 0;             
                   
                   #refresh timer  
                   lastSecondTime = currentSecondTime;
               
            else: #if paused                 
                 lastUpdateTime = now;
                 lastRenderTime = now;

            #Since window could be resized, we re-assign the values.
            #ideally we should just put this in a Eventlistener of the window, but this works.
            #windowWidth = gameWindow.getCanvasWidth();
            #windowHeight = gameWindow.getCanvasHeight();    
            #windowWidth = gameWindow.frame.getWidth();
            #windowHeight = gameWindow.frame.getHeight() - gameWindow.frame.getInsets().top;    
        

            """
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
            """
        
        self.__stop__();


#Execute this class as main class.
if __name__ == "__main__":
    game = Typocalpyse();
    

