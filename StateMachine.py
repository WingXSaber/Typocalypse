from tabulate import tabulate

class State():
    def __init__(self, name = "", alias = ""):
        self.transitionStates = {};
        """
        initialize Dictionary
        Format:
               key : value
        where:
              key = a string name of the next state, acts as 'conditon'
              value = [state, inputDescription]
                      where:
                           [0]state: next State
                           [1]inputDescription: a string of words detatiling the transition
        """        
        self.name = name;
        self.alias = alias;
        
    def getNext(self, input):
        if(len(self.transitionStates) == 0):
            print("Cannot move, this is a final state.");
        else:
            if(input in self.transitionStates):
                #Get Next State
                next_state, input_description = self.transitionStates[input]                                 
                return next_state;            
            else:
                print("Error, unable to do transition. Invalid: "+str(input));
        return self; #Indicate unsuccessful transition
    
    def isFinalState(self):
        if(len(self.transitionStates) <= 0):
            return True;
        else:
            return False;
    
    def connect(self, state, inputDescription):
        self.transitionStates[str(state)] = [state, inputDescription];
        
    def __str__(self):
        #return self.__class__.__name__;
        return self.name;


# Generate and display the transition table
def generate_transition_table(state, stateExplored = None):
    table = []
    #stateExplored = []#to prevent recursion error
    
    if(stateExplored is None):  #Because default parameter become static / does not reset
        stateExplored = [];        
    
    if(state.name not in stateExplored):   
        stateExplored.append(state.name);    
        if(not state.isFinalState()):
            for _, (next_state, inputDescription) in state.transitionStates.items():
                #table.append((state, input, inputDescription, next_state))
                table.append((state.name, state.alias, inputDescription, next_state.name))
                table.extend(generate_transition_table(next_state, stateExplored)) #Recursive method call        
        else:
            #If encountering a final State
            table.append((state.name, state.alias, "Final State", "None"));
    
    stateExplored = None
    #return table #unsorted table
    return sorted(table, key=lambda table: str(table[0])); #sorted by First Column 

def TransitionTableToString(transition_table):
    headers = [("State", "Alias", "Input Description", "Next State"), ("-----", "-----", "-----------------", "----------")];
    #return str(tabulate(transition_table, headers=headers));
    for i in transition_table:
        headers.append(i);
    return headers;







#sample code on how to initialize a State Machine on a different file
"""
#from StateMachine import State
def intializeStateMachine():
    q0 = State("q0", "idle");
    q1 = State("q1", "walking");
    q2 = State("q2", "Final");

    #connect
    q0.connect(q1, "presses NORMAL");
    q0.connect(q2, "Takes SHORTCUT");        
    
    q1.connect(q0, "Loop");
    q1.connect(q2, "End");    
    
    return q0; 
    
head = intializeStateMachine();

"""


#Sample code on how to use  generate_transition_table(state) on a different file
"""
#from StateMachine import generate_transition_table

transition_table = generate_transition_table(head)
headers = ["State", "Alias", "Input Description", "Next State"]
string = tabulate(transition_table, headers=headers)

#print(repr(string));           #print raw string
for i in string.splitlines():   #line by line print
    print(i);
    
print("Current State: ", head);
head.next("q1"); #Sample to traverse
print("Taversed to q1");    
print("is head final state? " +str(head.isFinalState()));

print();
transition_table = generate_transition_table(head)
headers = ["State",  "Alias", "Input Description", "Next State"]
print(tabulate(transition_table, headers=headers))

print();
print("Current State: ", head);
head.next("q2");
print("Taversed to q2");  
print("is head final state? " +str(head.isFinalState()));

print();
transition_table = generate_transition_table(head)
print(tabulate(transition_table, headers=headers))
"""