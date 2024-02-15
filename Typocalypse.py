#Import Built-in Modules
import sys;
import os;
import time as time;

#Import Third Party Modules
import pygame as pyg;
from pygame.locals import *;    #for keywords such as event 

#Import and initialize Project Modules ======================================
from Core import Core;
from GameObject import GameObject, GameObjectID;
from ObjectPlayer import ObjectPlayer;
from ObjectEnemy import ObjectEnemy;
from Window import Window;
from StateMachine import State, generate_transition_table, TransitionTableToString;


class Typocalpyse():
    
    def __init__(self):        
        #Initialize path of the system ==================================   ========
        #self.dir_path = os.path.dirname(os.path.realpath(__file__));  
        
        #Initialze Pygame  =========================================================
        pyg.init();                          
        self.pygClock = pyg.time.Clock();    #Initialze Pygame's clock
        #Initialize game loop variables ============================================
        self.UPDATE_TICKRATE = 30;     #target logic rate
        self.DISPLAY_FRAMERATE = 60;    #target display FPS
        
        self.updateTickCount = 0; #count current ticks have displayed
        self.updateAverageTPS = 0; #count average ticks have displayed per second

        self.displayFrameCount = 0; #count current frames have displayed
        self.displayAverageFPS = 0; #count average frames have displayed per second

        self.isRunning = True;  #Flag for whole application if running                           
        self.isPaused = False;  #Flag for application if paused (like minimized)
        
        self.isDebugMode = True;    #flag for showing debug details or not
        self.isEnemyDebugMode = False;
        self.isAimDebugMode = False;

        #Initialize modules of Typocalypse =========================================
        self.core = Core(); #initialized first, it contains variables shared by other modules        
        
        self.window = Window(self.core);
        self.core.initGame();
        
        #q0 = State("q0", "Main Menu");
        #q1 = State("q0", "Loading Assets");
        #q1 = State("q0", "Game Running");
        #q1 = State("q0", "Options Menu");
        #q1 = State("q0", "HighScore Menu");
        #q1 = State("q0", "System Exit");
        #self.gameStates = "";
        self.aimTransitionTable =  TransitionTableToString(generate_transition_table(self.core.intializeAimStateMachine()));                  
        self.enemyTransitionTable =  TransitionTableToString(generate_transition_table(ObjectEnemy(self.core,0,0,0,0,0,0,"").intializeEnemyStateMachine()));        
        
        
        self.__run__();
    


    def __tick__(self, deltaTime):      
        
        #Getting the current event list available and execute action        
        for event in pyg.event.get():            
            # Events ======================================================== 
            #if event.type == pyg.VIDEORESIZE:     #when window is resized
            #    #Update Camera
            #    #camera["x"] -= (event.size[0]-SCREEN_WIDTH)/2;
            #    #camera["y"] -= (event.size[1]-SCREEN_HEIGHT)/2;
            #    #Update current window size
            #    self.window.screenWidth = event.size[0];
            #    self.window.screenHeight = event.size[1];         
            if (event.type== pyg.locals.QUIT): #when exit buttton event is pressed   
                self.isRunning = False;     
                
            # Inputs ========================================================  
            self.core.eventCheck(event); 
            #should be changed to
            # if gamestate = Menu
            #   #call menu class EventCheck(event)
            # elif gamestate = Game
            #   #call game class event check(event)
            # elif gamestate = highscoremenu
            #   #call Highscore class event check (event)
            # or use swtich case
            if (event.type == pyg.KEYDOWN):
                if(event.key == pyg.K_F3): #Show Enemy States
                    self.isEnemyDebugMode = not self.isEnemyDebugMode;   
                    self.isAimDebugMode   = False;
                if(event.key == pyg.K_F4): #Show Aim States
                    self.isEnemyDebugMode = False; 
                    self.isAimDebugMode   = not self.isAimDebugMode ;
                if(event.key == pyg.K_F5):
                    self.core.initGame();
                
            
        ##Update Objects =====================================================    
        # if gamestate = Menu
        #   #call menu class tick(deltaTime)
        # elif gamestate = Game
        #   #call game class tick(deltaTime)
        for obj in self.core.gameObjectList:
            obj.tick(deltaTime);     
        # elif gamestate = highscoremenu
        #   #call Highscore class tick(deltaTime)
        # or use swtich case
        
       
        
        #Update UI ==========================================================    
        pass;
    
    def __render__(self):
        self.core.mainSurface.fill(pyg.Color(128, 128, 128)); #(re)fill screen with background color    
        
        # if gamestate = Menu
        #   #call menu class render()
        
        # elif gamestate = Game
        #   #call game class render()
        
        # elif gamestate = highscoremenu        
        
        
        ui_Y = 20;
        #self.core.playerHealthTextSurface = self.core.fontDefault.render("Player Heath:"+str(self.core.player.health), True, (255,255,255));
        playerHealthTextSurface = self.core.fontDefault.render("Player Heath:", True, (255,255,255));
        self.core.mainSurface.blit(playerHealthTextSurface, (10, ui_Y));        
        healthBarSize = 250;           
        pyg.draw.rect(self.core.mainSurface, pyg.Color(0,0,0),   (10+playerHealthTextSurface.get_width()+5, ui_Y-int((playerHealthTextSurface.get_height()+10)/4), healthBarSize, playerHealthTextSurface.get_height()+10), 0);        
        offset = 2;
        pyg.draw.rect(self.core.mainSurface, pyg.Color(255,0,0), (10+playerHealthTextSurface.get_width()+5+offset, ui_Y-int((playerHealthTextSurface.get_height()+10)/4)+offset, (self.core.player.health/self.core.playerMaxHealth*healthBarSize)-offset*2, playerHealthTextSurface.get_height()+10-offset*2), 0);                
        ui_Y += 30                
        self.core.mainSurface.blit(self.core.fontDefault.render("Press [Enter] to Aim!", True, (255,255,255)), (10, ui_Y));            
        ui_Y += 20                
        self.core.mainSurface.blit(self.core.fontDefault.render("While Aiming, press the corresponding keys to shoot!", True, (255,255,255)), (10, ui_Y));            
        ui_Y += 20                
        
        
        
        
        if(self.isDebugMode):
            ui_Y = self.core.mainSurface.get_height() - 20;
            ui_X = 10;
            #self.mainSurface.blit(self.font.render("dt:"+str(deltaTime), True, (0,0,0)), (10, 10));        
            self.core.mainSurface.blit(self.core.fontDefault.render("TPS:"+str(round(self.updateAverageTPS)),          True, (255,255,255)), (ui_X, ui_Y));            
            ui_X += 69
            self.core.mainSurface.blit(self.core.fontDefault.render("FPS:"+str(round(self.displayAverageFPS)),         True, (255,255,255)), (ui_X, ui_Y));            
            ui_X += 69
            self.core.mainSurface.blit(self.core.fontDefault.render("width:"+ str(self.core.mainSurface.get_width()),  True, (255,255,255)), (ui_X, ui_Y));            
            ui_X += 100
            self.core.mainSurface.blit(self.core.fontDefault.render("height:"+str(self.core.mainSurface.get_height()), True, (255,255,255)), (ui_X, ui_Y));            
            ui_X += 100
            self.core.mainSurface.blit(self.core.fontDefault.render("[F3] Show Enemy States: ("+str(self.isEnemyDebugMode)+")", True, (255,255,255)), (ui_X, ui_Y));            
            ui_X += 250
            self.core.mainSurface.blit(self.core.fontDefault.render("[F4] Show Aim States: ("+str(self.isAimDebugMode)+")", True, (255,255,255)), (ui_X, ui_Y));            
        
        
        for obj in self.core.gameObjectList:
            obj.render();
            
            
        for obj in self.core.gameObjectList:
            if(obj.id == GameObjectID.ENEMY):
                obj.renderUI();
                
                
        
        if(self.core.aimingState != None):
            match(self.core.aimingState.name):
                case "q01":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q01;
                case "q02":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q02;
                case "q03":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q03;     
                    if(self.core.shootingDelayTimer <= time.time()):      
                        self.core.shootingDelayTimer = 0;         
                        self.core.aimingState = None;  
                case "q04":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q04;
                case "q05":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q05;
                case "q06":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q06;
                case "q07":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q07;
                    if(self.core.shootingDelayTimer <= time.time()):               
                        self.core.shootingDelayTimer = 0;
                        self.core.aimingState = None;  
                case "q08":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q08;
                    if(self.core.shootingDelayTimer <= time.time()): 
                        self.core.shootingDelayTimer = 0;              
                        self.core.aimingState = None;  
                case "q09":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q09;
                case "q10":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q10;
                case "q11":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q11;
                case "q12":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q12;
                    if(self.core.shootingDelayTimer <= time.time()):    
                        self.core.shootingDelayTimer = 0;           
                        self.core.aimingState = None;  
                case "q13":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q13;                    
                    if(self.core.shootingDelayTimer <= time.time()):      
                        self.core.shootingDelayTimer = 0;         
                        self.core.aimingState = None;  
                case "q14":
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q14;
                    if(self.core.shootingDelayTimer <= time.time()):   
                        self.core.shootingDelayTimer = 0;            
                        self.core.aimingState = None;  
                case _:
                    self.core.image_AIM_FSM = self.core.image_AIM_FSM_q00;
            if(self.core.image_AIM_FSM.get_height() != self.core.mainSurface.get_height()):
                imageNewWidth = int(self.core.image_AIM_FSM.get_width() / self.core.image_AIM_FSM.get_height() * self.core.mainSurface.get_height());
                self.core.mainSurface.blit(pyg.transform.smoothscale(self.core.image_AIM_FSM, (imageNewWidth, self.core.mainSurface.get_height())), (self.core.mainSurface.get_width()-imageNewWidth-10, 0) );            
                self.core.mainSurface.blit(self.core.fontDefault.render("Key Pressed: "+self.core.keyPressed, True, (255,255,255)), (self.core.mainSurface.get_width()-imageNewWidth-100, 10));            
        
            else:
                self.core.mainSurface.blit(self.core.image_AIM_FSM, (self.core.mainSurface.get_width()-self.core.image_AIM_FSM.get_width()-10, 0) );
                self.core.mainSurface.blit(self.core.fontDefault.render("Key Pressed: "+self.core.keyPressed, True, (255,255,255)), (self.core.mainSurface.get_width()-self.core.image_AIM_FSM.get_width()-100, 10));            
            
            if(self.isAimDebugMode):
                ui_Y = self.core.mainSurface.get_height() - (len(self.aimTransitionTable)+1)*20;            
                for line in self.aimTransitionTable:
                    tempX = 10
                    self.core.mainSurface.blit(self.core.fontDefault.render(line[0], True, (255,255,255)), (tempX, ui_Y));            
                    tempX +=60;
                    self.core.mainSurface.blit(self.core.fontDefault.render(line[1], True, (255,255,255)), (tempX, ui_Y));            
                    tempX +=60;
                    self.core.mainSurface.blit(self.core.fontDefault.render(line[2], True, (255,255,255)), (tempX, ui_Y));            
                    tempX +=180;
                    self.core.mainSurface.blit(self.core.fontDefault.render(line[3], True, (255,255,255)), (tempX, ui_Y));                            
                    ui_Y+=20;
        
        
        if(self.isEnemyDebugMode):
            ui_Y = 100                
            self.core.mainSurface.blit(self.core.fontDefault.render("Enemy List:", True, (255,255,255)), (10, ui_Y));            
            ui_Y += 20                
            for obj in self.core.gameObjectList:
                if(obj.id == GameObjectID.ENEMY):
                    self.core.mainSurface.blit(self.core.fontDefault.render("Name: \""+obj.name+"\"", True, (255,255,255)), (10, ui_Y));            
                    ui_Y += 20                    
                    #self.core.mainSurface.blit(self.core.fontDefault.render("Health: "+str(obj.health)+" State: "+obj.state.name, True, (255,255,255)), (10, ui_Y));            
                    self.core.mainSurface.blit(self.core.fontDefault.render("     Health: "+str(obj.health), True, (255,255,255)), (10, ui_Y));            
                    
                    self.core.mainSurface.blit(self.core.fontDefault.render("State: "+obj.state.name, True, (255,255,255)), (120, ui_Y));            
                    ui_Y += 30
            
            ui_Y = self.core.mainSurface.get_height() - (len(self.enemyTransitionTable)+1)*20;            
            for line in self.enemyTransitionTable:
                tempX = 10
                self.core.mainSurface.blit(self.core.fontDefault.render(line[0], True, (255,255,255)), (tempX, ui_Y));            
                tempX +=60;
                self.core.mainSurface.blit(self.core.fontDefault.render(line[1], True, (255,255,255)), (tempX, ui_Y));            
                tempX +=80;
                self.core.mainSurface.blit(self.core.fontDefault.render(line[2], True, (255,255,255)), (tempX, ui_Y));            
                tempX +=280;
                self.core.mainSurface.blit(self.core.fontDefault.render(line[3], True, (255,255,255)), (tempX, ui_Y));                            
                ui_Y+=20;
        
        
        if(self.core.isGameOver or self.core.isGameWin):
            gameEndSurface = pyg.Surface((self.core.mainSurface.get_width(), self.core.mainSurface.get_height()/3));
            gameEndSurface.set_alpha(125);
            gameEndSurface.fill((0,0,0));
            self.core.mainSurface.blit(gameEndSurface, (0, self.core.mainSurface.get_height()/3 ));             
            
            textImage = "";
            if(self.core.isGameOver):
                textImage = self.core.fontLarge.render("YOU LOSE", True, (255,0,0));
                self.core.mainSurface.blit(textImage, (self.core.mainSurface.get_width()/2-textImage.get_width()/2, self.core.mainSurface.get_height()/2-textImage.get_height()/2));                            
            elif(self.core.isGameWin):                
                textImage = self.core.fontLarge.render("YOU WIN", True,  (0,255,0));                
                self.core.mainSurface.blit(textImage, (self.core.mainSurface.get_width()/2-textImage.get_width()/2, self.core.mainSurface.get_height()/2-textImage.get_height()/2));            
            textImage2 = self.core.fontDefault.render("Press [F5] to restart game", True,  (255,255,255));                
            self.core.mainSurface.blit(textImage2, (self.core.mainSurface.get_width()/2-textImage2.get_width()/2, self.core.mainSurface.get_height()/2-textImage2.get_height()/2+textImage.get_height()/2));            
            
            
        #   #call Highscore class render()
        # or use swtich case
        
        
        pyg.display.update();  #refresh the display and render 
        
    
    def __stop__(self):        
        print("See You Space Cowboy.");
        pyg.quit();          #Quit Pygame
        sys.exit()           #Quit entire program   
    
    def __run__(self):
        #Jeric's Game Loop

        #Calculate how many ns each frame should take for our target update framerate.
        TIME_BETWEEN_UPDATES = 1000000000 / self.UPDATE_TICKRATE;                        
        #Think of MAX_UPDATES_BEFORE_RENDER as similar to buffered updates.
        #If worried about visual hitches more than perfect timing, set this to 1.
        MAX_UPDATES_BEFORE_RENDER = 5;                
        lastUpdateTime = time.time_ns(); #Store the last update time.
                                
        #If we are able to get as high as this FPS, don't render again.        
        TARGET_TIME_BETWEEN_RENDERS = 1000000000 / self.DISPLAY_FRAMERATE;                        
        lastRenderTime =time.time_ns(); #Store the last time we rendered.               
        
        #Simple timer for finding TPS and FPS.
        lastSecondTime = int(lastUpdateTime / 1000000000);

        #Main Gane Loop =============================================================
        while(self.isRunning):  
            
            now = time.time_ns(); #Current time in nanoseconds
            
            if (not self.isPaused):
                # UPDATE CALLS ============================================================                
                #Using a loop for calling tick()
                #At the very most we will update the game this many times before a new render.
                #This is done so physics is more consistent at the cost of visuals        
                currentTickCount = 0;                
                while (now - lastUpdateTime > TIME_BETWEEN_UPDATES and currentTickCount < MAX_UPDATES_BEFORE_RENDER):
                    
                    #deltaTime is multiplied to any value that changes over time: such as velocity
                    #Do not multiply deltaTime to anything that is a fixed value: such as speed, distance                    
                    deltaTime = self.UPDATE_TICKRATE * (now - lastUpdateTime)  / 1000000000           
                    
                    #Call the main update method + use deltaTime
                    self.__tick__(deltaTime);          
                             
                    #Used for Counter: for Tick rate            
                    self.updateTickCount +=1;                    
                    lastUpdateTime = now;  
                    
                    currentTickCount+=1; #To find out how many ticks we have done.
                    
                                           
                # RENDER CALLS ===========================================================
                now = time.time_ns();
                if (now - lastRenderTime > TARGET_TIME_BETWEEN_RENDERS):
                    #Call the main render method
                    self.__render__(); 
                    
                    #Used for Counter: for render rate            
                    self.displayFrameCount+=1;
                    lastRenderTime = now;                               
                
                
                #Counter: Update the frames we got for counter.============================
                currentSecondTime = int(lastUpdateTime / 1000000000);
                if (currentSecondTime > lastSecondTime):              
                   self.updateAverageTPS = self.updateTickCount;
                   self.updateTickCount = 0;             
                    
                   self.displayAverageFPS = self.displayFrameCount;
                   self.displayFrameCount = 0;             
                   
                   #refresh timer  
                   lastSecondTime = currentSecondTime;
               
            else: #if paused                 
                 lastUpdateTime = now;
                 lastRenderTime = now;
        
        self.__stop__();


#Execute this class as main class.
if __name__ == "__main__":
    game = Typocalpyse();
    

