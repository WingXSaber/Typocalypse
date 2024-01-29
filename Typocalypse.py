#Import Built-in Modules
import sys;
import os;
import time as time;

#Import Third Party Modules
import pygame as pyg;
from pygame.locals import *;    #for keywords such as event 

#Import and initialize Project Modules ======================================
import Core;
import Window


class Typocalpyse():
    
    def __init__(self):
        #Initialize variables ======================= ===============================        
        pyg.init();                          #Initialze Pygame
        self.pygClock = pyg.time.Clock();    #Initialze Pygame's clock
        
        self.dir_path = os.path.dirname(os.path.realpath(__file__));  #Initialize path of the system        
        
        self.core = Core.Core();
        self.window = Window.Window(self);

        #framerateCap = 60;      #Framerate limit, 0 is unlimited
        #TARGET_FRAMERATE = 60;  #targeted 'universal' framerate for all computers
        #prevTime = time.time(); #used for calculating deltaTime
        #currentFrame = 0;       #current frame number
        #currentFPS = 0;         #For FPS Display

        self.isRunning = True;
        self.isDebugMode = False;    #flag for showing debug details or not

        #timerFramerate = 0;
                
        #Initialize fonts ==========================================================
        pyg.font.init();
        self.font = pyg.font.SysFont('None',30);

        

        self.UPDATE_FRAMERATE = 60;     #target logic rate
        self.DISPLAY_FRAMERATE = 30;    #target display FPS
        
        self.updateTickCount = 0; #count current ticks have displayed
        self.updateAverageTPS = 0; #count average ticks have displayed per second

        self.displayFrameCount = 0; #count current frames have displayed
        self.displayAverageFPS = 0; #count average frames have displayed per second

        self.isPaused = False;
        
        
        self.rectPos = 0;
        self.isRectForward = True;
        

        self.__run__();



    def __tick__(self):
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
                self.isRunning = False;     
            if (event.type== pyg.KEYDOWN):
                #print(pyg.key.name(event.key) );
                if (event.key == pyg.K_UP): 
                    pass;
                if (event.key == pyg.K_DOWN): 
                    pass;
                
                    
                
        if(self.isRectForward):
            self.rectPos+= 5;
        else:
            self.rectPos-= 5;   
        if(self.rectPos <0):
            self.isRectForward = True;
        elif( self.rectPos > 500):
            self.isRectForward = False;    
            
            
    
    def __render__(self):
        self.mainSurface.fill(pyg.Color(128, 128, 128)); #(re)fill screen with background color    
        #self.mainSurface.blit(self.font.render("dt:"+str(deltaTime), True, (0,0,0)), (10, 10));        
        self.mainSurface.blit(self.font.render("TPS:"+str(round(self.updateAverageTPS)), True, (0,0,0)), (10, 10));            
        self.mainSurface.blit(self.font.render("FPS:"+str(round(self.displayAverageFPS)), True, (0,0,0)), (10, 50));            
        self.mainSurface.blit(self.font.render("width:"+str(self.mainSurface.get_width()), True, (0,0,0)), (10, 150));            
        self.mainSurface.blit(self.font.render("height:"+str(self.mainSurface.get_height()), True, (0,0,0)), (10, 200));            
        pyg.draw.rect(self.mainSurface, pyg.Color(0,0,0), (0,0,self.mainSurface.get_width()+1, self.mainSurface.get_height()+1), 2);
        pyg.draw.rect(self.mainSurface, pyg.Color(0,0,0), (self.rectPos, self.mainSurface.get_height()/2,50,50), 2);
        
        pyg.display.update();  #refresh the display and render 
    
    def __stop__(self):        
        print("See You Space Cowboy.");
        pyg.quit();          #Quit Pygame
        sys.exit()           #Quit entire program   
    
    def __run__(self):
        #This game loop based on alleged Notch's Game Loop

        #Calculate how many ns each frame should take for our target game hertz.
        TIME_BETWEEN_UPDATES = 1000000000 / self.UPDATE_FRAMERATE;        
        #At the very most we will update the game this many times before a new render.
        #This is done so physics is more consistent at the cost of visuals
  
        #We will need the last update time.
        lastUpdateTime = time.time_ns();
        #Store the last time we rendered.
        lastRenderTime =time.time_ns();
        #If we are able to get as high as this FPS, don't render again.        
        TARGET_TIME_BETWEEN_RENDERS = 1000000000 / self.DISPLAY_FRAMERATE;
        

        
        #Simple timer for finding TPS and FPS.
        lastSecondTime = int(lastUpdateTime / 1000000000);

        #Main Gane Loop =============================================================
        while(self.isRunning):  
            
            

           
            
            if (not self.isPaused):
                
                now = time.time_ns();
                if (now - lastUpdateTime > TIME_BETWEEN_UPDATES):                
                    #Call the main update method
                    self.__tick__();          
                    self.updateTickCount +=1;
                    lastUpdateTime = now; 
                    
                
                #float interpolation = Math.min(1.0f, (float) ((now - lastUpdateTime) / TIME_BETWEEN_UPDATES) );    

                ##Call the main render method
                #self.__render__();             
                
                now = time.time_ns();
                if (now - lastRenderTime > TARGET_TIME_BETWEEN_RENDERS):
                    #Call the main render method
                    self.__render__();             
                    self.displayFrameCount+=1;
                    lastRenderTime = now;                                
                
 
               
                #Update the frames we got.
                currentSecondTime = int(lastUpdateTime / 1000000000);
                if (currentSecondTime > lastSecondTime):              
                   self.updateAverageTPS = self.updateTickCount;
                   self.updateTickCount = 0;             
                    
                   self.displayAverageFPS = self.displayFrameCount;
                   self.displayFrameCount = 0;             
                   
                   #refresh timer  
                   lastSecondTime = currentSecondTime;

                """
                #Yield until it has been at least the target time between renders. This saves the CPU from hogging.
                while (now - lastRenderTime < TARGET_TIME_BETWEEN_RENDERS and now - lastUpdateTime < TIME_BETWEEN_UPDATES) :
                  #Thread.yield();   #deprecrated by below   
                  #This stops the app from consuming all the CPU. It makes this slightly less accurate, but is worth it.
                  #We can remove this line and it will still work (better), the CPU just climbs on certain OSes.
                  #FYI on some OS's this can cause pretty bad stuttering. 
                  time.sleep(0.01);
                  now = time.time_ns();
                """
            else: #if paused
                 now = time.time_ns();
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
    

