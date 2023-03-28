'''
Logan Choi
Professor Morales
Intro to AI 
Puzzle #2
'''
#This is just the function/Class file so it looks a bit cleaner
import random
import sys

'''
the class State is to just generate all the different states with
absolutely necesssary information. 
'''
class State:
    def __init__(self, pengu=[], fishes=[],score = 0,moveStr = ""):
        self.pengu = pengu
        self.fishes = fishes
        self.score = score
        self.moveStr = moveStr
        self.dead = False

    '''
    this just manually deepcopies my new State
    '''
    def deepcopy(self, state):
        self.pengu = state.pengu[:]
        self.fishes = state.fishes[:]
        self.score = state.score
        self.moveStr = state.moveStr
        self.dead = state.dead

    '''
    this is the heuristic function. It takes the current state score and subtracts 
    how many moves it already has done. This way it puts loops in lower priority.
    My 'optimism' is that if you already have a lot of fish then you might as well keep going
    with that state.
    '''
    def heuristic(self):
        return self.score
    
    '''
    This compares the heuristics of each entry in the heap.
    I made it a max heap.
    '''
    def __lt__(self,other):
        return self.heuristic() > other.heuristic()

'''
print_board just writes the matrix in the output file
row by row
'''
def print_board(matrix,row,col,newState,fout):
    #Check if penguin is dead
    if newState.dead == True:
        matrix[newState.pengu[0]][newState.pengu[1]] = "X"
    else:
        matrix[newState.pengu[0]][newState.pengu[1]] = "P"
    for x in range(0,row):
        for y in range(0,col):
            if matrix[x][y] == '*':
                if [x,y] in newState.fishes:
                    fout.write(" ")
                else:
                    fout.write("*")
            else:
                fout.write(matrix[x][y])
        fout.write("\n")

'''
output() just takes the state and writes its parameters on the output file
'''
def output(matrix,row,col,newState):
    fout = open(sys.argv[2],'w')
    fout.write(newState.moveStr + '\n')
    fout.write(str(newState.score) + '\n')
    print_board(matrix,row,col,newState,fout)
    fout.close()

'''
get_board just builds the matrix and takes the row, col, and file input
as parameters. It builds the matrix row by row, and returns the matrix
and position of penguin
'''
def get_board(row,col,fin):
    matrix = []
    fishPos = []
    for x in range(0,row):
        newRow = list(fin.readline())
        for y in range(0,col):
            if newRow[y] == "P":
                pengu_pos = [x,y]
                newRow[y] = " "
        matrix.append(newRow)
    print("GOT BOARD")
    return matrix,pengu_pos,fishPos


'''
Get Valid_moves checks each surrounding cell block of the penguin's position
and sees if it's a wall or not
'''
def get_valid_moves(matrix,pengu_pos):
    #just encoded the moves as a dictionary
    dir = {'1':[1,-1], '2':[1,0], '3':[1,1], '4':[0,-1], 
             '6':[0,1], '7':[-1,-1], '8':[-1,0], '9':[-1,1]}
    WALL = "#"
    #List that will be returned for valid moves
    valid = []

    #Check each move 
    for x in dir.keys():
        if matrix[dir[x][0] + pengu_pos[0]][dir[x][1] + pengu_pos[1]] != WALL:
            valid.append(x)

    return valid

'''
make_move takes in paramters and boolean markers as an encoding of the state
Then it moves the penguin accordinngly
'''
def make_move(move,matrix,state):

    #Moves encoded as a dictionary
    dir = {'1':[1,-1], '2':[1,0], '3':[1,1], '4':[0,-1], 
             '6':[0,1], '7':[-1,-1], '8':[-1,0], '9':[-1,1]}
    S_BLOCK = '0'
    F_BLOCK = '*'
    WALL = '#'

    #Easier to just say hazard as a list
    hazard = ['U','S']

    #Continue to move depending in the direction
    #stop if you hit hazard, snow, or wall.
    while True:
        state.pengu[0] += dir[move][0]
        state.pengu[1] += dir[move][1]
        #Penguin in that snow position for now
        if matrix[state.pengu[0]][state.pengu[1]] == S_BLOCK:
            return
        #If hit ice with fish, increment and set that position
        #as empty ice 
        elif matrix[state.pengu[0]][state.pengu[1]] == F_BLOCK:
            if [state.pengu[0],state.pengu[1]] not in state.fishes:
                state.score += 1
                state.fishes.append([state.pengu[0],state.pengu[1]])
        #If hit wall, decrement and then set penguin position
        elif matrix[state.pengu[0]][state.pengu[1]] == WALL :
            state.pengu[0] -= dir[move][0]
            state.pengu[1] -= dir[move][1]
            return
        #If hit hazard, you dead bruh. GG and F in chat
        #and set death marker as True
        elif matrix[state.pengu[0]][state.pengu[1]] in hazard:
            state.dead = True
            return