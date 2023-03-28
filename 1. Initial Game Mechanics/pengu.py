'''
Logan Choi
Professor Morales
Intro to AI 
Puzzle #1
'''
import random
import sys


'''
get_board just builds the matrix and takes the row, col, and file input
as parameters. It builds the matrix row by row, and returns the matrix
and position of penguin
'''
def get_board(row,col,fin):
    matrix = []
    for x in range(0,row):
        newRow = list(fin.readline())
        if "P" in newRow:
            y = newRow.index("P")
            pengu_pos = [x,y]
        matrix.append(newRow)
    
    return matrix,pengu_pos

'''
print_board just writes the matrix in the output file
row by row
'''
def print_board(matrix,row,col,fout):
    for x in range(0,row):
        for y in range(0,col):
            fout.write(matrix[x][y])
        fout.write("\n")

'''
Get Valid_moves checks each surrounding cell block of the penguin's position
and sees if it's a wall or not
'''
def get_valid_moves(matrix,pengu_pos):
    #I just encoded the moves as a dictionary
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
def make_move(move,matrix,pengu_pos,snow,score,death):
    #Moves encoded as a dictionary
    dir = {'1':[1,-1], '2':[1,0], '3':[1,1], '4':[0,-1], 
             '6':[0,1], '7':[-1,-1], '8':[-1,0], '9':[-1,1]}
    S_BLOCK = '0'
    I_BLOCK = ' '
    P_BLOCK = 'P'
    F_BLOCK = '*'
    DEAD = 'X'
    WALL = '#'

    #Easier to just say hazard as a list
    hazard = ['U','S']
    
    #If snow is true, then that means we need to reset that cell
    #as a snow block and not an empty ice one
    if snow:
        matrix[pengu_pos[0]][pengu_pos[1]] = S_BLOCK
        snow = False
    else:
        matrix[pengu_pos[0]][pengu_pos[1]] = I_BLOCK

    #Continue to move depending in the direction
    #stop if you hit hazard, snow, or wall.
    while True:
        pengu_pos[0] += dir[move][0]
        pengu_pos[1] += dir[move][1]
        #if hit snow, set snow marker as True and put
        #Penguin in that position for now
        if matrix[pengu_pos[0]][pengu_pos[1]] == S_BLOCK:
            snow = True
            matrix[pengu_pos[0]][pengu_pos[1]] = P_BLOCK
            return(matrix,pengu_pos,snow,score,death)
        #If hit ice with fish, increment and set that position
        #as empty ice 
        elif matrix[pengu_pos[0]][pengu_pos[1]] == F_BLOCK:
            score += 1
            matrix[pengu_pos[0]][pengu_pos[1]] = I_BLOCK
        #If hit wall, decrement and then set penguin position
        elif matrix[pengu_pos[0]][pengu_pos[1]] == WALL :
            pengu_pos[0] -= dir[move][0]
            pengu_pos[1] -= dir[move][1]
            matrix[pengu_pos[0]][pengu_pos[1]] = P_BLOCK
            return(matrix,pengu_pos,snow,score,death)
        #If hit hazard, you dead bruh. GG and F in chat
        #set position as 'X' for death and set death marker as True
        elif matrix[pengu_pos[0]][pengu_pos[1]] in hazard:
            matrix[pengu_pos[0]][pengu_pos[1]] = DEAD
            death = True
            return (matrix,pengu_pos,snow,score,death)
        
'''
fish_check just checks if all the fish has been taken
'''
def fish_check(matrix,row,col):
    F_BLOCK = '*'
    #go through every cell, and if it's a fish then return false
    for x in range(0,row):
        for y in range(0,col):
            if matrix[x][y] == F_BLOCK:
                return False
    return True

'''
play() just actually makes the moves multiple times
'''
def play(matrix,row,col,pengu_pos):
    death = False
    numMoves = 0
    all_fish = False
    snow = False
    score = 0
    moveString = ""

    #play while you are not dead, you haven't done 6 moves, and if 
    #all fish are not taken
    while not death and numMoves != 6 and not all_fish:
        #get list of valid moves
        valid_moves = get_valid_moves(matrix,pengu_pos)
        #get random move from the list
        move = random.choice(valid_moves)
        moveString = moveString + str(move)
        #actually make the move
        matrix,pengu_pos,snow,score,death = make_move(move,matrix,pengu_pos,snow,score,death)
        #check all the fish taken
        all_fish = fish_check(matrix,row,col)
        #increment numMoves
        numMoves += 1

    #output all the results into the output file
    fout = open(sys.argv[2],'w')
    fout.write(moveString + '\n')
    fout.write(str(score) + '\n')
    print_board(matrix,row,col,fout)
    fout.close()
    

if __name__ == "__main__":
    #Open input file
    fin = open(sys.argv[1],'r')

    #Get row and column
    row,col = fin.readline().split()
    row = int(row)
    col = int(col)

    #Get_board function will build the matrix and 
    #get penguin position
    matrix, pengu_pos = get_board(row,col,fin)
    fin.close()

    #Play the game
    play(matrix,row,col,pengu_pos)

    

