#Import Built-in Modules
import os;
import time;

#Import Third Party Modules
import pygame as pyg;
from pygame.locals import *;    #for keywords such as event 
#from screeninfo import get_monitors;

#Import and initialize Project Modules ======================================
from GameObject import GameObject, GameObjectID;
from ObjectPlayer import ObjectPlayer;
from ObjectEnemy import ObjectEnemy;
from Window import Window;
from StateMachine import State, generate_transition_table, TransitionTableToString;


class Core():    
    
    #Initialize things needed by entire project =================================            
    def __init__(self):        
        #Initialize path of the system ==================================   ========
        self.dir_path = os.path.dirname(os.path.realpath(__file__));  
               
        #Initialize fonts =======================================================
        #print(pyg.font.get_fonts())   
        pyg.font.init();
        self.fontDefault = pyg.font.SysFont('freesans',16);
        self.fontLarge = pyg.font.SysFont('freesans',160);
        #self.fontDefault = pyg.font.SysFont('None',22);
        
        # Initilialize player input flags =======================================
        self.keyPressed_Up      = False;
        self.keyPressed_Down    = False;
        self.keyPressed_Left    = False;
        self.keyPressed_Right   = False;
        
        self.keyMovementsList = [pyg.K_UP, pyg.K_DOWN, pyg.K_LEFT, pyg.K_RIGHT, pyg.K_w,  pyg.K_s, pyg.K_a, pyg.K_d];
        
        # Define game object list
        self.gameObjectList = pyg.sprite.Group();         
        
        # Define player refenence
        self.player = None;
               
        # Boolean flag to check if player is aiming        
        self.isPlayerAiming = False;        
        
        # Aim State Machine
        self.aimingState = None;  
        
        # Player Shooting Timer
        self.shootingDelayTimer = 0;
        self.shootingDelayDuration = 2;
        
        # Player pressed Key
        self.keyPressed = "";
        
        self.isGameOver = False;
        self.isGameWin = False;
        
        
    #def intializeGameStateMachine(self): 
        
    def intializeAimStateMachine(self):    
        q00 = State("q00","Ready");
        q01 = State("q01","A");
        q02 = State("q02","AL");
        q03 = State("q03","ALT");
        
        q04 = State("q04","B");
        q05 = State("q05","BO");
        q06 = State("q06","BOA");
        q07 = State("q07","BOAR");
        q08 = State("q08","BOAT");
        
        q09 = State("q09","C");
        q10 = State("q10","CO");
        q11 = State("q11","COR");
        q12 = State("q12","CORE");
        q13 = State("q13","CORK");
        q14 = State("q14","CORN");        
        
        #Connect  
        q00.connect(q01, "Press 'A'");
        q00.connect(q04, "Press 'B'");
        q00.connect(q09, "Press 'C'");
        
        q01.connect(q02, "Press 'L'");
        q01.connect(q00, "Press an invalid key");                
        q02.connect(q03, "Press 'T'");
        q02.connect(q00, "Press an invalid key");
                
        q04.connect(q05, "Press 'O'");        
        q04.connect(q00, "Press an invalid key");        
        q05.connect(q06, "Press 'A'");
        q05.connect(q00, "Press an invalid key");
                        
        q06.connect(q07, "Press 'R'");
        q06.connect(q08, "Press 'T'");
        q06.connect(q00, "Press an invalid key");
        
        q09.connect(q10, "Press 'O'");
        q09.connect(q00, "Press an invalid key");
        q10.connect(q11, "Press 'R'");
        q10.connect(q00, "Press an invalid key");
        q11.connect(q12, "Press 'E'");
        q11.connect(q13, "Press 'K'");
        q11.connect(q14, "Press 'N'");
        q11.connect(q00, "Press an invalid key");
        
        #final states
        #q2, q5, q6, q8, q9 q10
        
        return q00

    def eventCheck(self, event):
        
        #if stateGame == game play    
        
        #print(pyg.key.name(event.key) );
        if (event.type == pyg.KEYDOWN):
            if(event.key == pyg.K_RETURN):
                if(self.isPlayerAiming == False):
                    #Player enters into aiming mode
                    self.isPlayerAiming = True;                
                    self.aimingState = self.intializeAimStateMachine();  
                    self.shootingDelayTimer = 0;
                    #transitionTable = generate_transition_table(self.aimingState);        
                    #print(TransitionTableToString(transitionTable));
                    #refresh movement inputs
                    self.keyPressed_Up      = False;
                    self.keyPressed_Down    = False;
                    self.keyPressed_Left    = False;
                    self.keyPressed_Right   = False;      

                else:
                    self.isPlayerAiming = False;                
                    self.aimingState = None;                  
        
            if(self.isPlayerAiming == False):
                if (event.key in self.keyMovementsList):                                         
                    if (event.key == pyg.K_UP    or event.key == pyg.K_w): 
                        self.keyPressed_Up = True;
                    if (event.key == pyg.K_DOWN  or event.key == pyg.K_s): 
                        self.keyPressed_Down = True;
                    if (event.key == pyg.K_LEFT  or event.key == pyg.K_a): 
                        self.keyPressed_Left = True;
                    if (event.key == pyg.K_RIGHT or event.key == pyg.K_d): 
                        self.keyPressed_Right = True; 
            else:#Player is aiming
                self.keyPressed = pyg.key.name(event.key).upper(); 
                #print("INPUT: "+keyPressed+" CURRENT AIM STATE: "+str(self.aimingState));
                match (self.aimingState.name):
                    case "q00": #Idle 
                        match (self.keyPressed):
                            case "A":
                                self.aimingState = self.aimingState.getNext("q01");
                            case "B":
                                self.aimingState = self.aimingState.getNext("q04");
                            case "C":
                                self.aimingState = self.aimingState.getNext("q09");
                            #case _ : #Invalid input
                            #    self.aimingState = self.aimingState.getNext("q00");
                    case "q01": #"A"
                        match (self.keyPressed):
                            case "L":
                                self.aimingState = self.aimingState.getNext("q02");
                            case _ : #Invalid input
                                self.aimingState = self.aimingState.getNext("q00");
                    case "q02": #"AL"
                        match (self.keyPressed):
                            case "T":
                                self.aimingState = self.aimingState.getNext("q03");
                            case _ : #Invalid input
                                self.aimingState = self.aimingState.getNext("q00");  
                    case "q04": #"B"
                        match (self.keyPressed):
                            case "O":
                                self.aimingState = self.aimingState.getNext("q05");
                            case _ : #Invalid input
                                self.aimingState = self.aimingState.getNext("q00");
                    case "q05": #"BO"
                        match (self.keyPressed):
                            case "A":
                                self.aimingState = self.aimingState.getNext("q06");
                            case _ : #Invalid input
                                self.aimingState = self.aimingState.getNext("q00");
                    case "q06": #"BOA"
                        match (self.keyPressed):
                            case "R":
                                self.aimingState = self.aimingState.getNext("q07");
                            case "T":
                                self.aimingState = self.aimingState.getNext("q08");
                            case _ : #Invalid input
                                self.aimingState = self.aimingState.getNext("q00");
                    case "q09": #"C"
                        match (self.keyPressed):
                            case "O":
                                self.aimingState = self.aimingState.getNext("q10");
                            case _: #Invalid input
                                self.aimingState = self.aimingState.getNext("q00");
                    case "q10": #"CO"
                        match (self.keyPressed):
                            case "R":
                                self.aimingState = self.aimingState.getNext("q11");
                            case _: #Invalid input
                                self.aimingState = self.aimingState.getNext("q00");
                    case "q11": #"COR"
                        match (self.keyPressed):
                            case "E":
                                self.aimingState = self.aimingState.getNext("q12");
                            case "K":
                                self.aimingState = self.aimingState.getNext("q13");
                            case "N":
                                self.aimingState = self.aimingState.getNext("q14");
                            case _: #Invalid input
                                self.aimingState = self.aimingState.getNext("q00"); 
                
                match(self.aimingState.name):
                    case "q03": #"ALT"
                        self.player.attack("ALT");
                        self.isPlayerAiming = False;
                        self.shootingDelayTimer = time.time() + self.shootingDelayDuration;
                    case "q07": #"BOAR"
                        self.player.attack("BOAR");
                        self.isPlayerAiming = False;
                        self.shootingDelayTimer = time.time() + self.shootingDelayDuration;
                    case "q08": #"BOAT"
                        self.player.attack("BOAT");
                        self.isPlayerAiming = False;
                        self.shootingDelayTimer = time.time() + self.shootingDelayDuration;
                    case "q12": #"CORE"            
                        self.player.attack("CORE");
                        self.isPlayerAiming = False;
                        self.shootingDelayTimer = time.time() + self.shootingDelayDuration;
                    case "q13": #"CORK"            
                        self.player.attack("CORK");
                        self.isPlayerAiming = False;
                        self.shootingDelayTimer = time.time() + self.shootingDelayDuration;
                    case "q14": #"CORN"            
                        self.player.attack("CORN");
                        self.isPlayerAiming = False;
                        self.shootingDelayTimer = time.time() + self.shootingDelayDuration;
               # print("   NEW AIM STATE: "+str(self.aimingState));
               
        if (event.type == pyg.KEYUP):            
            if(self.isPlayerAiming == False):
                if (event.key in self.keyMovementsList): 
                    if (event.key == pyg.K_UP    or event.key == pyg.K_w):
                        self.keyPressed_Up = False;
                    if (event.key == pyg.K_DOWN  or event.key == pyg.K_s):
                        self.keyPressed_Down = False;
                    if (event.key == pyg.K_LEFT  or event.key == pyg.K_a):
                        self.keyPressed_Left = False;
                    if (event.key == pyg.K_RIGHT or event.key == pyg.K_d):
                        self.keyPressed_Right = False;        
                
        #if stateGame == Menu
        #if stateGame == HighScore

                    
    def addToObjectList(self, gameObject):
        self.gameObjectList.add(gameObject);
    
    def removeFromObjectList(self, gameObject):
        self.gameObjectList.remove(gameObject);
        
    def clearObjectList(self):
        self.gameObjectList.empty();
    
    
    def initGame(self):
        self.clearObjectList();
        self.isGameOver = False;
        self.isGameWin = False;
        
        size = 35;
        self.playerMaxHealth = 100;
        self.player = ObjectPlayer(self, 500, 500, size, size, 5, self.playerMaxHealth);          
        
        enemy1 = ObjectEnemy (self, 1000, 250, size, size, 4, 10, "ALT");  
        enemy2 = ObjectEnemy (self, 500, 250, size, size, 4, 10, "BOAR");  
        enemy3 = ObjectEnemy (self, 750, 250, size, size, 4, 10, "BOAT");  
        enemy4 = ObjectEnemy (self, 250, 100, size, size, 4, 10, "CORE");  
        enemy5 = ObjectEnemy (self, 500, 100, size, size, 4, 10, "CORK");  
        enemy6 = ObjectEnemy (self, 750, 100, size, size, 4, 10, "CORN");
        
        self.addToObjectList(self.player);
        self.addToObjectList(enemy1);
        self.addToObjectList(enemy2);
        self.addToObjectList(enemy3);
        self.addToObjectList(enemy4);
        self.addToObjectList(enemy5);
        self.addToObjectList(enemy6);
        
        
        #add this MainGameScene    
        self.image_AIM_FSM_q00 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q00.png");
        self.image_AIM_FSM_q01 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q01.png");
        self.image_AIM_FSM_q02 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q02.png");
        self.image_AIM_FSM_q03 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q03.png");
        self.image_AIM_FSM_q04 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q04.png");
        self.image_AIM_FSM_q05 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q05.png");
        self.image_AIM_FSM_q06 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q06.png");
        self.image_AIM_FSM_q07 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q07.png");
        self.image_AIM_FSM_q08 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q08.png");
        self.image_AIM_FSM_q09 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q09.png");
        self.image_AIM_FSM_q10 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q10.png");
        self.image_AIM_FSM_q11 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q11.png");
        self.image_AIM_FSM_q12 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q12.png");
        self.image_AIM_FSM_q13 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q13.png");
        self.image_AIM_FSM_q14 = pyg.image.load(self.dir_path+"/AIM-FSM/AIM-FSM-q14.png");        
        self.image_AIM_FSM = self.image_AIM_FSM_q00;