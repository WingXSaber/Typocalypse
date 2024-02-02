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
        self.state = "";       
        self.x = x;   
        self.y = y;   
        self.sizeX = sizeX;   
        self.sizeY = sizeY;     
        self.speed = speed;
        self.velX = 0;   
        self.velY = 0;   
    
    def tick(self, deltaTime):
        #self.applyVelocity(deltaTime);
        pass;
    
    def render(self):        
        pass;
    
    def applyVelocity(self, deltaTime):
        #Update x position =================
        if(self.velX !=0):
            #handler remove this
            self.x += self.velX * deltaTime;
            #if(self.isAnyCollision()):
            #self.x -= self.velX;
        
        #Update y position =================
        if(self.velY !=0):
            #handler remove this
            self.y += self.velY * deltaTime;
            #if(self.isAnyCollision()):
            #self.y -= self.velY;
    
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
                
                
    
    #def isAnyCollision
    
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