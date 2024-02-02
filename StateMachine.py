from tabulate import tabulate

class State():
    def __init__(self, name = ""):
        #initialize Dictionary
        #Format:
        #       key : value
        #where:
        #      key = a string name of the next state, acts as 'conditon'
        #      value = [state, inputDescription]
        #              where:
        #                   [0]state: next State
        #                   [1]inputDescription: a string of words detatiling the transition
        self.transitionStates = {};
        self.name = name;
        
    def next(self, input):
        if(self.transitionStates == {}):
            print("Cannot move, this is a final state.");
        else:
            if(input in self.transitionStates):
                #Get Next State
                next_state, input_description = self.transitionStates[input]                
                
                #Turn that next State as current State
                self.__init__(next_state.name)  # Reinitialize the current state with the next state
                self.transitionStates = next_state.transitionStates; # Update transitionStates
                
                return True  # Indicate successful transition
            
                #return self.transitionStates[input][0]; #get the state [0]
            else:
                print("Error, unable to do transition. Invalid: "+str(input));
        return False; #Indicate unsuccessful transition
    
    def isFinalState(self):
        return self.transitionStates == {};
    
    def connect(self, input, state, inputDescription):
        self.transitionStates[input] = [state, inputDescription];
        
    def __str__(self):
        #return self.__class__.__name__;
        return self.name;


# Generate and display the transition table
def generate_transition_table(state):
    table = []
    for input, (next_state, inputDescription) in state.transitionStates.items():
        #table.append((state, input, inputDescription, next_state))
        table.append((state, inputDescription, next_state))
        table.extend(generate_transition_table(next_state)) #Recursive method call
    return table




#sample code on how to initialize a State Machine on a different file

#from StateMachine import State

def intializeStateMachine():
    q0 = State("q0");
    q1 = State("q1");
    q2 = State("q2");

    #connect
    q0.connect("q1", q1, "presses NORMAL");
    q0.connect("q2", q2, "Takes SHORTCUT");

    q1.connect("q2", q2, "NORMALly ends");
    return q0
    
head = intializeStateMachine();







#Sample code on how to use  generate_transition_table(state) on a different file
#from StateMachine import generate_transition_table

transition_table = generate_transition_table(head)
headers = ["State", "Input Description", "Next State"]
string = tabulate(transition_table, headers=headers)

#print(repr(string));           #print raw string
for i in string.splitlines():   #line by line print
    print(i);
    
print();
print("Taversing..");    
head.next("q1"); #Sample to traverse
print("is head final state? " +str(head.isFinalState()));
print();

transition_table = generate_transition_table(head)
headers = ["State", "Input Description", "Next State"]
print(tabulate(transition_table, headers=headers))

head.next("q2");
print("is head final state? " +str(head.isFinalState()));
