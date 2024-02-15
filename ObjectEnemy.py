#Import Built-in Modules
import math;
import random;
import time;

#Import Third Party Modules
import pygame as pyg;

#Import and initialize Project Modules ======================================
from GameObject import GameObject, GameObjectID;
from StateMachine import State, generate_transition_table, TransitionTableToString;

class ObjectEnemy(GameObject):
    
    def __init__(self, core, x, y, sizeX, sizeY, speed, health, name):
        super().__init__(GameObjectID.ENEMY, core, x, y, sizeX, sizeY, speed);
        self.name = name;
        self.health = health;
        self.state = self.intializeEnemyStateMachine();        
        self.transitionTable = generate_transition_table(self.state);        
        #print();
        #print(TransitionTableToString(self.transitionTable));
        
        self.attackRange = (sizeX+sizeY);    
        self.attackDamage = 10;
        self.attackStartTimer = 0;            
        self.attackDuration = 0.8;
        
        self.hurtTimer = 0;
        self.hurtDuration = 0.5;
        
        
    def intializeEnemyStateMachine(self):
        q0 = State("q0","Idle");
        q1 = State("q1","Walking");
        q2 = State("q2","Attacking");
        q3 = State("q3","Hurt");
        q4 = State("q4","Defeated");
        q5 = State("q5","Stop");

        #Connect 
        q0.connect(q1, "Player is alive and not within reach");
        q0.connect(q2, "Player is alive and within reach");
        q0.connect(q3, "Get shot by Player");
        q0.connect(q5, "Player has no more health left");

        q1.connect(q0, "Player takes aim");
        q1.connect(q2, "Player is within reach");
        q1.connect(q3, "Get shot by Player");
        q1.connect(q5, "Player has no more health left");        
        
        q2.connect(q0, "this Enemy has finished with hurting");
        
        q3.connect(q0, "this Enemy has finished with hurting");        
        q3.connect(q4, "this Enemy has no more health left");        
        
        return q0; #head node
    
            
    def tick(self, deltaTime):       
        #Update State:        
        #q3 = State("q3","Hurt");
        #q4 = State("q4","Defeated");
        #q5 = State("q5","Stop");
        match (self.state.name):
            case "q0": #Idle           
                self.velX = 0;
                self.velY = 0;                
                # "Player is alive and not within reach"
                if(self.core.player.health <= 0 ):
                    self.state = self.state.getNext("q5");       
                    self.core.isGameOver = True;
                else:
                    if(self.getDistance(self.core.player) >= self.attackRange):                    
                        self.state = self.state.getNext("q1");   
                    else:
                        self.state = self.state.getNext("q2");  
                        self.attackStartTimer = time.time() + self.attackDuration;                         
                        self.core.player.health -= self.attackDamage;
                        
            case "q1": #Walking                           
                if(self.core.player.health <= 0 ):
                    self.state = self.state.getNext("q5");
                    self.core.isGameOver = True;
                    
                angleTarget = self.getDegrees(self.core.player, random.randint(-10, 10), random.randint(-10, 10));
                xIntercept = math.cos(self.degreesToRadians(angleTarget));
                yIntercept = math.sin(self.degreesToRadians(angleTarget));
                
                self.velX = xIntercept * self.speed;
                self.velY = yIntercept * self.speed;
                
                if( self.core.player.health > 0 and self.getDistance(self.core.player) < self.attackRange):                    
                    self.state = self.state.getNext("q2");
                    self.attackStartTimer = time.time() + self.attackDuration;
                    self.core.player.health -= self.attackDamage;
                    
            case "q2": #Attacking
                if(self.velX != 0):
                    self.applyFrictionX();
                if(self.velY != 0):
                    self.applyFrictionY();
                    
                #else: #if(self.core.player.health > 0 ):
                    #self.core.player.health -= 1;
                
                #if( self.core.player.health > 0 and self.getDistance(self.core.player) >= self.attackRange):
                #    self.state = self.state.getNext("q0");
                if(self.attackStartTimer <= time.time()):
                    self.attackStartTimer = 0;
                    self.state = self.state.getNext("q0");
            
            case "q3": #Hurt        
                if(self.velX != 0):
                    self.applyFrictionX();
                if(self.velY != 0):
                    self.applyFrictionY(); 
                
                if(self.health <=0):
                    self.hurtTimer = 0;
                    self.state = self.state.getNext("q4");    
                    self.core.isGameWin = True;
                    for obj in self.core.gameObjectList:                        
                        if(self.core.isGameWin == True and obj.id == GameObjectID.ENEMY):
                            if(obj.state.name != "q4"):
                                self.core.isGameWin = False;
                elif(self.hurtTimer <= time.time()):
                    self.hurtTimer = 0;
                    self.state = self.state.getNext("q0");
                
                    
            case "q4": #Defeated
                if(self.velX != 0):
                    self.applyFrictionX();
                if(self.velY != 0):
                    self.applyFrictionY();      
                    
            case "q5": #Stop / Player Win
                if(self.velX != 0):
                    self.applyFrictionX();
                if(self.velY != 0):
                    self.applyFrictionY();
                
                    
        self.applyVelocityWithCollision(deltaTime);
        
        pass;
    
    def render(self):
        if(self.state.name == "q4"):
            pyg.draw.rect(self.core.mainSurface, pyg.Color(55,80,55), (self.x, self.y, self.sizeX, self.sizeY ), 0);             
        else:
            pyg.draw.rect(self.core.mainSurface, pyg.Color(0,120,0), (self.x, self.y, self.sizeX, self.sizeY ), 0);
        
    def renderUI(self):
        if(self.state.name == "q4"):
            textSurface = self.core.fontDefault.render(str(self.name), True, (160,160,160));
            self.core.mainSurface.blit(textSurface, (self.x+int(self.sizeX/2)-int(textSurface.get_width()/2), self.y-textSurface.get_height()));            
        else:
            textSurface = self.core.fontDefault.render(str(self.name), True, (255,255,255));
            self.core.mainSurface.blit(textSurface, (self.x+int(self.sizeX/2)-int(textSurface.get_width()/2), self.y-textSurface.get_height()));            
        #self.core.mainSurface.blit(self.core.fontDefault.render("State:"+str(self.state.name), True, (255,255,255)), (self.x+10, self.y+5));            
        #self.core.mainSurface.blit(self.core.fontDefault.render("Health:"+str(self.health), True, (255,255,255)), (self.x+10, self.y+20));            
        
    def getHurt(self, damage):
        if(self.health > 0):
            self.health -= damage;
            self.hurtTimer = time.time() + self.hurtDuration;
            self.state = self.state.getNext("q3");
        if(self.health < 0):
            self.health = 0;
       