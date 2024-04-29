import sys



#READ THIS AND DELETE
"""

WHAT WE ACTUALLY NEED TO DO:



then to deal with the function problem:
-while self.computeObj.inFunction
    -record everything that happens with conditionals and loops into new memory dict
    -you can simply modify the condit and loops current code by adding, if self.computeObj.inFunction: append all to mem
-then run can simply print out those memory collected outputs
-so we have better interconnectivity
    -instead of using inFunction inConditional etc. we should use inDifferentScope
    -this can make it easier to nest loops conditionals and functions inside each other
    -when this inDifferentScope is true, everything that adv op runs will be collected in mem


"""













#TODO:

#AFTER APPENDINF THE INSTRUCTIONS OF A FUNCTION TO THE FUNCTIONS DICT OF MEMORY, SEPARATE THEM BY NEW LINE BECAUSE THEYRE ALL IN ONE LINE

"""

PRIORITY:

#For future reference that will make things easier
-instead of doing segment[0] for operations, segment[1] for name, etc.
-make it more convenient by just doing segment[n] for op, segment[n+1] for name, etc.
-n will be 0 by default but will make things easier later when chaining operations



HOINESTLY JUST IMPLEMENT THE BASICS FIRST AND WORRY ABOUT MAKING THE MORE COMPLEX CONNECTIONS LATER

Adds: (Implement in order)
-booleans
-comparison operators, not or and < > ==
-data types (string, )
-recognize already initialized variable
-conditionals (start with comparisons)
-loops



Need to fix:
data types (sort variables accordingly)
variable recall 
(for example:
1    set var1 12
2   set added add var1 32
#in line 2, var1 should be recognized by the program as an alrdy existing variable
)


I THINK WE HAVE TO HAVE DATA TYPES INDICATORS

Main computer processes to integrate:
-I/O
-Arithmetic 
-Looping
-Conditionals
-multi word strings

idea:

***FOR FUNCTION
*for now no parameters, only void funcs, add it later when it works

#ERROR
furnish different errors


(idea for effect)
can use semicolons and colons and just strip them when wrangling

I feel like its handy to have a list of all operations and functions somewhere for an easy "if in" check.

Function ideas:
use the eval() python method to solve equations with uknown variables such as x
.length
"""


class Wrangle:
    def __init__(self, code):
        self.code = code
        self.listInstructions = []
        #splits the instructions by line anf stores them in a list
        for line in self.code.split("\n"):
            if len(line) >= 1:
                self.listInstructions.append(line)

    def single_line_separate(self, toSeparate):
        #separate one line instructions to a list
        splitted = toSeparate.split(" ")
        return splitted


class Compute:
    def __init__(self):
        self.instructionIndex = 0 #to traverse thru instructions one at a time
        #initialize memoryObj
        self.memoryObj = Memory()
        self.inIfConditional = False #switch to determine if currLine is in a conditional
        self.inIfElseConditional = False #switch to determine if currLine is in a conditional
        self.inFunction = False #switch to determine if currLine is in a function
        self.inConditional = False #switch to determine if currLine is in a conditional
        self.inLoop = False #switch to determine if currLine is in a loop
        self.loopIterator = ''
        self.loopRange = 0
        self.currInstructions = []
        self.declareFunction = False
    #VARIABLES

    def setVariable(self, segment):
        #user declares variable
        userSet = segment[0]
        varName = segment[1]

        #this is for
        if userSet == "set":
            varVal = segment[2]
            self.memoryObj.add_variable(varName, varVal)

        #operation value into a variable
        if len(segment) > 3:
            operation = segment[2]
            num1 = segment[3]
            num2 = segment[4]
            outputValue = self.arithmeticOperation(segment[2:len(segment)])
            self.memoryObj.add_variable(varName, outputValue)

    def printVariable(self, segment):
        printStatement = segment[0]
        printValue = segment[1]
        if printStatement == "out":
            #if list
            if printValue[-1] == "]":
                new=printValue.strip("[]")
                index=int(new[len(new)-1])
                lisName=new[0:len(new)-2]
                return self.memoryObj.lists[lisName][index]
            else:
                #if variable
                if printValue in self.memoryObj.variables.keys():
                    return self.memoryObj.variables[printValue]
                elif printValue in self.memoryObj.lists.keys():
                    return self.memoryObj.lists[printValue]
    
    #MATH 

    def arithmeticOperation(self, segment):
        
        #SINCE ITS FOR ONE LINE COMMDS, MIGHT AS WELL USE THIS FOR MY PROPRIETARY FUNCTIONS
        #just add them to the operations dict

        #determine what operation to be used per line, segment will be single_line_seperated()
        operator = segment[0] #since first word will be the operator in line
        operand1 = int(segment[1])
        operand2 = int(segment[2])
        operations = {"add" : self.addition(operand1, operand2),
                      "sub" : self.subtraction(operand1, operand2),
                      "mult" : self.multiplication(operand1, operand2),
                      "div" : self.division(operand1, operand2)}

        #check operator and run function accordingly
        if operator == "add":
            return operations["add"]
        elif operator == "sub":
            return operations["sub"]
        elif operator == "mult":
            return operations["mult"]
        elif operator == "div":
            return operations["div"]
        else: 
            return 0

    def addition(self, one, two):
        return one + two
    def subtraction(self, one, two):
        return one - two
    def multiplication(self, one, two):
        return one * two
    def division(self, one, two):
        return one / two

    #LIST
    def createList(self, segment):
        #format: list lisName {1,2,3,4,5}
        #strip the curly brackets and split by comma
        if segment[0] == "list":
            #split the list contents
            contents = segment[2].strip(" {}").split(",")
            #add list to memory
            self.memoryObj.add_list(segment[1], contents)

    def appendList(self, segment):
        if segment[0] == "append":
            #if index provided
            if len(segment) > 3:
                index = segment[4]
                self.memoryObj.add_list(segment[1], segment[2], index)
            else:
                self.memoryObj.add_list(segment[1], segment[2])

    #accessing list is done through the out variable
    #now figure out how to do list indices, also will be in the out variable

    def removeList(self, segment): 
        if segment[0] == "remove":
            lisName = segment[1]
            lisInd = segment[2]
            self.memoryObj.remove_list(lisName, lisInd)


    #LOOPING
    #syntax (loop i for n < #code >)
    def loopingCheck(self, segment):
        if segment[0] == "loop":
            self.inLoop = True
            self.loopIterator = segment[1]
            self.loopRange = segment[3]

    #while inloop collect operations
    def loopCollect(self, line):
        self.memoryObj.loopOps.append(line)

    #CONDITIONALS
    #start with simple if else that takes conditional as expression
    def conditionalCheck(self, segment):
        #running while self.inIfConditional or self.inIfElseConditional is True
        #pretty sure u can also use self.currInstructions
        #self.isConditional in the __init__
        #my syntax will be if for single if statement and if else for ifelse statement
        if segment[0] == "if":
            self.inConditional = True
            ifComparisonCheck = self.comparisonCheck(segment[1:])
            if ifComparisonCheck: #if true, scope runs
                self.inIfConditional = True

        if segment[0] == "ifelse":
            self.inConditional = True
            ifComparisonCheck = self.comparisonCheck(segment[1:])
            if ifComparisonCheck: #if true, scope runs
                self.inIfElseConditional = True
        #FOR NOW IT SETS THE BOOLEAN SWITCH TO TRUE WHICH MEANS RUN THE SUBSEQUENT STATEMENTS INSIDE THE CONDITIONAL scope 


    #COMPARISON OPERATORS

    #check if number using isdigit(), if not then its most likely in the variables dict
    def comparisonCheck(self, segment, index=0):
        #one line comparisons syntax: compare var1 > var2   returns boolean
        #can be reusable with the index param
        if segment[0] == "compare":
            comp1 = segment[1]
            compOp = segment[2]
            comp2 = segment[3]
        compOps = ["<", ">", "==", "!=", "<=", ">="]
        result = False
        if compOp == "<":
            if comp1 < comp2:
                result = True
        elif compOp == ">":
            if comp1 > comp2:
                result = True
        elif compOp == "==":
            if comp1 == comp2:
                result = True
        elif compOp == "!=":
            if comp1 != comp2:
                result = True
        elif compOp == "<=":
            if comp1 <= comp2:
                result = True
        elif compOp == ">=":
            if comp1 >= comp2:
                result = True
        return result
        

    #FUNCTIONS
    def determineFunction(self, fragments):     #Puts user function into the memory
        #self.inFunction is in the compute init
        if fragments[0] == "function": #user wants to declare function and set name
            self.currNewFuncName = fragments[1]
            self.declareFunction = True
        if fragments[0] == "<":  #start of user function
            self.inFunction = True
        if fragments[0] == ">":  #end of user function
            self.declareFunction = False
            self.inFunction = False
            self.currInstructions = [] #clears it again

        if self.inFunction == True:
            self.currInstructions = [fragments]
            if self.currNewFuncName in self.memoryObj.functions.keys():
                self.memoryObj.functions[self.currNewFuncName] += self.currInstructions
            else:
                self.memoryObj.add_function(self.currNewFuncName, self.currInstructions)
            
        #self.memoryObj[funcName].strip("<>")

    
    def runFunction(self, segment):
        #segment.strip("():")
        if segment[0] == "run":
            funcname = segment[1]
        return self.memoryObj.functions[funcname]
    
    def printDict(self):
        print(self.memoryObj.functions)
        print(self.memoryObj.lists)
        print(self.memoryObj.variables)

class Main:
    def __init__(self):
        codeTxtFile = open(sys.argv[1], "r+")
        #this is also where you should output the beginning message, create some graphics
        #close the file once wrangled to save space: codeFile.close()
        codeTxt = codeTxtFile.read()
        wrangledCode = Wrangle(codeTxt)
        #initialize compute object
        self.computeObj = Compute()

        self.operations = ['list', 'append', 'remove', 'add', 'sub', 'mult', 'div', 'set', 'out', 'compare']

        """TEST"""
        for line in wrangledCode.listInstructions:

            newLine = wrangledCode.single_line_separate(line)
            #NORMAL OPERATIONS
            if newLine[0] in self.operations and self.computeObj.inFunction == False and self.computeObj.inConditional == False and self.computeObj.inLoop == False:
                #normal one line ops
                self.determineOperation(newLine, 0)
            #FUNCTIONS
            if newLine[0] == "function":
                #in function scope
                self.computeObj.determineFunction(newLine)
            if self.computeObj.declareFunction:
                self.computeObj.determineFunction(newLine)

            #run the function
            if newLine[0] == "run":
                instructions = self.computeObj.runFunction(newLine)
                for instruction in instructions[1:len(instructions)]:
                    self.determineOperation(instruction)
                    #this is where you will print the conditionals and loops in memory

            #CONDITIONALS
            if newLine[0] == "if" or newLine[0] == "ifelse":
                #in conditional scope
                self.computeObj.conditionalCheck(newLine)
            if self.computeObj.inIfConditional:
                self.determineOperation(newLine)
            if self.computeObj.inIfElseConditional:
                self.determineOperation(newLine)
            #ELSE in ifelse WORKS
            if (self.computeObj.inIfElseConditional == False) and self.computeObj.inConditional and not self.computeObj.inIfConditional:
                if newLine[0] == ":":
                    self.computeObj.inIfElseConditional = True
                    continue
            #IF in ifelse 
            if self.computeObj.inIfElseConditional and self.computeObj.inConditional:
                if newLine[0] == ":":
                    self.computeObj.inIfElseConditional = False
                    continue
            #break scope
            if newLine[0]==")" and self.computeObj.inConditional:
                self.computeObj.inConditional = False
                self.computeObj.inIfConditional=False
                self.computeObj.inIfElseConditional=False

            #LOOPING
            if newLine[0] == "loop":
                self.computeObj.loopingCheck(newLine)
            if self.computeObj.inLoop:
                self.computeObj.loopCollect(newLine)
            if newLine[0] == "}" and self.computeObj.inLoop:
                self.computeObj.inLoop = False
                for m in range(int(self.computeObj.loopRange)):
                    self.computeObj.memoryObj.variables[self.computeObj.loopIterator] = m
                    for instruction in self.computeObj.memoryObj.loopOps:
                        self.determineOperation(instruction)
        
        #TEST
        #self.computeObj.printDict()

    """
    HOW IS THIS GONNA WORK???
    -so the problem is that each advanced op only uses determine function for each
    -we need connectivity
    -maybe each function will simply flip the boolean switches
    
    """


    def determineOperation(self, segment, index=0):  #index will be useful in the future
        if segment[index] == "add":
            print(">> " ,self.computeObj.arithmeticOperation(segment))
        elif segment[index] == "sub":
            print(">> " ,self.computeObj.arithmeticOperation(segment))
        elif segment[index] == "mult":
            print(">> " ,self.computeObj.arithmeticOperation(segment))
        elif segment[index] == "div":
            print(">> " ,self.computeObj.arithmeticOperation(segment))
        elif segment[index] == "set":
            self.computeObj.setVariable(segment)
        elif segment[index] == "out":
            print(">>",self.computeObj.printVariable(segment))
        elif segment[index] == "list":
            print(">> Created List: " + segment[1])
            self.computeObj.createList(segment)
        elif segment[index] == "append":
            self.computeObj.appendList(segment)
        elif segment[index] == "remove":
            self.computeObj.removeList(segment)
        elif segment[index] == "compare":
            print(">>",self.computeObj.comparisonCheck(segment))
        #else:
        #    print("###There was an error###") #This is where you will put the errors once its made

        #the arithmetic operations here are only for one line operations
        """
        list of instructions will be wrangledCode
        go through every instruction and removing them after its finished
        will have to hardcode every function
        """
        


class Memory:
    #store all data and variable sorted in a category
    #make sure to implement indexes
    def __init__(self):
        self.variables = {} #set user declared variabled
        self.functions = {} #set user declared functions
        self.functionOperations = {} #this is where you will store all the outputs of conditionals and loops
        self.lists = {}
        self.ifelse = []
        self.loopOps = []

    #appends new variable name with set value
    #works well because it can replace the value if same variable name
    def add_variable(self, var, val):
        self.variables[var] = val

    def remove_variable(self, removeKey):
        pass

    def add_function(self, funcName, instruction): #instruction is a list of instructsns
        self.functions[funcName] = instruction
        #when instructions want to be called just run it with the determineOperation

    def add_list(self, listName, contents, index=-1):
        if listName not in self.lists.keys():
            #if dont exist, creates a list
            self.lists[listName] = contents 
        else:
            #if exists, appends it to existing list
            self.lists[listName].insert(int(index), contents)

    def remove_list(self, listName, index):
        if listName in self.lists.keys():
            self.lists[listName].pop(int(index))

#DRIVER CODE        
run = Main()




"""
DO THIS FIRST!!!!
#THE PROBLEM IS THE SHITS INSIDE THE FUNCTION ONLY DOES THE determineOperation() so you cant do loop and conditional inside function
-in the main class, create another operation that deals with the conditionals, looping, and function
-basically, everthing in the for line in wrangledCode.listInstructions:, tinker it to have a better semantic analysis


WHAT I HAVE SO FAR:
-declare variables and also setting expressions to variables
-arithmetics
-returning variables
-setting functions
-running functions
-list create print append remove
-conditionals (if and ifelse)
-looping
    -for now its only going to loop n times not being able to use iterators
    -able to use the iterator inside the scope

CURRENT:
-looping
    -can do more ops with iterator
-when using ops such as out, check if the thing is a variable in the memory class so you can use it.

WHATS NEXT:
-FOR FUTURE UPDATE: make it easier by going through each line by token instead of parsing the line itself, makes it easier for more complex, combined ops
-best to have an instanceOf type deal to handle certain types better (ex:strings > 1)
-looping (should be complete)
-little functions (.length, etc.)
-elifs
-and/or/not 

"""

"""
#DOCUMENTATION

#variables

set varName Kris
out varName

*can also do
set varAdd add 54 75
out varAdd

#simple arithmetic
sub 700 8637

#functions
function addPrint
<
set name1 Kris
out name1
>
run addPrint

#lists
list lisName {1,2,3,4,5}
append lisName 9 at 2           *append 9 to index 2
out lisName[2]
out lisName
remove lisName 2

#conditionals
if compare 32 > 2
(
set m 23
out m
)

ifelse compare 33 == 54
(
set res istrue
out res
:
set res nottrue
out res
)
* ":" is the delimiter

#loops
loop i for 5
{
out i
}

"""
            
