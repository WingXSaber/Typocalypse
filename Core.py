#Import Built-in Modules
import os;

#Import Third Party Modules
import pygame as pyg;
from pygame.locals import *;    #for keywords such as event 
from screeninfo import get_monitors;

#Import and initialize Project Modules ======================================
#from GameObject import GameObject, GameObjectID;



class Core():    
    
    #Initialize things needed by entire project =================================            
    def __init__(self):   
        #Initialize path of the system ==================================   ========
        self.dir_path = os.path.dirname(os.path.realpath(__file__));  
        
        #Initialize window and variables =============================================
        screenWidth = 1024;
        screenHeight = 768;
        DISPLAY_FLAGS = pyg.RESIZABLE | pyg.SHOWN 
        #Set window to center of screen
        monitors = get_monitors();  #Get current monitor and the resolution
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (monitors[0].width/2-screenWidth/2,(monitors[0].height/2-screenHeight/2));

        #Create Window and main display
        self.mainSurface = pyg.display.set_mode( (screenWidth, screenHeight), DISPLAY_FLAGS);
        self.mainSurface.fill(pyg.Color(128, 128, 128));    #fill background color 
        pyg.display.update();  
        #pyg.display.flip();  

        #Set Window Name
        pyg.display.set_caption("Typocalypse");

        #dir_path = os.path.dirname(os.path.realpath(__file__));  #Initialize path of the system
        #Set Icon of the Window
        #try:    
        #    pyg.display.set_icon(pyg.image.load(dir_path+"/Assets/logo.png"));
        #except:
        #    print("Icon not found at : "+dir_path+"/Assets/logo.png");
        #    pass;

        
        
        
        #Initialize fonts =======================================================
        pyg.font.init();
        self.fontDefault = pyg.font.SysFont('None',24);
        
        # Initilialize player input flags =======================================
        self.keyPressed_Up      = False;
        self.keyPressed_Down    = False;
        self.keyPressed_Left    = False;
        self.keyPressed_Right   = False;
        
        self.keyMovementsList = [pyg.K_UP, pyg.K_DOWN, pyg.K_LEFT, pyg.K_RIGHT, pyg.K_w,  pyg.K_s, pyg.K_a, pyg.K_d];
        
        # Define game object list
        self.gameObjectList = pyg.sprite.Group(); 


    def eventCheck(self, event):
        #if stateGame == game play
        
        
        if (event.type == pyg.KEYDOWN):
            #print(pyg.key.name(event.key) );
            if (event.key in self.keyMovementsList):                                         
                if (event.key == pyg.K_UP    or event.key == pyg.K_w): 
                    self.keyPressed_Up = True;
                if (event.key == pyg.K_DOWN  or event.key == pyg.K_s): 
                    self.keyPressed_Down = True;
                if (event.key == pyg.K_LEFT  or event.key == pyg.K_a): 
                    self.keyPressed_Left = True;
                if (event.key == pyg.K_RIGHT or event.key == pyg.K_d): 
                    self.keyPressed_Right = True;
        
        if (event.type == pyg.KEYUP):
            #print(pyg.key.name(event.key) );
            if (event.key in self.keyMovementsList): 
                if (event.key == pyg.K_UP    or event.key == pyg.K_w):
                    self.keyPressed_Up = False;
                if (event.key == pyg.K_DOWN  or event.key == pyg.K_s):
                    self.keyPressed_Down = False;
                if (event.key == pyg.K_LEFT  or event.key == pyg.K_a):
                    self.keyPressed_Left = False;
                if (event.key == pyg.K_RIGHT or event.key == pyg.K_d):
                    self.keyPressed_Right = False;
                
                    
    def addToObjectList(self, gameObject):
        self.gameObjectList.add(gameObject);
    
    #def 