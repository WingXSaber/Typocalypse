#Import Built-in Modules
import os;

#Import Third Party Modules
import pygame as pyg;
from screeninfo import get_monitors;

class Window():

    def __init__(self, Typocalypse):
        
        #Initialize window and variables =============================================
        self.screenWidth = 1024;
        self.screenHeight = 768;
        self.DISPLAY_FLAGS = pyg.RESIZABLE | pyg.SHOWN;

        #Set window to center of screen
        monitors = get_monitors();  #Get current monitor and the resolution
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (monitors[0].width/2-self.screenWidth/2,(monitors[0].height/2-self.screenHeight/2));
              
        #Create Window and main display
        Typocalypse.mainSurface = pyg.display.set_mode((self.screenWidth, self.screenHeight), self.DISPLAY_FLAGS);
        Typocalypse.mainSurface.fill(pyg.Color(128, 128, 128));     
        pyg.display.update();  
        
        #Set Window Name
        pyg.display.set_caption("Typocalypse");
        
         #dir_path = os.path.dirname(os.path.realpath(__file__));  #Initialize path of the system
        #Set Icon of the Window
        #try:    
        #    pyg.display.set_icon(pyg.image.load(dir_path+"/Assets/logo.png"));
        #except:
        #    print("Icon not found at : "+dir_path+"/Assets/logo.png");
        #    pass;
        