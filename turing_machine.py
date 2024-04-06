# Five Tuple Turing Machine Implementation
# Based on https://morphett.info/turing/turing.html

class Instruction:
    def __init__(self, current_state, current_symbol, new_symbol, direction, new_state):
        self.current_state = current_state
        self.current_symbol = current_symbol
        self.new_symbol = new_symbol
        self.direction = direction
        self.new_state = new_state

    def __str__(self):
        return  f"{self.current_state} {self.current_symbol} {self.new_symbol} {self.direction} {self.new_state}"

    def convertStringToInstruction(s):
        tokens = s.split(" ");
        current_state = tokens[0].strip()
        current_symbol = tokens[1].strip()
        new_symbol = tokens[2].strip()
        direction = tokens[3].strip()
        new_state = tokens[4].strip()
        
        return Instruction(current_state, current_symbol, new_symbol, direction, new_state)

class Tape:
    def __init__(self, initial_input):
        self.symbols = []
        
        self.index = 0
        for symbol in initial_input:
            # * Used to denote starting index (default is 0)
            if symbol == "*":
                self.index = initial_input.index("*")
            else:
                self.symbols.append(symbol)
        
    def read(self):
        if len(self.symbols) > 0:
            return self.symbols[self.index]
        else:
            return " "
        
    def write(self, symbol):
        if len(self.symbols) > 0:
            self.symbols[self.index] = symbol
        else:
            self.symbols.append(symbol)
        
    def delete_current_symbol(self):
        del(self.symbols[self.index])
        
    def right(self):
        self.index += 1
        if(self.index==len(self.symbols)):
            self.symbols.append(" ")
            
    def left(self):
        self.index -= 1
        if(self.index==-1):
            self.symbols.insert(0, " ")
            self.index = 0
            
    def __str__(self):
        result =""
        for symbol in self.symbols:
            result += symbol
            
        result += "\n"
        
        for i in range(self.index):
            result += " "
            
        result += "^"
        
        return result
        
class TuringMachine:
    def __init__(self, initial_input, initial_state, program):
        self.tape = Tape(initial_input)
        self.state = initial_state
        self.running = True
        self.print_tape = False
        self.step_through = False
        self.current_instruction = None

        # Parse lines and convert to instruction objects
        lines = program.split("\n")
        self.instructions = []
        for line in lines:
            # Skip Empty line
            if(len(line)==0):
                continue
            # Skip Comment
            elif(line[0]==";"):
                continue
            else:
                instruction = Instruction.convertStringToInstruction(line)
                self.instructions.append(instruction)    
    
    def findInstruction(self, state):
        for instruction in self.instructions:
            # Check if state matches (exact or wild card)
            if((instruction.current_state == state) or (instruction.current_state == "*")):                

                # Check if the current symbol matches
                # Symbol is space (Represented by _)
                
                # Check for space (represented by _)
                is_same_symbol = (instruction.current_symbol == "_" and self.tape.read() == " ")
                
                # Symbol is same, or wildcard
                is_same_symbol = is_same_symbol or instruction.current_symbol in [self.tape.read(), "*"]
                
                if is_same_symbol:
                    return instruction
        return None
    
    def step(self):
        # Fetch instruction basted on state
            self.instruction = self.findInstruction(self.state)
            # self.current_instruction = instruction
            
            # If not instruction found print error and exit
            if(not self.instruction):
                print(f"No matching instruction found for State: {self.state}")
                self.running = False
                return
                
            # Write
            if(self.instruction.new_symbol not in [";", "*", "_", " "]):
                self.tape.write(self.instruction.new_symbol)
            # Delete symbol
            elif(self.instruction.new_symbol == "_"):
                self.tape.write(" ")
                
            # Move Head
            if(self.instruction.direction == "r"):
                self.tape.right();
            
            if(self.instruction.direction == "l"):
                self.tape.left()
                
            # State
            self.state = self.instruction.new_state
            
            # Check if state is halted
            if(len(self.state)>3 and self.state[0:4]=="halt"):
                self.running = False;
                
            # Print tape
            if(self.print_tape):
                print(self.tape)
    
    def run(self):
        self.running = True
        count = 0
        
        print("Tape Start: ")
        print(self.tape)
        
        while(self.running):
            count += 1
            
            self.step()
            
            if(self.step_through):
                input()
        
        print("\nTape End: ")
        print(self.tape)
        print(f"Num of steps: {count}")
            

# Program from: https://morphett.info/turing/turing.html
program = """
; This example program checks if the input string is a binary palindrome.
; Input: a string of 0's and 1's, eg '1001001'


; Machine starts in state 0.

; State 0: read the leftmost symbol
0 0 _ r 1o
0 1 _ r 1i
0 _ _ * accept     ; Empty input

; State 1o, 1i: find the rightmost symbol
1o _ _ l 2o
1o * * r 1o

1i _ _ l 2i
1i * * r 1i

; State 2o, 2i: check if the rightmost symbol matches the most recently read left-hand symbol
2o 0 _ l 3
2o _ _ * accept
2o * * * reject

2i 1 _ l 3
2i _ _ * accept
2i * * * reject

; State 3, 4: return to left end of remaining input
3 _ _ * accept
3 * * l 4
4 _ _ r 0  ; Back to the beginning
4 * * l 4

accept * : r accept2
accept2 * ) * halt-accept

reject _ : r reject2
reject * _ l reject
reject2 * ( * halt-reject
"""

if(__name__ == "__main__"):
    print("Python Turing Machine Implementation\n")
    
    initial_value = "1001001"
    initial_state = "0"
    
    turing_machine = TuringMachine(initial_value, initial_state, program)
    
    print("Program")
    for instruction in turing_machine.instructions:
        print(instruction)
    
    input("\n\nPress ENTER to run program. > ")
    turing_machine.run()

    input("\n\nPress ENTER to close window. > ")
