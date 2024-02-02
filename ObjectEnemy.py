#Import Third Party Modules
import pygame as pyg;

#Import and initialize Project Modules ======================================
from GameObject import GameObject, GameObjectID;

class ObjectEnemy(GameObject):
    
    def __init__(self, core, x, y, sizeX, sizeY, speed):
        super().__init__(GameObjectID.ENEMY, core, x, y, sizeX, sizeY, speed);
        
    def tick(self, deltaTime):        
        #self.applyVelocity(deltaTime);
        pass;
    
    def render(self):
        pyg.draw.rect(self.core.mainSurface, pyg.Color(0,0,128), (self.x, self.y, self.sizeX, self.sizeY ), 2);