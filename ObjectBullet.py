#Import Built-in Modules
import math;

#Import Third Party Modules
import pygame as pyg;

#Import and initialize Project Modules ======================================
from GameObject import GameObject, GameObjectID;

class ObjectBullet(GameObject):
    
    def __init__(self, core, x, y, sizeX, sizeY, speed, targetObject):
        super().__init__(GameObjectID.PLAYER, core, x, y, sizeX, sizeY, speed);
        
        angleTarget = self.getDegrees(targetObject, 0, 0);
        xIntercept = math.cos(self.degreesToRadians(angleTarget));
        yIntercept = math.sin(self.degreesToRadians(angleTarget));                
        self.velX = xIntercept * self.speed;
        self.velY = yIntercept * self.speed;        
        
        self.damage = 10;
        
    def tick(self, deltaTime):                        
        self.applyOnlyVelocity(deltaTime);
        
        if( ((self.x+self.sizeX < 0) or (self.x > self.core.mainSurface.get_width()) ) 
            or 
            ((self.y+self.sizeY < 0) or (self.y > self.core.mainSurface.get_height()))
        ):
            self.core.removeFromObjectList(self);
            return;
        
        #if collides with enemy
        #damage enemy
        enemyCollide = self.getAnyCollision();
        if(enemyCollide != None and enemyCollide.id == GameObjectID.ENEMY):
            enemyCollide.getHurt(self.damage);
            self.core.removeFromObjectList(self);
            return;
        
    
    def render(self):
        pyg.draw.rect(self.core.mainSurface, pyg.Color(255,255,255), (self.x, self.y, self.sizeX, self.sizeY ), 2);
        pass;