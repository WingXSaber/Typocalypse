#Import Third Party Modules
import pygame as pyg;

#Import and initialize Project Modules ======================================
from GameObject import GameObject, GameObjectID;
from ObjectBullet import ObjectBullet;

class ObjectPlayer(GameObject):
    
    def __init__(self, core, x, y, sizeX, sizeY, speed, health):
        super().__init__(GameObjectID.PLAYER, core, x, y, sizeX, sizeY, speed);
        self.health = health;
        
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
        
        
        self.applyVelocityWithCollision(deltaTime);
    
    def render(self):
        pyg.draw.rect(self.core.mainSurface, pyg.Color(20,20,255), (self.x, self.y, self.sizeX, self.sizeY ), 0);
        pass;
    
    def getHurt(self, damage):
        #add invulnuerablity time
        if(self.health > 0):
            self.health -= damage;
        if(self.health < 0):
            self.health = 0;
            
    def attack(self, enemyName):
        #Change state to shooting
        print("Shooting Enemy: "+enemyName);
        bulletSize = 5;
        bulletSpeed = 10;
        
        for obj in self.core.gameObjectList:
            if(obj.id == GameObjectID.ENEMY and obj.name == enemyName):
                self.core.addToObjectList(ObjectBullet(self.core, 
                                                  self.x + (self.sizeX/2) - (bulletSize/2), 
                                                  self.y + (self.sizeY/2) + (bulletSize/2),
                                                  bulletSize, bulletSize, bulletSpeed, obj));
        #Return state
        pass;