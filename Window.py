#Import Built-in Modules
import os;

#Import Third Party Modules
import pygame as pyg;
from screeninfo import get_monitors;

#Initialize window and variables =============================================
screenWidth = 1024;
screenHeight = 768;
DISPLAY_FLAGS = pyg.RESIZABLE | pyg.SHOWN;

#Set window to center of screen
monitors = get_monitors();  #Get current monitor and the resolution
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (monitors[0].width/2-screenWidth/2,(monitors[0].height/2-screenHeight/2));

#Set Window Name
pyg.display.set_caption("Typocalypse");

#dir_path = os.path.dirname(os.path.realpath(__file__));  #Initialize path of the system
#Set Icon of the Window
#try:    
#    pyg.display.set_icon(pyg.image.load(dir_path+"/Assets/logo.png"));
#except:
#    print("Icon not found at : "+dir_path+"/Assets/logo.png");
#    pass;