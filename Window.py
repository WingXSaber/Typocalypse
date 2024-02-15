#Import Built-in Modules
import os;

#Import Third Party Modules
import pygame as pyg;
from screeninfo import get_monitors;

class Window():

    def __init__(self, Core):        
        #Set window to center of screen
        self.DISPLAY_FLAGS = pyg.RESIZABLE | pyg.SHOWN ;
        monitors = get_monitors();  #Get current monitor and the resolution
        
        #Initialize window and variables =============================================
        #screenWidth = 1024;
        #screenHeight = 768;
        #os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (monitors[0].width/2-screenWidth/2,(monitors[0].height/2-screenHeight/2));
        screenWidth = monitors[0].width;
        screenHeight = monitors[0].height;
              
        #Create Window and main display
        Core.mainSurface = pyg.display.set_mode( (screenWidth, screenHeight), self.DISPLAY_FLAGS);
        Core.mainSurface.fill(pyg.Color(128, 128, 128));     
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
        