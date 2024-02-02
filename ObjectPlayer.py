#Import Third Party Modules
import pygame as pyg;

#Import and initialize Project Modules ======================================
from GameObject import GameObject, GameObjectID;

class ObjectPlayer(GameObject):
    
    def __init__(self, core, x, y, sizeX, sizeY, speed):
        super().__init__(GameObjectID.PLAYER, core, x, y, sizeX, sizeY, speed);
        
    def tick(self, deltaTime):
        #Update Velocity X
        if((self.core.keyPressed_Left and self.core.keyPressed_Right) or (not self.core.keyPressed_Left and not self.core.keyPressed_Right)):        
            #If no input in x plane
            self.applyFrictionX();            
        elif(self.core.keyPressed_Left):
            if(self.velX>-self.speed): 
                #self.velX-=1; #add -velocity until matching -speed
                self.velX-=self.speed/4; #add -velocity until matching -speed                
        elif(self.core.keyPressed_Right):
            if(self.velX<self.speed):
                #self.velX+=1; #add velocity until matching speed
                self.velX+=self.speed/4; #add velocity until matching speed
                
        #Update Velocity Y
        if((self.core.keyPressed_Up and self.core.keyPressed_Down) or (not self.core.keyPressed_Up and not self.core.keyPressed_Down)):        
            #If no input in x plane
            self.applyFrictionY();            
        elif(self.core.keyPressed_Up):
            if(self.velY>-self.speed): 
                #self.velY-=1; #add -velocity until matching -speed
                self.velY-=self.speed/4; #add -velocity until matching -speed
        elif(self.core.keyPressed_Down):
            if(self.velY<self.speed):
                #self.velY+=1; #add velocity until matching speed
                self.velY+=self.speed/4; #add velocity until matching speed
        
        
        self.applyVelocity(deltaTime);
    
    def render(self):
        pyg.draw.rect(self.core.mainSurface, pyg.Color(255,128,0), (self.x, self.y, self.sizeX, self.sizeY ), 2);
        pass;