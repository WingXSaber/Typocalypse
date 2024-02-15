#Import Built-in Modules
import math;

#Import Third Party Modules
import pygame as pyg;
from enum import Enum, auto;


class GameObject(pyg.sprite.Sprite):           #extends pygame's sprite
    """The base class, inherited by other gameObjects
    """
    
    def __init__(self, id, core, x, y, sizeX, sizeY, speed):
        # Call the parent class (Sprite) constructor
        super().__init__();    #pyg.sprite.Sprite.__init__(self)
        self.core = core;
        self.id = id; 
        self.state = None;       
        self.x = x;   
        self.y = y;   
        self.sizeX = sizeX;   
        self.sizeY = sizeY;     
        self.speed = speed;
        self.velX = 0;   
        self.velY = 0;   
        self.rect = pyg.Rect(x,y,sizeX,sizeY);
    
    def tick(self, deltaTime):
        #self.applyVelocity(deltaTime);
        pass;
    
    def render(self):        
        pass;
    
    
    def applyOnlyVelocity(self, deltaTime):
        #Update x position =================
        if(self.velX !=0):            
            self.x += self.velX * deltaTime;   
            self.rect.x = self.x;         
        
        #Update y position =================
        if(self.velY !=0):
            #handler remove this
            self.y += self.velY * deltaTime;
            self.rect.y = self.y;
            
    
    def applyVelocityWithCollision(self, deltaTime):
        #Update x position =================
        if(self.velX !=0):            
            self.x += self.velX * deltaTime;   
            self.rect.x = self.x;         
            
            self.core.gameObjectList.remove(self);#handler remove this            
            if(self.isAnyCollision()):
                self.x -= self.velX;
                self.rect.x = self.x;
            self.core.gameObjectList.add(self);
        
        #Update y position =================
        if(self.velY !=0):
            #handler remove this
            self.y += self.velY * deltaTime;
            self.rect.y = self.y;
            
            self.core.gameObjectList.remove(self);
            if(self.isAnyCollision()):
                self.y -= self.velY;
                self.rect.y = self.y;
            self.core.gameObjectList.add(self);
            
        
    
    def applyFrictionX(self):
        #reduce X velocity / apply friction
        if(abs(self.velX)>0):
            if(abs(self.velX)<1):  #if floating value but near zero
                self.velX = 0;
            else:
                #Reduce velocityX by adding one unit of it's inverse sign
                #example: velX = one unit, inverse sign
                #example: 5 = -1
                #example: -5 = 1
                self.velX+=-(self.velX/abs(self.velX));
    
    def applyFrictionY(self):
        #reduce Y velocity / apply friction
        if(abs(self.velY)>0):
            if(abs(self.velY)<1):  #if floating value but near zero
                self.velY = 0;
            else:
                #Reduce velocityY by adding one unit of it's inverse sign
                #example: velY = one unit, inverse sign
                #example: 5 = -1
                #example: -5 = 1
                self.velY+=-(self.velY/abs(self.velY));
    
    def getDistance(self, otherObject):      
        #get distance from another object using center point  
        distanceX = abs(abs(self.x+(self.sizeX/2)) - abs(otherObject.x+(otherObject.sizeX/2)));
        distanceY = abs(abs(self.y+(self.sizeY/2)) - abs(otherObject.y+(otherObject.sizeY/2)));
        return  distanceX + distanceY
    
    def getDegrees(self, targetObject, offsetX = 0, offsetY = 0):
        x1 = self.x+(self.sizeX/2);
        y1 = self.y+(self.sizeY/2);
        x2 = targetObject.x+(targetObject.sizeX/2) + offsetX;
        y2 = targetObject.y+(targetObject.sizeY/2) + offsetY;
        return self.radiansToDegrees(math.atan2(y2-y1,x2-x1)) ;    

    def degreesToRadians(self, value):
        return value * (math.pi / 180);
    
    def radiansToDegrees(self, value):
        return value * (180 / math.pi);
    
    def isAnyCollision(self):
        for obj in self.core.gameObjectList:
            if(obj != self and self.rect.colliderect(obj.rect)):
                return True;               
        return False;
    
    def getAnyCollision(self):
        for obj in self.core.gameObjectList:
            if(obj != self and self.rect.colliderect(obj.rect)):
                return obj;
        return None;
    
class GameObjectID(Enum):
    #An enum class for defining Gameobjects and accessed through its attributes. 
    PLAYER = auto();
    ENEMY = auto();
    BULLET = auto();
    LEVEL = auto();
    
    def __str__(self):
        """Function called if state is used as string such as in print()
        """
        return self.name;    